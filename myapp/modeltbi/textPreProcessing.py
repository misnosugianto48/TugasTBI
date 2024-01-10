# Regular expression operations: https://docs.python.org/3/library/re.html
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet as wn

class TextPreProcessing:
    def __init__(self):
        # Ensure that resources are downloaded
        self.download_stopwords()

    def download_stopwords(self):
        try:
            # Try to download stopwords
            stopwords.words('english')
        except LookupError:
            # If LookupError occurs, download the resource
            nltk.download('stopwords')

        # Download 'punkt' resource
        try:
            word_tokenize("Test sentence")
        except LookupError:
            nltk.download('punkt')

        # Download 'wordnet' resource
        try:
            wn.synsets('test')
        except LookupError:
            nltk.download('wordnet')

    def textprocessing(self, data):
        ps = PorterStemmer()
        stop_words = set(stopwords.words('english'))
        corpus = []
        index = 0
        for jurnal in data:
            # print(jurnal.title, jurnal.abstract, jurnal.link, jurnal.abstracturl)
            review = re.sub('[^a-zA-Z]', ' ', jurnal.title)  # Changed from '' to ' '
            review = review.lower()
            tokens = word_tokenize(review)

            filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

            # Apply stemming to individual words
            stemmed_tokens = [ps.stem(word) for word in filtered_tokens]

            # Join the stemmed tokens back into a string
            stemmed_text = ' '.join(stemmed_tokens)
            index = index+1
            linkjurnal = jurnal.abstracturl
            abstrak = jurnal.abstract
            # Append the preprocessed text to the corpus list
            corpus.append((index,linkjurnal, abstrak, stemmed_text))


        return corpus
