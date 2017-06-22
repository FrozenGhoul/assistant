AFFIRMATIVE = ["YES", "YEAH", "SURE", "YAH", "YA"]
NEGATIVE = ["NO", "NEGATIVE", "NAH", "NA", "NOPE"]

class BaseModule:

    def __init__(self, key_words_assigned, raw_text, sub_words, key_words, inter, cfg):
        self.key_words_assigned = key_words_assigned
        self.raw_text = raw_text
        self.sub_words = sub_words
        self.key_words = key_words
        self.interface = inter
        self.config = cfg