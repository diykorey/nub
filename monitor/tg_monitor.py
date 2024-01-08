import getopt
import sys

from telethon import TelegramClient, events

from archive import Archive
from channels_profile import Profile
from message import Message


class Monitor:

    def __init__(self, api_id, api_hash, tg_client_owner):
        self.api_id = api_id
        self.api_hash = api_hash
        self.archive = Archive(24, True)
        self.tg_client_owner = tg_client_owner

    def start_listener(self, tg_client: TelegramClient, source_channel: str, recipient: str):
        channel = f'https://t.me/{source_channel}'

        @tg_client.on(events.NewMessage(chats=channel))
        async def message_listener(event: events.NewMessage):
            # collect messages and analyze
            # combine message and define priority when to write message
            # write combined message to shared chat
            # write combined message to registered users if requested

            await self.process_message(tg_client, event.message, recipient)

    async def process_message(self, tg_client: TelegramClient, tg_message, recipient: str):
        content = tg_message.message
        source = tg_message.chat.title
        date = tg_message.date
        if not content or not content.strip():
            return

        message = Message(content, source, date)
        if self.archive.contains_similar_message(message):
            return

        self.archive.store(message)

        await tg_client.forward_messages(recipient, tg_message)

    async def start_tg_client(self, profile: Profile):
        tg_client: TelegramClient = TelegramClient(profile.session_name, self.api_id, self.api_hash)
        await tg_client.start(phone=self.tg_client_owner)
        try:
            # Start the listener
            for source_channel in profile.source_channels:
                print(f"Starting the listener {source_channel}")
                self.start_listener(tg_client, source_channel, profile.message_recipient)
            async with tg_client:
                await tg_client.run_until_disconnected()
        except getopt.GetoptError:
            sys.exit(1)
