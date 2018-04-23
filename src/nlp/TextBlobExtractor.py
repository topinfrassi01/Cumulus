from textblob import Blobber
from textblob.np_extractors import ConllExtractor


class TextBlobExtractor:
    def __init__(self):
        self.blob_factory = Blobber(np_extractor=ConllExtractor(), analyzer=None)

    def fix(self,np):
        return np.replace("'s", "").replace("\"", "").strip()

    def extract_noun_phrases(self,text):

        blob = self.blob_factory(text)

        # For sake of brievity, I kept only phrases with less than 3 words.
        noun_phrases = set([np.strip() for np in blob.noun_phrases if len(np) > 4 and not np.count(" ") > 3])

        # Removing all special characters.
        noun_phrases = filter(lambda np: all(x.isalnum() or x.isspace() for x in np), noun_phrases)

        return list(noun_phrases)

