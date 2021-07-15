import gensim
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

import matplotlib.pyplot as plt

import dskc

def _compute_coherence_values(dictionary, corpus, texts, limit,id2word, start=2, step=3):
    """
    Compute c_v coherence for various number of topics

    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    limit : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    
    mallet_path = "{}\\dskc\\clean\\topic_modeling\\mallet-2.0.8".format(dskc.get_root_path())
    
    coherence_values = []
    model_list = []
    
    for num_topics in range(start, limit, step):
        model = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics=num_topics, id2word=id2word)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values

def _graph(coherence_values,x):
    from dskc import dskc_terminal
    
    # table 
    table = [["Num Topics","Coherence"]]
    # Print the coherence scores
    for m, cv in zip(x, coherence_values):
        table.append([m, round(cv, 2)])
                      
    dskc_terminal.markdown_table(table)
    
    # graph
    plt.plot(x, coherence_values)
    
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score")
    
    plt.ylim(0, 1) 
    
    plt.show()
    

def search_model(lda_model,corpus,data_words,id2word):
    limit=20
    start=2
    step=1
    x = range(start, limit, step)
    
    # Can take a long time to run.
    model_list, coherence_values = _compute_coherence_values(dictionary=id2word, 
                                                            corpus=corpus, 
                                                            texts=data_words,
                                                            id2word=id2word, 
                                                            start=start, 
                                                            limit=limit, 
                                                            step=step)
    
    _graph(coherence_values,x)
    
    
                      
                      
        
    