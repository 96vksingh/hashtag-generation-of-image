import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from matplotlib import pyplot as plt
import numpy as np
from numpy  import array
import seaborn as sns
get_ipython().magic('matplotlib inline')







# In[18]:

class TwitterClient(object):
    def __init__(self):
        # keys and tokens from the Twitter Dev Console
        consumer_key = "qAZXMRvttjWaq4Ns8hR6KtIG7"
        consumer_secret = "XTBuR26hXrJFc4qwL7EzvtWMIq5dq7pnB01FAWfsRa0ViMDcGx"
        access_token = "497030183-5XWr6IF688dxPXKyF7Xx12eJ6PDSX4uNNaewc3fx"
        access_token_secret = "JlZOhLs923LQp6LZ82OgWWPUAA9x9xb2YoWulPECvUEOI"
 
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
 
    def clean_tweet(self, tweet):
        #remove links and special characters from the text using regex
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        #classifying sentment of passed tweets using textblobs sentiment method
        #Utility function to classify sentiment of passed tweet
        
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
        
    def get_tweet_sentiment_value(self, tweet):

        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # return sentiment value
        return analysis.sentiment.polarity
 
    def get_tweets(self, query, count = 1000):
        # tweets to getch tweets and parse them

        # empty list to store parsed tweets and tweet values
        tweets = []
        tweet_value = []
 
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)
 
            #if query['user']['lang'] == 'en':
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
                if (tweet.metadata['iso_language_code'] == 'en'):               
                    # saving text of tweet
                    parsed_tweet['text'] = tweet.text
                    
                    # saving sentiment of tweet
                    parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                    
                    print(parsed_tweet['text'])

                    # appending parsed tweet to tweets list
                    if tweet.retweet_count > 0:
                        # if tweet has retweets, ensure that it is appended only once
                        if parsed_tweet not in tweets:
                            tweets.append(parsed_tweet)
                            #tweet_value.append(self.get_tweet_sentiment_value(tweet.text))
                    else:
                        tweets.append(parsed_tweet)
                        #tweet_value.append(self.get_tweet_sentiment_value(tweet.text))
 
                tweet_value.append(self.get_tweet_sentiment_value(tweet.text))
            # return parsed tweets
            return tweets, tweet_value
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
 
def main(name):
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets, tweet_value = api.get_tweets(query = name, count = 100)

    #print(tweets['text'])
    file1 = open("data1.txt","w")
    
    #print(len(tweet_value))
        
    x = np.arange(0,len(tweet_value),1)
    y = np.asarray(tweet_value)
    
    plt.plot(x,y)
    plt.ylim(-1,1)
    plt.ylabel('Sentiment value')
    plt.xlabel('Tweet Count')
    plt.title('Twitter sentiment analysis for ' + name)
    plt.show()
    
    # picking positive tweets from tweets

    
if __name__ == "__main__":
    main("india")
   