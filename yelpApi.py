
import requests
import json
import pandas as pd
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager



def Getinfo(key,parameters):
    base_url = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization':'Bearer %s' % key}
    response = requests.get(base_url,headers=headers,params=parameters)
    data = response.json()['businesses']
    r_id = []
    names = []
    category = []
    ratings = []
    pricing = []
    cnt = []
    address = []
    url = []
    for r in data:
        r_id.append(r['id'])
        names.append(r['name'])
        ratings.append(r['rating'])
        address.append(r['location']['display_address'][0])
        try:
            temp = []
            for i in r['categories']:
                temp.append(i['title'])
            category.append(temp)
        except:
            category.append(None)
        try:
            pricing.append(len(r['price']))
        except:
            pricing.append(None)
        cnt.append(r['review_count'])
        url.append(r['url'])
    biz = {'id':r_id, 'name':names, 'rating':ratings, 'category':category, 
           'pricing': pricing,'num_reviews':cnt, 'street address':address, 
           'reviews':[],'city':'','url':url}
    display={'Name':names, 'Rating':ratings, 'Category':category, 
           'Pricing': pricing, 'Street Address':address}
    return biz,display


def GetReview(key,df):
    review=[]
    headers = {'Authorization':'Bearer %s' % key}
    for business_id in df['id']:
        temp = []
        review_url = f'https://api.yelp.com/v3/businesses/{business_id}/reviews'
        review_json = requests.get(review_url,headers=headers)
        data = review_json.json()
        try:
            for i in data['reviews']:
                temp.append(i['text'])
        except:
            temp=['Null']
        review.append(temp)
    return review


#cache all the info 
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



def main(user_key,user_location):
    key = user_key
    info = []
    i = 0
    for j in range(0,1000,50):
        city = user_location
        parameters = {'term' : 'restaurants','location' : f"{city}",
                      'limit':50,'offset':j}
        df,display = Getinfo(key,parameters)
        review = GetReview(key,df)
        df['reviews'] = review
        df['city'] = city
        i+=1
        print(i)
        info.append(df)
    save_cache(info)
    print('File was saved into json format, filename is "cacheRestaurants_info.json".')


# In[ ]:




