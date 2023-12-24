import json
import asyncio

from python_bot.Models.Event import Event
from python_bot.chat_gpt.chat_gpt import chat_gpt_request
from python_bot.chat_gpt.generate_prompt import generate_prompt
from python_bot.links_api.get_links import get_links
from telegram_api.get_new_events import get_new_events
from datetime import datetime

# придумать откуда брать lastUpdate
lastUpdate = None


async def main():
    all_messages = []
    all_events = []
    links = get_links()
    for link in links:
        messages = await get_new_events(link=link, lastUpdate=lastUpdate)

        for message in messages:
            if len(message) == 0:
                continue

            promt = generate_prompt(message)
            reply = await chat_gpt_request(promt)
            j = json.loads(reply)
            event = Event(**j)
            all_events.append(event)
            all_messages.append(reply)

    with open('channel_messages.json', 'w') as outfile:
        json.dump(all_messages, outfile)
        print(all_events)


if __name__ == '__main__':
    asyncio.run(main())
