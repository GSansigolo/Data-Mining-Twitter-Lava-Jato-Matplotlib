'''
Created on Oct 05, 2017
Author: @G_Sansigolo
'''

import pymongo
from pymongo import MongoClient
import json
import twitter
from pprint import pprint

'''
OAUTH
'''

CONSUMER_KEY      = "" 
CONSUMER_SECRET   = "" 
OAUTH_TOKEN       = "" 
OATH_TOKEN_SECRET = ""

auth = twitter.oauth.OAuth(OAUTH_TOKEN,OATH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

'''
connect mongodb database
'''

client = MongoClient()
db = client.tweet_db_1
tweet_collection = db.tweet_collection
tweet_collection.create_index([("id", pymongo.ASCENDING)],unique = True) 

'''
define query in REST API
'''
 
count = 100

#geocode = "-84.56,33.62,50mi

 
q = "lava jato"
  
'''
fetch data
'''

search_results = twitter_api.search.tweets( count=count,q=q)
#pprint(search_results['search_metadata'])
         
statuses = search_results["statuses"]


since_id_new = statuses[-1]['id']

for statuse in statuses:
   
    try:
        tweet_collection.insert(statuse)
	#pprint(statuse['created_at'])
  
    except:
        pass
        

'''
continue fetching previous data with the same query
YOU WILL REACH YOUR RATE LIMIT VERY FAST
'''   
since_id_old = 0
while(since_id_new != since_id_old):
    #pprint(search_results['search_metadata'])
    since_id_old = since_id_new
    search_results = twitter_api.search.tweets( count=count,q=q, max_id= since_id_new)
    statuses = search_results["statuses"]

    since_id_new = statuses[-1]['id']

    for statuse in statuses:
                
        try:
            tweet_collection.insert(statuse)
	    #pprint(statuse['created_at'])
        except:
            pass
 
'''
query collected data in MongoDB

 
tweet_cursor = tweet_collection.find()
  
print (tweet_cursor.count())
  
user_cursor = tweet_collection.distinct("user.id")
 
print (len(user_cursor))
 
 
  
for document in tweet_cursor:
    try:
        print ('----')
#         pprint (document)
 
  
        print ('name:', document["user"]["name"])
        print ('text:', document["text"])
    except:
        print ("***error in encoding")
        pass
'''    
