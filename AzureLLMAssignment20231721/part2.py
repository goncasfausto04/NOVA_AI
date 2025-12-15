import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
)

MODEL_NAME = "gpt-4o"


# TV CLASS

class Television:
    def __init__(self):
        self.state = False
        self.volume = 20
        self.brightness = 50
        self.current_channel = 1
        self.channel_list = {
            1: "RTP",
            2: "RTP2",
            3: "SIC",
            4: "TVI",
            5: "ARTV",
            6: "CNN",
            7: "CMTV",
            8: "Disney Channel",
            9: "Cartoon Network",
            10: "Nickelodeon",
        }

    def turn_on(self):
        self.state = True
        return "The television is now ON."

    def turn_off(self):
        self.state = False
        return "The television is now OFF."

    def set_volume(self, volume):
        if not self.state:
            return "TV is OFF. Turn it on first."
        if not 0 <= volume <= 100:
            return "Volume must be between 0 and 100."
        self.volume = volume
        return f"Volume set to {self.volume}."

    def set_brightness(self, brightness):
        if not self.state:
            return "TV is OFF. Turn it on first."
        if not 0 <= brightness <= 100:
            return "Brightness must be between 0 and 100."
        self.brightness = brightness
        return f"Brightness set to {self.brightness}."

    def change_channel(self, channel):
        if not self.state:
            return "TV is OFF. Turn it on first."
        if channel not in self.channel_list:
            return "Invalid channel number."
        self.current_channel = channel
        return f"Channel changed to {self.channel_list[channel]}."

    def show_channels(self):
        if not self.state:
            return "TV is OFF. Turn it on first."
        return ", ".join(
            f"{num} - {name}" for num, name in self.channel_list.items()
        )

    def get_status(self):
        if not self.state:
            return "Television is OFF."
        return (
            f"ON | Volume: {self.volume} | Brightness: {self.brightness} | "
            f"Channel: {self.channel_list[self.current_channel]}"
        )


# TV AI BOT

class TVAIBOT:
    def __init__(self, client: AzureOpenAI):
        self.client = client
        self.conversation_history = []
        self.system_prompt = """
You are a friendly TV control assistant that helps users control their television.

Available actions:
- turn_on / turn_off
- set_volume (0–100)
- set_brightness (0–100)
- change_channel (1–10)
- show_channels
- get_status

Channels:
1 = RTP
2 = RTP2
3 = SIC
4 = TVI
5 = ARTV
6 = CNN
7 = CMTV
8 = Disney Channel
9 = Cartoon Network
10 = Nickelodeon

IMPORTANT RULES:
1. Use conversation context to understand what the user wants
2. If a user says "set it to 50" after asking about volume, infer they mean volume
3. Only ask for clarification when truly ambiguous
4. Be conversational but always return valid JSON
5. Never guess critical values like channel numbers
6. When user mentions a channel by name, map it to the correct number

RESPONSE FORMATS:
{"action": "turn_on"}
{"action": "set_volume", "value": 30}
{"action": "change_channel", "value": 5}
{"ask": "question to clarify"}
{"error": "error description"}

Example multi-turn:
User: "I want to watch something"
You: {"ask": "Which channel would you like? Available channels: 1-RTP, 2-RTP2, 3-SIC, 4-TVI, 5-ARTV, 6-CNN, 7-CMTV, 8-Disney Channel, 9-Cartoon Network, 10-Nickelodeon"}
User: "CNN"
You: {"action": "change_channel", "value": 6}
"""

    def process(self, user_input: str) -> dict:
        # Add user message to conversation history
        self.conversation_history.append(
            {"role": "user", "content": user_input}
        )
        
        # Build messages with system prompt + conversation history
        messages = [
            {"role": "system", "content": self.system_prompt}
        ] + self.conversation_history
        
        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0,
            )
            
            content = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversation_history.append(
                {"role": "assistant", "content": content}
            )
            
            # Keep only last 10 messages to avoid token limits
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return json.loads(content)
            
        except json.JSONDecodeError:
            return {"error": "AI returned invalid JSON."}
        except Exception as e:
            return {"error": f"API error: {str(e)}"}



# EXECUTION

def execute_action(tv: Television, result: dict) -> tuple[str, bool]:
    """
    Returns (response_message, is_question)
    is_question tells us if AI is asking for clarification
    """
    if "ask" in result:
        return result["ask"], True

    if "error" in result:
        return result["error"], False

    action = result.get("action")

    if action == "turn_on":
        return tv.turn_on(), False
    if action == "turn_off":
        return tv.turn_off(), False
    if action == "set_volume":
        return tv.set_volume(result["value"]), False
    if action == "set_brightness":
        return tv.set_brightness(result["value"]), False
    if action == "change_channel":
        return tv.change_channel(result["value"]), False
    if action == "show_channels":
        return tv.show_channels(), False
    if action == "get_status":
        return tv.get_status(), False

    return "Unknown action.", False


# RUN THE BOT

if __name__ == "__main__":
    tv = Television()
    bot = TVAIBOT(client)

    print("TV AI ready. Talk to it like a normal person. Type 'exit' to quit.")
    print(f"Current Status: {tv.get_status()}\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in {"exit", "quit"}:
            print("AI: Powering down. Bye 👋")
            break

        ai_result = bot.process(user_input)
        response, is_question = execute_action(tv, ai_result)
        
        print(f"AI: {response}")
        
        if not is_question:
            print("----------------------------------")
            print(f"Current TV Status: {tv.get_status()}")
            print("----------------------------------")
        
        print()  