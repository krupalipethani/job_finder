import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def ask_groq(prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # ✅ safe and working model
        messages=[
            {
                "role": "system",
                "content": "You are a job finder assistant for Surat city. Give short, useful job suggestions."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content