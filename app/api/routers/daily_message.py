import json
from dotenv import load_dotenv
from fastapi import APIRouter
from openai import OpenAI
import os

from app.api.deps import Auth

load_dotenv()

PROJECT_URL = os.environ.get("PROJECT_URL")
OPEN_ROUTER_URL = "https://openrouter.ai/api/v1"
OPEN_ROUTER_API_KEY = os.environ.get("OPEN_ROUTER_API_KEY")


router = APIRouter(prefix="/daily-messages")


@router.post("")
def generate_profile_monthly_messages(auth: Auth):
    # def generate_profile_monthly_messages():
    prompt = """Generate a short message of the day.
        This will be used in an router called
        VIVID - visually intuitive & versatile interactive data strcuture.
        this is an router made to simplify learning dsa and make it fun thru
        the use of automated simulations based on user input. I want you
        to generate motivating & encauraging words to support the user.
        make it short sentence of 5-10 words. generate 50 messages.
        """
    client = OpenAI(
        base_url=OPEN_ROUTER_URL,
        api_key=OPEN_ROUTER_API_KEY,
    )
    referer_url = ""
    if PROJECT_URL:
        referer_url = PROJECT_URL
    completion = client.chat.completions.create(
        extra_headers={"HTTP-Referer": referer_url, "X-Title": "Vivid"},
        extra_body={},
        model="deepseek/deepseek-v3.1-terminus",
        messages=[
            {"role": "user", "content": prompt},
            {
                "role": "assistant",
                "content": """
                   ```
                   [
                       "Datastructures are the building blocks of code.",
                       "Algorithms are the recipes for problem-solving.",
                       "Mastering DSA is mastering problem-solving.",
                    ]
                   ```
                   """,
            },
        ],
    )
    content = completion.choices[0].message.content
    if not content:
        return
    messages = json.loads(content.split("```")[1].strip())
    print(messages)
    return messages
