# -*- coding: utf-8 -*-
"""LDA_topic.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XJTyoi2IxiblGw-PlD4pgjJyHNQk2cD3

Referenced https://github.com/kapadias/mediumposts/blob/master/natural_language_processing/topic_modeling/notebooks/Introduction%20to%20Topic%20Modeling.ipynb

Load Data
"""

from google.colab import files
uploaded = files.upload()

import io
import pandas as pd
papers = pd.read_csv(io.BytesIO(uploaded['abstract_title.csv']), sep = "DELIMITER")
# Dataset is now stored in a Pandas Dataframe

papers.head()

"""Preprocess"""

# use regular expression library to process data
import re

# Remove punctuation
papers['abstract'] = papers['abstract'].apply(str)
papers['abstract_processed'] = papers['abstract'].map(lambda x: re.sub('[,\.!?]', '', x))

papers['abstract_processed'] = papers['abstract_processed'].map(lambda x: re.sub('services', 'service', x))

# Convert the abstracts to lowercase
papers['abstract_processed'] = \
papers['abstract_processed'].map(lambda x: x.lower())

# Print out the first rows of papers
papers['abstract_processed'].head()

"""Explore Data"""

# Import the wordcloud library
from wordcloud import WordCloud

# Join the different processed titles together.
long_string = ','.join(list(papers['abstract_processed'].values))

# Create a WordCloud object
wordcloud = WordCloud(background_color="white", max_words=1000, contour_width=3, contour_color='steelblue')

# Generate a word cloud
wordcloud.generate(long_string)

# Visualize the word cloud
wordcloud.to_image()

"""More Processing - tokenize and remove stopwords"""

import gensim
from gensim.utils import simple_preprocess
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

def sent_to_words(sentences):
    for sentence in sentences:
        # deacc=True removes punctuations
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) 
             if word not in stop_words] for doc in texts]

data = papers.abstract_processed.values.tolist()
data_words = list(sent_to_words(data))

# remove stop words
data_words = remove_stopwords(data_words)

print(data_words[:1][0][:30])

"""Create Dictionary and Corpus"""

import gensim.corpora as corpora

map = {}

# Create Dictionary
id2word = corpora.Dictionary(data_words)

# Create Corpus
texts = data_words

# Term Document Frequency

corpus = [id2word.doc2bow(text) for text in texts]

# View
print(corpus[:1][0][:30])

"""Train LDA Model"""

from pprint import pprint

# number of topics
num_topics = 10

# Build LDA model
lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                       id2word=id2word,
                                       num_topics=num_topics)

# Print the Keyword in the 10 topics
pprint(lda_model.print_topics())
doc_lda = lda_model[corpus]

def predict_class(num):
  tuple_in_array = lda_model[corpus[num]] 
  #print(tuple_in_array)
  max = 0.0
  pred_class = 0

  for x in tuple_in_array:
    pot_class = x[0]
    percentage = x[1]

    if percentage > max:
      max = percentage
      pred_class = pot_class

  return pred_class


# print the topic probability distribution for the 0th and 2999th abstracts 
print(lda_model.get_document_topics(corpus[0]))
print(lda_model.get_document_topics(corpus[2999]))
print("here it comes")

print(predict_class(2999))

print(papers.shape)

"""Save Classifications to Local File"""

# Commented out IPython magic to ensure Python compatibility.
from google.colab import drive 
drive.mount('/content/drive')
# %cd /content/drive/My\ Drive/

import os
cwd = os.getcwd()
print(cwd)

f = open("testfile.txt", "a")
f.write("March 21 is working")
f.close()

print(cwd)

print(papers['title'][1])

"""Save Classifications to file in my Google Drive """

import json
paperNum = 4029
f = open("lda_topic_distribution_8.txt", "a")


for i in range(paperNum):   # paperNum
    tuple_in_array = lda_model[corpus[i]] 
    data = {}
    data['title'] = papers['title'][i]
    for tuple in tuple_in_array:
      data[str(tuple[0])] = tuple[1]
    pred_class = predict_class(i)
    data['predicted class'] = pred_class
    data_json = json.dumps(str(data))
    f.write(data_json)
    #print(tuple_in_array)
    pure_tuple = tuple_in_array[0]
    #print(pure_tuple)
    #pred_class = predict_class(i)
    #f.write(str(papers['title'][i]) + "DELIMITER"+ str(pred_class) + "\n")

f.close()
print("done")

"""I save the trained model and show how to easily load the model """

from gensim.test.utils import datapath

#save trained model
temp_file =  datapath("model")
lda_model.save(temp_file)

#load the already trained model
lda = gensim.models.LdaModel.load(temp_file)
pprint(lda.print_topics())