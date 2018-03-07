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
  if write == True:
       all_tweets.to_json(out_file)
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
t_max = 2000

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

suff_list = tweets[tweets['location'].str.contains("SUFFOLK")]['location']
tweets['location'].replace(suff_list, 'Suffolk County, MA', inplace = True)

florida_list = tweets[tweets['location'].str.contains("Florida")]['location']
tweets['location'].replace(florida_list, 'Florida, US', inplace = True)

us_list = tweets[tweets['location'].str.contains("USA")]['location']
tweets['location'].replace(us_list, 'US', inplace = True)

mich_list = tweets[tweets['location'].str.contains("M I C H I G A N")]['location']
tweets['location'].replace(mich_list, 'Michigan, US', inplace = True)

moreUS_list = tweets[tweets['location'].str.contains("Estados")]['location']
tweets['location'].replace(moreUS_list, 'US', inplace = True)

United_list = tweets[tweets['location'].str.contains("United")]['location']
tweets['location'].replace(United_list, 'US', inplace = True)

bos2_list = tweets[tweets['location'].str.contains("BOS")]['location']
tweets['location'].replace(bos2_list, 'Boston, MA', inplace = True)

unknown_list = tweets[tweets['location'].str.contains('M̴̳̝̺̅̽̔Á̵̟̦̗̈̋Ș̶̝͇̓̐͝S̵̡̎͊͝')]['location']
tweets['location'].replace(unknown_list, 'Unknown', inplace = True)

unknown2_list = tweets[tweets['location'].str.contains('gurls')]['location']
tweets['location'].replace(unknown2_list, 'Unknown', inplace = True)

unknown3_list = tweets[tweets['location'].str.contains('other')]['location']
tweets['location'].replace(unknown3_list, 'Unknown', inplace = True)

unknown4_list = tweets[tweets['location'].str.contains('in my')]['location']
tweets['location'].replace(unknown4_list, 'Unknown', inplace = True)

print(tweets['location'].unique())


tweets[tweets.duplicated(subset = 'content', keep = False)]
tweets.drop_duplicates(subset = 'content', keep = False, inplace = True)

tweets.to_csv('twitter_nosearch.csv', sep=',', encoding='utf-8')


# Create a list of colors (from iWantHue)
colors = ["#697dc6","#5faf4c","#7969de","#b5b246",
          "#cc54bc","#4bad89","#d84577","#4eacd7",
          "#cf4e33","#894ea8","#cf8c42","#d58cc9",
          "#737632","#9f4b75","#c36960"]

# Create a pie chart
plt.pie(df_count_tweets['count'], labels=df_count_tweets.index.get_values(), shadow=False, colors=colors, rotatelabels = True)
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
  if write == True:
     all_tweets.to_json(out_file)
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
t_max = 2000

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

tweets_climate = get_tweets_search(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  out_file = file_name)

import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

tweets_climate.dtypes
tweets_climate['location'].unique()
loc_tweets_climate = tweets_climate[tweets_climate['location'] != '']
## limits to tweets that have location specified
count_tweets_climate = loc_tweets.groupby('location')['id'].count()
## counts tweets grouping by location
df_count_tweets_climate = count_tweets.to_frame()
df_count_tweets_climate
df_count_tweets_climate.columns
df_count_tweets_climate.columns = ['count']
## sets name of the column
df_count_tweets_climate

df_count_tweets_climate.sort_index()

sbright_list = tweets_climate[tweets_climate['location'].str.contains("Brighton")]['location']
tweets_climate['location'].replace(sbright_list, 'Brighton, MA', inplace = True)

sbos_list = tweets_climate[tweets_climate['location'].str.contains("Boston")]['location']
tweets_climate['location'].replace(sbos_list, 'Boston, MA', inplace = True)

scamb_list = tweets_climate[tweets_climate['location'].str.contains("Cambridge")]['location']
tweets_climate['location'].replace(scamb_list, 'Cambridge, MA', inplace = True)

susa_list = tweets_climate[tweets_climate['location'].str.contains("U.S.A")]['location']
tweets_climate['location'].replace(susa_list, 'United States', inplace = True)

ssomer_list = tweets_climate[tweets_climate['location'].str.contains("Somerville")]['location']
tweets_climate['location'].replace(ssomer_list, 'Somerville, MA', inplace = True)

sdc_list = tweets_climate[tweets_climate['location'].str.contains("DC")]['location']
tweets_climate['location'].replace(sdc_list, 'Washington DC', inplace = True)

smiami_list = tweets_climate[tweets_climate['location'].str.contains("Miami")]['location']
tweets_climate['location'].replace(smiami_list, 'Miami, FL', inplace = True)

sflorida_list = tweets_climate[tweets_climate['location'].str.contains("Florida")]['location']
tweets_climate['location'].replace(sflorida_list, 'Florida, US', inplace = True)

sny_list = tweets_climate[tweets_climate['location'].str.contains("New York")]['location']
tweets_climate['location'].replace(sny_list, 'New York, NY', inplace = True)

scali_list = tweets_climate[tweets_climate['location'].str.contains("California")]['location']
tweets_climate['location'].replace(scali_list, 'California, US', inplace = True)

snorth_list = tweets_climate[tweets_climate['location'].str.contains("north")]['location']
tweets_climate['location'].replace(snorth_list, 'United States', inplace = True)

scape_list = tweets_climate[tweets_climate['location'].str.contains("Cape")]['location']
tweets_climate['location'].replace(scape_list, 'Cape Cod, RI', inplace = True)

snh_list = tweets_climate[tweets_climate['location'].str.contains("NH")]['location']
tweets_climate['location'].replace(snh_list, 'New Hampshire, US', inplace = True)

snj_list = tweets_climate[tweets_climate['location'].str.contains("New Jersey")]['location']
tweets_climate['location'].replace(snj_list, 'New Jersey, US', inplace = True)

print(tweets_climate['location'].unique())

tweets_climate[tweets_climate.duplicated(subset = 'content', keep = False)]
tweets_climate.drop_duplicates(subset = 'content', keep = False, inplace = True)

tweets_climate.to_csv('twitter_climatesearch.csv', sep=',', encoding='utf-8')

tweets_climate_geo = tweets_climate[tweets_climate['lon'].notnull() & tweets['lat'].notnull()]
len(tweets_climate_geo)
len(tweets_climate)
# Use a scatter plot to make a quick visualization of the data points
plt.scatter(tweets_climate_geo['lon'], tweets_climate_geo['lat'], s = 25)
plt.show()

## END. 
