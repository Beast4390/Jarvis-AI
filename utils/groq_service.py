import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_ai_response(messages):

    try:

        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",

            messages=[
                {
                    "role": "system",
                    "content": "You are Jarvis AI, a helpful and friendly AI assistant."
                }
            ] + messages

        )

        return completion.choices[0].message.content

    except Exception as e:

        return str(e)