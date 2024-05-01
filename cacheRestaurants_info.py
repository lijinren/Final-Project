#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
import json
import pandas as pd
from IPython.display import display

CACHE_FILENAME = "cacheRestaurants_info.json"

def open_cache():
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()



def main():
    local_cache = open_cache()
    data1 = local_cache
    for i in range(20):
        data1[i]['city'] = []
    for i in range(20):
        j = 0
        while j < 50 :
            data1[i]['city'].append('New York City')
            j += 1
    ids = []
    name = []
    rating = []
    category = []
    pricing = []
    num_reviews = []
    street_address = []
    reviews = []
    city = [] 
    url = []
    for i in data1:
        ids += i['id']
        print(len(ids))
        name += i['name']
        rating += i['rating']
        category += i['category']
        pricing += i['pricing']
        num_reviews += i['num_reviews']
        street_address += i['street address']
        reviews += i['reviews']
        city += i['city']
        url += i['url']
    df = {'id':ids, 'name':name, 'rating':rating, 'category':category, 
          'pricing': pricing,'num_reviews':num_reviews, 'street address':street_address, 
          'reviews':reviews,'city':city,'url':url}
    results = pd.DataFrame(df)
    display(results)
    results.to_csv('results_info.csv')
    print("The basic information about the restaurants was cached in to csv format named 'results_info.csv'")


main()
"""


# In[4]:


import json
import pandas as pd
from IPython.display import display

CACHE_FILENAME = "cacheRestaurants_info.json"

def open_cache():
    """Loads cached content from a JSON file."""
    try:
        with open(CACHE_FILENAME, 'r') as cache_file:
            cache_dict = json.load(cache_file)
    except FileNotFoundError:
        print(f"File '{CACHE_FILENAME}' not found. Loading with an empty cache.")
        cache_dict = {}
    except Exception as e:
        print(f"Error loading cache: {e}")
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    """Saves content to a JSON file."""
    try:
        with open(CACHE_FILENAME, "w") as fw:
            fw.write(json.dumps(cache_dict))
    except Exception as e:
        print(f"Error saving cache: {e}")

def main():
    local_cache = open_cache()
    data1 = local_cache

    if not isinstance(data1, dict):
        print("Cache content is not a valid dictionary.")
        return

    # Ensure all necessary keys exist
    for i in range(20):
        if i not in data1:
            data1[i] = {}
        if "city" not in data1[i]:
            data1[i]['city'] = []

        for _ in range(50):
            data1[i]['city'].append("New York City")

    # Lists to store data for the dataframe
    ids, name, rating, category, pricing, num_reviews, street_address, reviews, city, url = [], [], [], [], [], [], [], [], [], []

    # Populate lists with data from data1
    for key in data1:
        item = data1[key]
        
        try:
            ids += item.get('id', [])
            name += item.get('name', [])
            rating += item.get('rating', [])
            category += item.get('category', [])
            pricing += item.get('pricing', [])
            num_reviews += item.get('num_reviews', [])
            street_address += item.get('street address', [])
            reviews += item.get('reviews', [])
            city += item.get('city', [])
            url += item.get('url', [])
        except KeyError as e:
            print(f"Missing key {str(e)} in item {key}")
            continue

    # Check if all lists have the same length before creating the dataframe
    lengths = [len(lst) for lst in [ids, name, rating, category, pricing, num_reviews, street_address, reviews, city, url]]
    
    if len(set(lengths)) > 1:
        print("Data lists have uneven lengths, unable to create a dataframe.")
        print(f"Lengths: {lengths}")
        return

    # Create and display the dataframe
    df = {'id': ids, 'name': name, 'rating': rating, 'category': category, 'pricing': pricing,
          'num_reviews': num_reviews, 'street address': street_address, 'reviews': reviews, 'city': city, 'url': url}
    
    results = pd.DataFrame(df)
    display(results)
    results.to_csv('results_info.csv')
    print("The basic information about the restaurants has been cached into CSV format as 'results_info.csv'.")

if __name__ == "__main__":
    main()


# In[ ]:




