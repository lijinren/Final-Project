#!/usr/bin/env python
# coding: utf-8

# In[25]:


"""
from time import sleep
import pandas as pd
import webbrowser
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
import json
from lxml import html
import requests

"""

"""
def parse_html(html):
    soup = BeautifulSoup(html,'lxml')
    dine_list = []
    resto = soup.find('header', class_='_header_1wadv_1')
    section1stTitle = resto.find('h1',class_='_h1_1wadv_5').text
    dict = {}
    article_list = []
    head_zone = soup.find('div',class_='_zoneItems_ncpe6_1')
    for article in head_zone.find_all('div', class_='_articleContent_1pzwm_26'):
        temp = {}
        temp['name'] = article.find('h3', class_='_h3_cuogz_1').text
        temp['url'] = 'https://www.timeout.com' + article.find('a')['href']
        article_list.append(temp)
    dict[section1stTitle] = article_list
    dine_list.append(dict)
    for resto in soup.find_all('div', class_='zone _zone_abr0c_1'):
        section = resto.find('h2',class_='_h2_1ikgb_1')
        section_title = section.find('span').text
        #print(title)
        dict={}
        article_list=[]
        for i in resto.find_all('div', class_='_zoneItems_1ktxs_1'):
            for article in i.find_all('div', class_='_articleContent_1pzwm_26'):
                temp = {}
                temp['name'] = article.find('h3',class_='_h3_cuogz_1').text
                temp['url'] = 'https://www.' + article.find('a')['href']
                article_list.append(temp)
        dict[section_title] = article_list
        dine_list.append(dict)
        for i in resto.find_all('div', class_=''):
            for article in i.find_all('div', class_='_articleContent_1pzwm_26'):
                temp = {}
                temp['name'] = article.find('h3',class_='_h3_cuogz_1').text
                temp['url'] = 'https://www.' + article.find('a')['href']
                article_list.append(temp)
        dict[section_title] = article_list
        dine_list.append(dict)

    return dine_list

CACHE_FILENAME = "Timeout_articles.json"

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
    driver = webdriver.Chrome(ChromeDriverManager().install())
    url = 'https://www.timeout.com/newyork/food-drink'
    driver.get(url)
    webbrowser.open(url)
    sleep(0)
   
    #response = requests.get(url)
    #data = html.fromstring(response.content)
    print(data)
    
    #page = driver.page_source
    #data = parse_html(page)
    newdata = []
    for i in data:
        if i not in newdata:
            newdata.append(i)
    #del newdata[2]

    
    if len(newdata) > 2:
        del newdata[2]

    save_cache(newdata)  

    dict = open_cache()  
    return dict
    #save_cache(newdata)
    #dict = open_cache()
    #return dict
"""


# In[8]:


from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import json

def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    dine_list = []

    # Parse initial header
    resto = soup.find('header', class_='_header_1wadv_1')
    if resto:
        section1stTitle = resto.find('h1', class_='_h1_1wadv_5').text
        dict = {}
        article_list = []

        # Parse articles in the header section
        head_zone = soup.find('div', class_='_zoneItems_ncpe6_1')
        for article in head_zone.find_all('div', class_='_articleContent_1pzwm_26'):
            temp = {}
            temp['name'] = article.find('h3', class_='_h3_cuogz_1').text
            temp['url'] = 'https://www.timeout.com' + article.find('a')['href']
            article_list.append(temp)

        dict[section1stTitle] = article_list
        dine_list.append(dict)

    # Parse other zones
    for resto in soup.find_all('div', class_='zone _zone_abr0c_1'):
        section = resto.find('h2', class_='_h2_1ikgb_1')
        if section:
            section_title = section.find('span').text
            dict = {}
            article_list = []

            # Parsing zone items
            for i in resto.find_all('div', class_='_zoneItems_1ktxs_1'):
                for article in i.find_all('div', class_='_articleContent_1pzwm_26'):
                    temp = {}
                    temp['name'] = article.find('h3', class_='_h3_cuogz_1').text
                    temp['url'] = 'https://www.timeout.com' + article.find('a')['href']
                    article_list.append(temp)

            dict[section_title] = article_list
            dine_list.append(dict)

    return dine_list

CACHE_FILENAME = "Timeout_articles.json"

def open_cache():
    try:
        with open(CACHE_FILENAME, 'r') as cache_file:
            return json.loads(cache_file.read())
    except:
        return {}

def save_cache(cache_dict):
    with open(CACHE_FILENAME, "w") as fw:
        fw.write(json.dumps(cache_dict))

def scrape_timeout_articles(url):
    # Initialize the driver with a Service object
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Optional headless mode
    options.add_argument("--disable-gpu")  # For stability

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    # Extract and parse page content
    page_source = driver.page_source
    data = parse_html(page_source)

    # Clean up driver
    driver.quit()

    # Ensure unique entries
    newdata = []
    for i in data:
        if i not in newdata:
            newdata.append(i)

    return newdata

def main():
    
    # Usage in a Jupyter Notebook
    url = 'https://www.timeout.com/newyork/food-drink'
    newdata = scrape_timeout_articles(url)

    # Save to cache and print for validation
    save_cache(newdata)
    cache = open_cache()
    return cache


# In[ ]:




