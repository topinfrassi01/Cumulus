from textblob import TextBlob


class TextBlobExtractor:
    @staticmethod
    def fix(np):
        if not str.isalpha(np[-1]):
            np = str.strip(np[:-1])

        return np

    @staticmethod
    def extract_noun_phrases(text):
        blob = TextBlob(text)

        noun_phrases = set([np for np in blob.noun_phrases if len(np) > 4 and not np.count(" ") > 3])

        noun_phrases = map(TextBlobExtractor.fix, noun_phrases)

        return list(noun_phrases)

