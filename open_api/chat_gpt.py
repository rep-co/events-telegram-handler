import os
import openai
from openai.types.chat import ChatCompletion


async def chat_gpt_request(content: str) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = await ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": content}])
    return response.choices[0].message.content
