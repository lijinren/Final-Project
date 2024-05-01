# Final-Project-- Restaurant Reccomendation for Yelp
# main()
The users will be asked bunches of yes or no questions and provide some key words to get a reccomendation of restaurants near them. Firstly, the interesting part is that if they want to get their own key from Yelp and personalize the program, they can just input the key and their location. The user could find the way to create the account here "https://docs.developer.yelp.com/docs/fusion-intro". The program will help the user to retrieve the data from yelp and cache the data as well. The text in the data will also be processedfor recommendation, data would be also be cached after it was processed.

# yelpApi
The program retrieves information about 1000 restaurants in New York City using a default key and location. Due to the rate limit, a maximum of 5000 calls can be made, and exceeding this limit might cause an error. Once the data is retrieved, it will be cached into a JSON file.

# cacheRestaurants_info
After running the program, the data will be pre-processed and cached into a CSV file.

# locationBasedRecommendation
The data is processed within this program, and once processed, it will be cached into a CSV file. The similarities between restaurants, as well as the similarity between restaurants and the user's description, will be obtained after the program runs.

# dataStructureGraph
A graph is used as the data structure, with nodes representing restaurant names and edges representing the similarity between restaurants. After running the program, an HTML file containing a network of restaurants will be created and added to the specified path.

# Timeout_article
Articles about restaurants will be retrieved from the website "https://www.timeout.com/newyork/food-drink" and cached into a JSON file.




