import jsonpickle
import tweepy
import pandas as pd

import os
os.chdir('week-04')
from twitter_keys import api_key, api_secret

auth = tweepy.AppAuthHandler(api_key, api_secret)
# wait_on_rate_limit and wait_on_rate_limit_notify are options that tell our API object to automatically wait before passing additional queries if we come up against Twitter's wait limits (and to inform us when it's doing so).
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

def auth(key, secret):
  auth = tweepy.AppAuthHandler(key, secret)
  api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
  # Print error and exit if there is an authentication error
  if (not api):
      print ("Can't Authenticate")
      sys.exit(-1)
  else:
      return api

api = auth(api_key, api_secret)

def get_tweets(
    geo,
    out_file,
    search_term = '',
    tweet_per_query = 100,
    tweet_max = 150,
    since_id = None,
    max_id = -1,
    write = False
  ):
  tweet_count = 0
  all_tweets = pd.DataFrame()
  while tweet_count < tweet_max:
    try:
      if (max_id <= 0):
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            since_id = since_id
          )
      else:
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1)
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1),
            since_id = since_id
          )
      if (not new_tweets):
        print("No more tweets found")
        break
      for tweet in new_tweets:
        all_tweets = all_tweets.append(parse_tweet(tweet), ignore_index = True)
        max_id = new_tweets[-1].id
      ## return the last thing in the array
        tweet_count += len(new_tweets)
      ## adds the number of new tweets
      ## += is python shorthand for tweet_count = tweet_count + len(new_tweets)

    except tweepy.TweepError as e:
      # Just exit if any error
      print("Error : " + str(e))
      break
  print (f"Downloaded {tweet_count} tweets.")
  # if write == True:
  #     all_tweets.to_json(out_file)
  return all_tweets

# Set a Lat Lon
latlng = '42.359416,-71.093993' # Eric's office (ish)
# Set a search distance
radius = '5mi'
# See tweepy API reference for format specifications
geocode_query = latlng + ',' + radius
# set output file location
file_name = 'data/tweets.json'
# set threshold number of Tweets. Note that it's possible
# to get more than one
t_max = 5000

get_tweets(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  out_file = file_name
)

def parse_tweet(tweet):
  p = pd.Series()
  ## series is a one-row data frame
  if tweet.coordinates != None:
    p['lat'] = tweet.coordinates['coordinates'][0]
    p['lon'] = tweet.coordinates['coordinates'][1]
  else:
    p['lat'] = None
    p['lon'] = None
  p['location'] = tweet.user.location
  ## this sets a key for each attribute
  p['id'] = tweet.id_str
  p['content'] = tweet.text
  p['user'] = tweet.user.screen_name
  p['user_id'] = tweet.user.id_str
  p['time'] = str(tweet.created_at)
  return p

tweets = get_tweets(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  out_file = file_name)

#RELOADING DATA CODE: df = pd.read_json('path/example_json.json')

# Import some additional libraries that will allow us to plot and interact with the operating system
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

tweets.dtypes
tweets['location'].unique()
loc_tweets = tweets[tweets['location'] != '']
## limits to tweets that have location specified
count_tweets = loc_tweets.groupby('location')['id'].count()
## counts tweets grouping by location
df_count_tweets = count_tweets.to_frame()
df_count_tweets
df_count_tweets.columns
df_count_tweets.columns = ['count']
## sets name of the column
df_count_tweets

df_count_tweets.sort_index()

bos_list = tweets[tweets['location'].str.contains("Boston")]['location']
## creates a mask for the array to pass through. searching for string that contains 'boston'
tweets['location'].replace(bos_list, 'Boston, MA', inplace = True)
## this replaces all the things with Boston, MA
tweets['location'].unique()
## data has been replaced with more consistent conventions

camb_list = tweets[tweets['location'].str.contains("cambridge")]['location']
tweets['location'].replace(camb_list, 'Cambridge, MA', inplace = True)

somewhere_list = tweets[tweets['location'].str.contains("somewhere")]['location']
tweets['location'].replace(somewhere_list, 'Somewhere', inplace = True)

somewhere1_list = tweets[tweets['location'].str.contains("Somewhere")]['location']
tweets['location'].replace(somewhere1_list, 'Somewhere', inplace = True)

somerville_list = tweets[tweets['location'].str.contains("somerville")]['location']
tweets['location'].replace(somerville_list, 'Somerville, MA', inplace = True)

somerville2_list = tweets[tweets['location'].str.contains("Somerville")]['location']
tweets['location'].replace(somerville2_list, 'Somerville, MA', inplace = True)

bos2_list = tweets[tweets['location'].str.contains("boston")]['location']
tweets['location'].replace(bos2_list, 'Boston, MA', inplace = True)

bos3_list = tweets[tweets['location'].str.contains("BOSTON")]['location']
tweets['location'].replace(bos3_list, 'Boston, MA', inplace = True)

florida_list = tweets[tweets['location'].str.contains("Florida")]['location']
tweets['location'].replace(florida_list, 'Florida, USA', inplace = True)

cali_list = tweets[tweets['location'].str.contains("California")]['location']
tweets['location'].replace(cali_list, 'California, USA', inplace = True)

there_list = tweets[tweets['location'].str.contains("There")]['location']
tweets['location'].replace(there_list, 'There', inplace = True)

there2_list = tweets[tweets['location'].str.contains("there")]['location']
tweets['location'].replace(there2_list, 'There', inplace = True)

LA_list = tweets[tweets['location'].str.contains("Los Angeles")]['location']
tweets['location'].replace(LA_list, 'Los Angeles, CA', inplace = True)

lagos_list = tweets[tweets['location'].str.contains("Lagos")]['location']
tweets['location'].replace(lagos_list, 'Lagos, Nigeria', inplace = True)

india_list = tweets[tweets['location'].str.contains("India")]['location']
tweets['location'].replace(india_list, 'India', inplace = True)

chicago_list = tweets[tweets['location'].str.contains("Chicago")]['location']
tweets['location'].replace(chicago_list, 'Chicago, IL', inplace = True)

newyork_list = tweets[tweets['location'].str.contains("NYC")]['location']
tweets['location'].replace(newyork_list, 'New York, NY', inplace = True)

newyork1_list = tweets[tweets['location'].str.contains("New York")]['location']
tweets['location'].replace(newyork1_list, 'New York, NY', inplace = True)

tweets['location'].unique()


tweets[tweets.duplicated(subset = 'content', keep = False)]
tweets.drop_duplicates(subset = 'content', keep = False, inplace = True)

tweets.to_csv('twitter_nosearch.csv', sep=',', encoding='utf-8')


# Create a list of colors (from iWantHue)
colors = ["#697dc6","#5faf4c","#7969de","#b5b246",
          "#cc54bc","#4bad89","#d84577","#4eacd7",
          "#cf4e33","#894ea8","#cf8c42","#d58cc9",
          "#737632","#9f4b75","#c36960"]

# Create a pie chart
plt.pie(df_count_tweets['count'], labels=df_count_tweets.index.get_values(), radius = 10, shadow=False, colors=colors, labeldistance = 1.2, rotatelabels = True)
plt.axis('equal')
plt.tight_layout()
plt.show()

# Create a filter from df_tweets filtering only those that have values for lat and lon
tweets_geo = tweets[tweets['lon'].notnull() & tweets['lat'].notnull()]
len(tweets_geo)
len(tweets)
# Use a scatter plot to make a quick visualization of the data points
plt.scatter(tweets_geo['lon'], tweets_geo['lat'], s = 25)
plt.show()



##WITH SEARCH TERM

def get_tweets_search(
    geo,
    out_file,
    search_term = 'climate',
    tweet_per_query = 100,
    tweet_max = 150,
    since_id = None,
    max_id = -1,
    write = False
  ):
  tweet_count = 0
  all_tweets = pd.DataFrame()
  while tweet_count < tweet_max:
    try:
      if (max_id <= 0):
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            since_id = since_id
          )
      else:
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1)
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1),
            since_id = since_id
          )
      if (not new_tweets):
        print("No more tweets found")
        break
      for tweet in new_tweets:
        all_tweets = all_tweets.append(parse_tweet(tweet), ignore_index = True)
        max_id = new_tweets[-1].id
      ## return the last thing in the array
        tweet_count += len(new_tweets)
      ## adds the number of new tweets
      ## += is python shorthand for tweet_count = tweet_count + len(new_tweets)

    except tweepy.TweepError as e:
      # Just exit if any error
      print("Error : " + str(e))
      break
  print (f"Downloaded {tweet_count} tweets.")
  # if write == True:
  #     all_tweets.to_json(out_file)
  return all_tweets

# Set a Lat Lon
latlng = '42.359416,-71.093993' # Eric's office (ish)
# Set a search distance
radius = '5mi'
# See tweepy API reference for format specifications
geocode_query = latlng + ',' + radius
# set output file location
file_name = 'data/tweets.json'
# set threshold number of Tweets. Note that it's possible
# to get more than one
t_max = 5000

get_tweets(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  out_file = file_name
)

def parse_tweet(tweet):
  p = pd.Series()
  ## series is a one-row data frame
  if tweet.coordinates != None:
    p['lat'] = tweet.coordinates['coordinates'][0]
    p['lon'] = tweet.coordinates['coordinates'][1]
  else:
    p['lat'] = None
    p['lon'] = None
  p['location'] = tweet.user.location
  ## this sets a key for each attribute
  p['id'] = tweet.id_str
  p['content'] = tweet.text
  p['user'] = tweet.user.screen_name
  p['user_id'] = tweet.user.id_str
  p['time'] = str(tweet.created_at)
  return p

tweets = get_tweets_search(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  out_file = file_name)

import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

tweets.dtypes
tweets['location'].unique()
loc_tweets = tweets[tweets['location'] != '']
## limits to tweets that have location specified
count_tweets = loc_tweets.groupby('location')['id'].count()
## counts tweets grouping by location
df_count_tweets = count_tweets.to_frame()
df_count_tweets
df_count_tweets.columns
df_count_tweets.columns = ['count']
## sets name of the column
df_count_tweets

df_count_tweets.sort_index()

sbos_list = tweets[tweets['location'].str.contains("Boston")]['location']
tweets['location'].replace(sbos_list, 'Boston, MA', inplace = True)
sbright_list = tweets[tweets['location'].str.contains("Brighton")]['location']
tweets['location'].replace(sbright_list, 'Brighton, MA', inplace = True)
