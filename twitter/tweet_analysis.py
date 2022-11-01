# import the libraries
import base64
import io
import os
import urllib.parse
from typing import Any, List, Optional, Union
import math
import tweepy
from searchtweets import collect_results
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
import plotly.graph_objects as go
import pandas as pd
from io import StringIO
import numpy as np
import re
from matplotlib import pyplot as plt
plt.style.use('fivethirtyeight')
plt.switch_backend('agg')
# Get the data
log = pd.read_csv(
    'C:/Users/bsqua/Personal Projects/twitter_analysis/twitter_credentials.csv')

# Twitter API Credentials
accessToken = log['key'][0]
accessTokenSecret = log['key'][1]
consumerKey = log['key'][2]
consumerSecret = log['key'][3]

# Create the authentication object
authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)

# Set the access token and access token secret
authenticate.set_access_token(accessToken, accessTokenSecret)

# Create the API object while passing in the auth information
api = tweepy.API(authenticate, wait_on_rate_limit=True)

# Extract 100 tweets from the twitter user


def getTweets(query):
    posts = api.search_tweets(
        q=query, count=200, lang="en", tweet_mode="extended")
    # Create a dataframe with a column called Tweets

    df = pd.DataFrame(columns=['Tweets', 'Likes', 'Retweets', 'Date'])
    for tweet in posts:
        df1 = pd.DataFrame({'Tweets': tweet.full_text, 'Likes': tweet.favorite_count,
                            'Retweets': tweet.retweet_count, 'Date': tweet.created_at}, index=[tweet])
        df = pd.concat([df, df1], ignore_index=True)
        df = df.drop_duplicates(subset=['Tweets'])
    return df


# Clean the text

# Create a function to clean the tweets
def cleanTxt(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text)  # Removes @mentions
    text = re.sub(r'#', '', text)  # Removes hashtags
    text = re.sub(r'RT[\s]+', '', text)  # Removing RT
    text = re.sub(r'https?:\/\/\S+', '', text)  # Remove the hyper link

    return text


# Create a function to get the subjectivity
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

# Create a function to get the polarity


def getPolarity(text):
    return TextBlob(text).sentiment.polarity

# Create a function to compute the negative, neutral and positive analysis


def getAnalysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'


def getDataframe(query):
    df = getTweets(query)
    # Cleaning the text
    df['Tweets'] = df['Tweets'].apply(cleanTxt)

    # Create three new columns
    df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)

    df['Polarity'] = df['Tweets'].apply(getPolarity)

    df['Analysis'] = df['Polarity'].apply(getAnalysis)

    return df


def getRating(query):
    df = getDataframe(query)
    # make the mean polarity a scale of -1 to 1 and return

    # exclude neutral opinions?
    df = df[df['Polarity'] != 0]
    rating = df['Polarity'].mean()
    rating = math.floor(rating * 100)

    return rating


def getDistribution(df):
    # Get the distribution of positive, neutral, and negative opinions
    ptweets = df[df['Analysis'] == 'Positive']
    p = ptweets.shape[0]
    ntweets = df[df['Analysis'] == 'Negative']
    n = ntweets.shape[0]
    neutral = 100 - p - n
    return [p, n, neutral]


def getWordcloud(query):
    try:
        df = getDataframe(query)
        # Plot The Word Cloud
        plt.cla()
        allWords = ' '.join([twts for twts in df['Tweets']])
        stoplist = STOPWORDS
        stoplist.update({query, "Crypto", "Follow", "Giveaway",
                        "USD", "ETH", "Cryptocurrency"})
        wordCloud = WordCloud(width=500, height=300, random_state=21,
                              max_font_size=110, stopwords=stoplist).generate(allWords)
        plt.title('Word Cloud')
        plt.imshow(wordCloud, interpolation="bilinear")
        plt.tight_layout()
        plt.axis("off")
        fig = plt.gcf()
        fig.set_size_inches(5, 3, forward=True)
        image = io.BytesIO()
        plt.savefig(image, format='png')
        image.seek(0)
        string = base64.b64encode(image.read())
        image64 = "data:image/png;base64," + urllib.parse.quote_plus(string)
        return image64
    except ValueError:
        return None


def getPiechart(query):
    plt.cla()
    df = getDataframe(query)
    # Plot and visualize the counts
    fig = plt.figure()

    plt.title('Sentiment Analysis')
    plt.xlabel('Sentiment')
    plt.ylabel('Counts')
    plt.tight_layout()
    df['Analysis'].value_counts().plot(kind='pie')

    imgdata = StringIO()
    fig = plt.gcf()
    fig.set_size_inches(5, 3, forward=True)
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data
