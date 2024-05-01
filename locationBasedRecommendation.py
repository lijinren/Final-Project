#!/usr/bin/env python
# coding: utf-8

# In[4]:


from ast import literal_eval
from IPython.display import display
import nltk


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

import pandas as pd

import networkx as nx
import matplotlib.pyplot as plt
# download nltk packages
nltk.download('all')

# Convert strings to python list and dirty data to pandas NA
def convert_to_list(x):
    try:
        return literal_eval(x)
    except ValueError:
        return pd.NA

def process_sentences(text):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    temp_sent =[]

    # Tokenize words
    words = nltk.word_tokenize(text)

    # Lemmatize each of the words based on their position in the sentence
    tags = nltk.pos_tag(words)
    for i, word in enumerate(words):
        if tags[i][1] in ('VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'):  # only verbs
            lemmatized = lemmatizer.lemmatize(word, 'v')
        else:
            lemmatized = lemmatizer.lemmatize(word)
        
        # Remove stop words and non alphabet tokens
        if lemmatized not in stop_words and lemmatized.isalpha(): 
            temp_sent.append(lemmatized)

    # Some other clean-up
    full_sentence = ' '.join(temp_sent)
    full_sentence = full_sentence.replace("n't", " not")
    full_sentence = full_sentence.replace("'m", " am")
    full_sentence = full_sentence.replace("'s", " is")
    full_sentence = full_sentence.replace("'re", " are")
    full_sentence = full_sentence.replace("'ll", " will")
    full_sentence = full_sentence.replace("'ve", " have")
    full_sentence = full_sentence.replace("'d", " would")
    return full_sentence




def cleanData():
    df = pd.read_csv('results_info.csv')
    #print('The dataset has %s rows and %s columns' % df.shape)
    # Drop unnecessary columns
    df.drop(columns=['id','num_reviews'], inplace=True)
    # Rename columns for better convention
    df.rename(columns={'pricing': 'price','category': 'style'}, inplace=True)
    #display('Missing values', df.stb.missing())
    df['reviews'].replace("['Null']", pd.NA, inplace=True)
    #print("Before drop: %s" % df.shape[0])
    df.dropna(inplace=True)
    #print("After drop: %s" % df.shape[0])
    df['reviews'] = df['reviews'].str.lower()
    df['style'] = df['style'].str.lower()
    df['city'] = df['city'].str.lower()

    #display('Dataset after converting to lower case', df.head())

    # Convert strings to python list
    df['style'] = df['style'].apply(lambda x: literal_eval(x))

    # Join the list items together
    df['style'] = df['style'].apply(lambda x: ', '.join(x))

    df['reviews'] = df['reviews'].apply(convert_to_list)

    #print("Before drop: %s" % df.shape[0])
    df.dropna(inplace=True)
    #print("After drop: %s" % df.shape[0])
    # Join the list items together, notice that we only send first item 
    # of list (reviews) to the function and ignore the second (dates)
    df['reviews'] = df['reviews'].apply(lambda x: ', '.join(x))

    df['price'].unique()

    df['price'].replace([1.0, 2.0, 3.0, 4.0, 5.0], ['cheap-eats', 'mid-range','mid-range', 'fine-dining','fine-dining'], inplace=True)

    #print("Before drop: %s" % df.shape[0])
    df = df.drop_duplicates(subset=['name'])
    #print("After drop: %s" % df.shape[0])

    #print('Number of cities: %s ' % df['city'].nunique())
    cities_list = df['city'].unique()
    #print(cities_list)

    
    df['reviews_processed'] = df['reviews'].apply(process_sentences)
    df['style_processed'] = df['style'].apply(process_sentences)

    df['bag_of_words'] = df['style_processed'] + ' ' + df['reviews_processed']


    df.to_csv('results_processed.csv')
    print("The processed data was save into cvs file named 'results_processed.csv'")
    return df,cities_list




def recommend(description):
    df,cities_list = cleanData()
    price_map = {
        'cheap-eats': ('cheap', 'inexpensive', 'low-price', 'low-cost', 'economical','economic', 'affordable'),
        'mid-range': ('moderate', 'fair', 'mid-price', 'reasonable', 'average'),
        'fine-dining': ('expensive', 'fancy', 'lavish')
        }
    # Convert user input to lowercase
    description = description.lower()

    data = df.copy()

    # Extract cities
    cities_input = []
    for city in cities_list:
        if city in description:
            cities_input.append(city)
            description = description.replace(city, "")

    if cities_input:
        data = data[data['city'].isin(cities_input)]

    # Extract price class
    for key, value in price_map.items():
        if any(v in description for v in value):
            data = data[data['price'] == key]
            break
    
    # Process user description text input 
    description = process_sentences(description)
    description = description.strip()
    print('Processed user feedback:', description)

    # Init a TF-IDF vectorizer
    tfidfvec = TfidfVectorizer()

    # Fit data on processed reviews
    vec = tfidfvec.fit(data["bag_of_words"])
    features = vec.transform(data["bag_of_words"])

    # Transform user input data based on fitted model
    description_vector =  vec.transform([description])

    # Calculate cosine similarities between restaurants
    cos_sim = linear_kernel(description_vector, features)

    # Add similarities to data frame
    data['similarity'] = cos_sim[0]

    # Sort data frame by similarities
    data.sort_values(by='similarity', ascending=False, inplace=True)

    return data[['name', 'city', 'price', 'style', 'reviews', 'similarity']]


# In[ ]:




