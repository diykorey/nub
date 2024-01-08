from channels_profile import Profile

message_recipient = 'world_news_a'
source_channels = {
    #'CNN_English_News',
    'bloomberg',
    'bbc_nws',
    'France24_en',
    'Kyivpost_official',
    'guardian',
    'washingtonpost',
    'nytimes',
    'associated_press_news',
    'wall_street_journal_news',
    'ReutersWorldChannel'
}

instance = Profile('world_news_en', message_recipient, source_channels)
