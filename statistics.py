from message import Message


class Statistics:
    def __init__(self):
        self.dictionary = {}

    def add(self, origin: Message, duplicate: Message):
        record = Record(origin, duplicate)
        origin_chat_stats = self.dictionary.get(origin.source)
        if origin_chat_stats is None:
            origin_chat_stats = ChatStats(origin.source)
            self.dictionary[origin.source] = origin_chat_stats
        origin_chat_stats.add_origin(record)

        duplicate_chat_stats = self.dictionary.get(duplicate.source)
        if duplicate_chat_stats is None:
            duplicate_chat_stats = ChatStats(duplicate.source)
            self.dictionary[duplicate.source] = duplicate_chat_stats

        duplicate_chat_stats.add_duplicate(record)

    def __str__(self):
        return str(self.dictionary)


class ChatStats:
    def __init__(self, name: str):
        self.name = name
        self.origins = {}
        self.duplicates = []

    def add_duplicate(self, record: "Record"):
        self.duplicates.append(record)

    def add_origin(self, record: "Record"):
        origin = self.origins.get(record.origin_msg_id)
        if origin is None:
            self.origins[record.origin_msg_id] = record
            return
        origin.duplicates.extend(record.duplicates)

    def __str__(self):
        return f'\n Channel - {self.name} \n     Origins\n        {self.origins} \n     Duplicates\n        {self.duplicates}'

    def __repr__(self):
        return f'\n Channel - {self.name} \n     Origins\n        {self.origins} \n     Duplicates\n        {self.duplicates}'


class Record:

    def __init__(self, origin: Message, duplicate: Message):
        self.origin_msg_id = origin.id
        self.origin_channel_name = origin.source
        self.origin_date = origin.date

        self.recent_duplicate = {"duplicate_channel_name": duplicate.source, "duplicate_msg_id": duplicate.id,
                                 "duplicate_date": duplicate.date}

        self.duplicates = [self.recent_duplicate]

    def __str__(self):
        return f'Origin at {self.origin_date} from {self.origin_channel_name} -> Duplicated {self.recent_duplicate}\n'

    def __repr__(self):
        return f'Origin at {self.origin_date} from {self.origin_channel_name} -> Duplicated {self.recent_duplicate}\n'
