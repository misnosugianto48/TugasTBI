import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class QueryExpansion:
    def __init__(self):
        
        pass
    def get_synonyms(self, word):
        # Mencari sinonim menggunakan WordNet Bahasa Indonesia
        synsets = wn.synsets(word, lang='eng')
        synonyms = set()
        for synset in synsets:
            for lemma in synset.lemmas('eng'):
                synonyms.add(lemma.name())
        return list(synonyms)

    def expand_query(self, query):
        # Tokenisasi query dan menghapus stop words
        stop_words = set(stopwords.words('english'))
        tokens = [word.lower() for word in word_tokenize(query) if word.isalnum() and word.lower() not in stop_words]

        # Mencari sinonim untuk setiap kata dalam query
        expanded_tokens = []
        for token in tokens:
            # Mencari sinonim menggunakan WordNet Bahasa Inggris
            synonyms = self.get_synonyms(token)
            if synonyms:
                expanded_tokens.extend(synonyms)
            else:
                expanded_tokens.append(token)

        # Menghilangkan duplikat    
        expanded_tokens = list(set(expanded_tokens))

        # Menggabungkan hasil ekspansi menjadi string baru
        expanded_query = ' '.join(expanded_tokens)

        return expanded_query
