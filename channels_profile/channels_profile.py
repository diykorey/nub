class Profile:
    def __init__(self, name, message_recipient, source_channels=None):
        self.name = name
        self.message_recipient = message_recipient
        self.source_channels = source_channels is None if [] else source_channels
        self.session_name = f"{name}_session"

    def add_channel(self, channel_name):
        self.source_channels.append(channel_name)
