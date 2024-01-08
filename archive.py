from datetime import datetime, timedelta

from message import Message
from statistics import Statistics


class Archive:
    def __init__(self, period_hours: int = 24, stats_enabled: bool = False):
        self.period_hours = timedelta(hours=period_hours)
        self.storage = {}
        self.statistics = Statistics()
        self.stats_enabled = stats_enabled

    def store(self, message: Message):
        records = self.storage.get(message.source)
        if records is None:
            records = []
            self.storage[message.source] = records
        records.append(message)

    def contains_similar_message(self, message: Message):
        self.cleanup()
        for source, messages in self.storage.items():

            if source == message.source:
                # skip the same source channel
                continue

            for item in messages.copy():
                if item.similar(message):
                    if self.stats_enabled is True:
                        self.statistics.add(item, message)
                    return True

        return False

    def cleanup(self):
        for messages in self.storage.values():
            for message in messages.copy():
                if message.date.timestamp() < (datetime.now() - self.period_hours).timestamp():
                    messages.remove(message)
