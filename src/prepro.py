import spacy
import nltk
from bs4 import BeautifulSoup

class Prepro:
    def __init__(self, corpus_file, stopwords_file):
        self.corpus_file = corpus_file
        self.stopwords_file = stopwords_file

    def main(self):
        documents = self.get_paragraphs()
        documents_whithout_stopwords = self.delete_stopwords(documents)
        documents_lemmatized = self.get_lemmatized_words(documents_whithout_stopwords)
        documents_final = self.delete_stopwords(documents_lemmatized)
        vocabulary = self.get_vocabulary(documents_final)

        print(vocabulary)

        return documents_final, vocabulary

    def get_lemmatized_words(self, documents):
        documents_lemmatized = []
        for d in documents:
            nlp = spacy.load('es_core_news_sm')
            doc = nlp(" ".join(d))
            lemmatized_words = [token.lemma_ for token in doc]
            documents_lemmatized.append(lemmatized_words)
        
        return documents_lemmatized

    def get_paragraphs(self):
        clean_words = []
        f = open(self.corpus_file, 'r', encoding='utf-8')
        soup = BeautifulSoup(f.read(), 'html.parser')
        f.close()

        titles = soup.find_all('title')
        results = []

        for i in range(len(titles)):
            start = titles[i]
            end = titles[i+1] if i+1 < len(titles) else None
            paragraph = ""

            for sibling in start.find_all_next():
                if sibling == end:
                    break
                if sibling.name == 'p':
                    paragraph = paragraph + " " + sibling.get_text()
                    
            wordpunkt_wt = nltk.WordPunctTokenizer()
            words = wordpunkt_wt.tokenize(paragraph)

            clean_words = []
            for word in words:
                if word.isalpha():
                    clean_words.append(word)

            results.append(clean_words)

        return results
    
    def delete_stopwords(self, documents):
        f = open(self.stopwords_file, 'r', encoding='utf-8')
        words = f.read()
        stopwords = words.split()
        f.close()

        docuemnts_whitout_stopwords = []
        for d in documents:
            tokens_without_stopwords = []

            for tok in d:
                #if tok not in stopwords:
                if " " not in tok:
                    tokens_without_stopwords.append(tok)

            docuemnts_whitout_stopwords.append(tokens_without_stopwords)

        return  docuemnts_whitout_stopwords
    
    def get_vocabulary(self, documents):
        vocabulary = []

        for d in documents:
            for tok in d:
                if tok not in vocabulary:
                    vocabulary.append(tok)

        return vocabulary
            