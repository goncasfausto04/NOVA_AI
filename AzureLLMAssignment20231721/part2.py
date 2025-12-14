import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI

# =======================
# ENV + AZURE CONFIG
# =======================

load_dotenv()

client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
)

MODEL_NAME = "gpt-4o"


# =======================
# TELEVISION CLASS
# =======================

class Television:
    def __init__(self):
        self.state = False
        self.volume = 20
        self.brightness = 50
        self.current_channel = 1
        self.channel_list = {
            1: "BBC",
            2: "CNN",
            3: "Discovery",
            4: "National Geographic",
            5: "HBO",
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


# =======================
# TV AI BOT
# =======================

class TVAIBOT:
    def __init__(self, client: AzureOpenAI):
        self.client = client
        self.pending_action = None

        self.system_prompt = """
You are a TV control assistant.

You must convert user requests into TV actions.

Available actions:
- turn_on
- turn_off
- set_volume (0–100)
- set_brightness (0–100)
- change_channel (1–5)
- show_channels
- get_status

Channels:
1=BBC, 2=CNN, 3=Discovery, 4=National Geographic, 5=HBO

RULES:
- If required info is missing, ask for it.
- Do NOT guess values.
- Respond ONLY with valid JSON.
- No extra text.

RESPONSE FORMATS:

{"action": "turn_on"}
{"action": "set_volume", "value": 30}
{"action": "change_channel", "value": 5}
{"ask": "question to ask the user"}
{"error": "error message"}

Examples:

User: "I want to change channel"
Response:
{"ask": "Which channel? 1-BBC, 2-CNN, 3-Discovery, 4-National Geographic, 5-HBO"}

User: "Set volume"
Response:
{"ask": "What volume level (0–100)?"}
"""

    def process(self, user_input: str) -> dict:
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input},
            ],
            temperature=0,
        )

        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"error": "AI returned invalid JSON."}


# =======================
# EXECUTION LAYER
# =======================

def execute_action(tv: Television, result: dict) -> str:
    if "ask" in result:
        return result["ask"]

    if "error" in result:
        return result["error"]

    action = result.get("action")

    if action == "turn_on":
        return tv.turn_on()
    if action == "turn_off":
        return tv.turn_off()
    if action == "set_volume":
        return tv.set_volume(result["value"])
    if action == "set_brightness":
        return tv.set_brightness(result["value"])
    if action == "change_channel":
        return tv.change_channel(result["value"])
    if action == "show_channels":
        return tv.show_channels()
    if action == "get_status":
        return tv.get_status()

    return "Unknown action."


# =======================
# MAIN LOOP
# =======================

tv = Television()
bot = TVAIBOT(client)

print("🤖 TV AI ready. Talk to it like a normal person. Type 'exit' to quit.")

while True:
    user_input = input("\nYou: ")

    if user_input.lower() in {"exit", "quit"}:
        print("AI: Powering down. Bye 👋")
        break

    ai_result = bot.process(user_input)
    response = execute_action(tv, ai_result)
    print("----------------------------------")
    print("Current TV Status:")
    print(tv.get_status())
    print("-----------------------------------")
    print("\n") 
    print(f"AI: {response}")
