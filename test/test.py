import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv(
    "GROQ_API_KEY"
)

if not API_KEY:
    raise ValueError(
      "Missing GROQ_API_KEY"
    )

client = Groq(
    api_key=API_KEY
)
#  strong verstile model for agent (llama-3.3-70b-versatile)
#  cheap intern model (llama-3.1-8b-instant)

while(1):
    a=input("enter prompt...")
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        
        messages=[
            {
                "role":"user",
                "content":a
            }
        ]
    )

    print(
     response.choices[0]
     .message.content
    )
