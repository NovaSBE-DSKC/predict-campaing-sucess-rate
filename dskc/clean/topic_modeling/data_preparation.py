import nltk
import spacy
import gensim
import re

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    nlp = spacy.load('en', disable=['parser', 'ner'])

    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

def _get_stop_words(stop_words):
    from dskc import get_root_path
    
    # read from file
    file ="{}/dskc/clean/stopwords/pt-en.txt".format(get_root_path())
    with open(file, "r") as f:
        stop_words.extend(f.read().splitlines())
    
    # remove accents
    stop_words=[word.encode("ascii","ignore").decode() for word in stop_words]
    
    return stop_words

def _build_bigram_trigram(data_words):
    
    # Build the bigram and trigram models
    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
    trigram = gensim.models.Phrases(bigram[data_words], threshold=100)  

    # Faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)

    return bigram,trigram

def make_bigrams(texts,bigram_mod):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts,trigram_mod):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]


# Define functions for stopwords, bigrams, trigrams and lemmatization
def remove_stopwords(texts,stop_words):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def prepare_data(data,stop_words):
    
    # Remove Emails
    data = [re.sub(r'\S*@\S*\s?', '', sent) for sent in data]

    # Remove new line characters
    data = [re.sub(r'\s+', ' ', sent) for sent in data]

    # Remove distracting single quotes
    data = [re.sub(r"\'", "", sent) for sent in data]

    # to words
    data_words = list(sent_to_words(data))
    
    # Remove Stop Words
    stop_words=_get_stop_words(stop_words)
    data_words = remove_stopwords(data_words,stop_words)
    
    
    # Form Bigrams
    bigram_mod, trigram_mod = _build_bigram_trigram(data_words)
    data_words = make_bigrams(data_words,bigram_mod)
    

    # Initialize spacy ‘en’ model, keeping only tagger component (for efficiency)
    # Run in terminal: python -m spacy download en
    #nlp = spacy.load("en", disable=["parser", "ner"])

    # Do lemmatization keeping only Noun, Adj, Verb, Adverb
    #data_words = lemmatization(data_words, allowed_postags=["NOUN", "VERB"]) #select noun and verb
    
    # Create Dictionary
    id2word = corpora.Dictionary(data_words)

    # Create Corpus
    texts = data_words

    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]
 
    return data,data_words,id2word,corpus
    
   

    