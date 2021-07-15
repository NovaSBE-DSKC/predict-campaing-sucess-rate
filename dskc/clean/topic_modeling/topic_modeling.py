"""
strongly based on  https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/
"""

import numpy as np
import pandas as pd
import re

import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

import pyLDAvis
import pyLDAvis.gensim  # don't skip this

# my imports
import dskc
from . import data_preparation
from .search_model import search_model
from . import io

def _metrics(lda_model,corpus,id2word,data_words):
   
    # Compute Coherence Score
    coherence_model_lda = CoherenceModel(model=lda_model, texts=data_words, dictionary=id2word, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    
    print('Perplexity: ', lda_model.log_perplexity(corpus))  # a measure of how good the model is. lower the better.
    print('Coherence Score: ', coherence_lda)

def _get_baseline_model(corpus, id2word,n_topics):
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=n_topics, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)
    
    return lda_model

def _visualization(lda_model, corpus, id2word):
    vis_data = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
    return pyLDAvis.display(vis_data)
  
def apply_lda(n_topics,lda_model,corpus):
    # Init output
    dominant_topics=[]
    prob_dominant_topics=[]
    topics_prob={x:[] for x in range(n_topics)}

    # Get main topic in each document
    # for each sample
    
    for i, row in enumerate(lda_model[corpus]):
        row = sorted(row[0], key=lambda x: (x[1]), reverse=True)

        topics_score = {x[0]:x[1] for x in row}    

        dominant_topic = row[0][0]
        prop_topic = row[0][1]

        dominant_topics.append(dominant_topic)
        prob_dominant_topics.append(prop_topic)

        row_topics_prob = {x[0]:x[1] for x in row}
        for topic,prob in row:
            row_topics_prob[topic]=prob

        for x in range(n_topics):
            if x in row_topics_prob:
                value=row_topics_prob[x]
            else:
                value=0

            topics_prob[x].append(value)
            
    return dominant_topics, prob_dominant_topics, topics_prob

def _modify_df(df,column,n_topics,lda_model,corpus,dominant_topic=True,topics_proba=True):

    dominant_topics,prob_dominant_topics,topics_prob= apply_lda(n_topics,lda_model,corpus)
    
    idx_col=0
    for col in enumerate(df.columns):
        if col==column:
            idx_col=i
            break


    if dominant_topic:
        df.insert(idx_col+1,column+"_dominant_topic",dominant_topics)
        df.insert(idx_col+1,column+"_prob_dominant_topic",prob_dominant_topics)

    if topics_proba:
        for x in reversed(range(n_topics)):
            df.insert(idx_col,"{}_topic_{}".format(column,x+1),topics_prob[x])

    
        
    
    
def topic_modeling(df,
                   column, 
                   n_components=3,
                   modify=True, 
                   visualize=True, 
                   search=False, 
                   stop_words=[],
                   force_train=False,
                   path=None, 
                   save=True,
                   dominant_topic=True, 
                   topics_proba=True):
    # Convert to list
    series = df[column].fillna("").values.tolist()

    # prepare data
    data, data_words, id2word, corpus = data_preparation.prepare_data(series,stop_words)

    lda_model = None
    if path and not force_train:
        lda_model = io.load_model(path)
        
    if lda_model is None:
        lda_model = _get_baseline_model(corpus, id2word, n_components)
        
    if save and path:
        io.save_model(lda_model, path)

    #_metrics(lda_model,corpus,id2word,data_words)
    
    if search:
        search_model(lda_model,corpus,data_words,id2word)
       
    if modify:
        _modify_df(df, column,n_components,lda_model,corpus,dominant_topic,topics_proba)
    
    if visualize:
        return _visualization(lda_model,corpus,id2word)
    
def topic_modeling_transform(data,
                    lda_model,
                    n_topics=6,#extract from model
                    stop_words=[]):
    data, data_words, id2word, corpus = data_preparation.prepare_data(data,stop_words)
    dominant_topics,prob_dominant_topics,topics_prob = apply_lda(n_topics,lda_model,corpus)
    return dominant_topics,prob_dominant_topics,topics_prob
    
    