import asyncio
import json

from links_api.get_links import get_links
from models.Event import Event
from open_api.chat_gpt import chat_gpt_request
from open_api.generate_prompt import generate_prompt
from telegram_api.get_new_events import get_new_events


async def handler(event, context):
    try:
        all_messages = []
        all_events = []
        links = get_links()

        for link in links:
            messages = await get_new_events(link=link, lastUpdate=None)

            for message in messages:
                if len(message) == 0:
                    continue

                prompt = generate_prompt(message)
                reply = await chat_gpt_request(prompt)
                j = json.loads(reply)
                event = Event(**j)
                all_events.append(event)
                all_messages.append(reply)

        return {
            'statusCode': 200,
            'body': json.dumps(
                all_events,
                default=vars,
            ),
        }

    except Exception:
        return {
            'statusCode': 500,
            'body': "Oooops",
        }


async def main():
    await handler(None, None)


if __name__ == '__main__':
    asyncio.run(main())
