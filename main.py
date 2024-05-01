#!/usr/bin/env python
# coding: utf-8

# In[1]:


import locationBasedRecommendation
import dataStructureGraph
import yelpApi
import timeout_article
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import webbrowser


def yes(prompt):
    user_response = input(prompt).lower()
    positive_responses = ["yes", "y", "yup", "sure"]
    return user_response in positive_responses


def forDetailed_info(num):
    df,a = locationBasedRecommendation.cleanData()
    #driver = webdriver.Chrome(ChromeDriverManager().install())
    #driver.get(df['url'][int(num)])
    webbrowser.open(df['url'][int(num)])

def search_n_display(description):
    rec = locationBasedRecommendation.recommend(description)
    display = rec.copy()
    display.drop(columns=['reviews','similarity'], inplace=True)
    print(display[:20])



def personalize(user_key,user_location):
    print(f"\nLet's find your favourite food in {user_location}!")
    print('\nHere are some basic information you might want to know about the restaurants in the city!')
    yelpApi.main(user_key,user_location)


def default(user_key,user_location):
    print(f"\nLet's find your favourite food in {user_location}!")
    print("\nHere are some basic information that you might want to know about the restaurants in the city!")
    time.sleep(6)
    #dataStructureGraph.main()
    start = yes("\nDo you want start for a recommendation for restaurants with specific category? ")
    while start:
        print("\nWhat kind of restaurants are you looking for?")
        description = input("\nWords such as'good for party', 'fancy palce for meeting' would be recommended for matching perfect restaurants: ")
        search_n_display(description)
        temp = True
        while temp:
            num = input("\nPlease enter the number before the name of restaurant to get more detailed information about it: ")
            forDetailed_info(num)
            prompt = yes("\nDo you want to have a look at the other restaurants? ")
            temp = True if prompt else False 
        start = yes("\nDo you want to start by entering key words? ")
       

def article():
    dict = timeout_article.main()
    temp = 0
    for i in dict:
        for key in i:
            temp += 1
            print(temp,key)
    conti = True
    while conti:
        num = input("\nWhich section's articles would you like to read? Please enter a number: ")
        for values in dict[int(num)-1].values():
            for i in values:
                for j in i.values():
                    print(j)
        conti = yes("\nDo you want to read the articles from the other sections? ")



def main():
    print('Hi! Welcome to location based restaurants recommendation program!\n')
    s = True
    while s:
        print("\nDo you wish to create an app on Yelp's Developer site to get your own key and personalize the program?\n")
        personalize = yes("\nPlease enter yes or no:  ")
        if personalize:
            user_key = input('\nPlease enter your key: ')
            user_location = input('\nPlease enter your location')
            default(user_key,user_location)
        else:
            user_key = 'yC5KZDAAh3mve9aiTTFPaI47UMqTsKGej2uNt0LnRJhzAbgnReE6dcTsxkyUINaA6MU7frbR0B3mjCznCXIHErn7iAmc--mT-XZJAuAzufCg63Mo8oAeNGkA19s9ZHYx'
            user_location = 'New York City'
            default(user_key,user_location)
        
        print(f"\nThere is no satisfied restaurants? Here are some latest articles from timeout website about {user_location} you might be interested in! ")
        article()
        s = yes("\nDo you want another round? ")

    print("\nThank you! Bye!")


if __name__ == '__main__':
    main()
    


# In[ ]:




