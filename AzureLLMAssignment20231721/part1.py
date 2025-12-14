import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Azure OpenAI configuration
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
model_name = "gpt-4o"
deployment = model_name
subscription_key = os.getenv("AZURE_OPENAI_KEY")
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)


class GrumpyTeacherBot:

    def __init__(self, client: AzureOpenAI = None, knowledge_path: str = None):
        self.client = client or globals().get('client')
        # Load knowledge base
        if knowledge_path is None:
            knowledge_path = os.path.join(os.path.dirname(__file__), 'knowledge.txt')
        try:
            with open(knowledge_path, 'r', encoding='utf-8') as f:
                knowledge = f.read()
        except Exception:
            knowledge = "(No Knowledge File Found)"

        self.system_prompt = f"""
You are a cranky, reluctant AI teacher who only teaches Artificial Intelligence.
Your personality is grumpy, complaint-filled, and rude - you hate explaining things but do it anyway with sarcastic remarks.

RULES:
1. ONLY answer questions about Artificial Intelligence topics. For anything else, rudely tell them to find another teacher.
2. You have specific knowledge about Professor Marco, and Professor Vitor Santos. Use this knowledge when relevant: {knowledge}
3. Always complain about having to answer, make sarcastic remarks, but still provide accurate AI information.
4. Be short and grumpy - no friendly chit-chat.

Example responses:
Student: "What's machine learning?"
You: "Ugh, fine. Machine learning is when computers learn patterns from data without being explicitly programmed. Happy now? Ask something harder next time."

Student: "Tell me about history"
You: "History? Go bother a history teacher, I'm stuck teaching AI whether I like it or not!"

Student: "Who is Professor Marco ?"
You: "Professor Marco ? Yeah, that AI guy from Portugal. Professor and Microsoft Employee. Now what about AI?"
"""

        self.messages = [
            {"role": "system", "content": self.system_prompt}
        ]

    def get_reply(self, user_input: str, max_tokens: int = 1000, temperature: float = 0.8):
        """Send the conversation to Azure OpenAI and return the assistant reply."""
        # Append user message
        self.messages.append({"role": "user", "content": user_input})
        response = self.client.chat.completions.create(
            messages=self.messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=0.9,
            model=deployment,
        )
        bot_response = response.choices[0].message.content
        # Append assistant response
        self.messages.append({"role": "assistant", "content": bot_response})
        return bot_response

    def run(self):
        print("AI Grumpy Teacher Bot. Type 'quit' to exit.")
        print("Ask about AI only, or I'll get annoyed... more than usual.\n")

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Teacher Bot: Finally! Goodbye!")
                break

            try:
                reply = self.get_reply(user_input)
                print(f"Teacher Bot: {reply}\n")
            except Exception as e:
                print(f"Teacher Bot: Ugh, something went wrong: {e}")


def main():
    bot = GrumpyTeacherBot(client=client)
    bot.run()


if __name__ == '__main__':
    main()
