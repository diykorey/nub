from analyzer import jaccard_similarity
import ulid


class Message:
    def __init__(self, content: str, source: str, date) -> None:
        self.content = content
        self.source = source
        self.date = date
        self.id = ulid.new()

    def similar(self, message: "Message"):
        return jaccard_similarity(self.content, message.content) > 0.2

    def __str__(self) -> str:
        return f'Message from {self.source} at {self.date} with content {self.content}'

    def __repr__(self) -> str:
        return self.content
