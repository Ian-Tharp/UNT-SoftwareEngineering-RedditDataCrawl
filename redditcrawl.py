'''
Ian Tharp - ict0011
CSCE 3444
Professor Wajdi Aljedaani
4/9/22
Individual Assignment #2 - Reddit Data Crawl
References: https://medium.com/@plog397/webscraping-reddit-python-reddit-api-wrapper-praw-tutorial-for-windows-a9106397d75e
'''

import praw
import pandas as pd
import datetime as dt

optionchecker = ""
#Initialize Reddit developer keys
reddit = praw.Reddit(client_id='12_CHAR_CLIENTID',
                     client_secret='24_CHAR_CLIENTSECRET',
                     user_agent='SCRIPT_NAME',
                     password='REDDIT_LOGIN_PASSWORD')

while True:
    print("Do you want to select a specific subreddit, or search all?")
    optionchecker = input("1 - Yes, specific\n2 - No, all: ")
    if optionchecker == "1":
        break
    elif optionchecker == "2":
        break
#Create dictionary for pandas csv
dict = { "title":[], "subreddit":[],
        "votes":[], "id":[],
        "url":[], "comms_num": [],
        "created": [], "body":[]}

#Function to retrieve correct date time format
def get_date(created):
    return dt.datetime.fromtimestamp(created)

#Specific SubReddit searcher
if optionchecker == "1":
    subreddit1 = input("Enter SubReddit to search: ")
    keyword = input("Enter keyword to search: ")
    print("This will return the 'relevant' SubReddit posts in: " + subreddit1 + " including: " + keyword)

    sub = reddit.subreddit(subreddit1).search(keyword, limit=None)
    print("Retrieving data...(this may take a while)")
    for submission in sub:
        dict["title"].append(submission.title)
        dict['subreddit'].append(submission.subreddit)
        dict["votes"].append(submission.score)
        dict["id"].append(submission.id)
        dict["url"].append(submission.url)
        dict["comms_num"].append(submission.num_comments)
        dict["created"].append(submission.created)
        dict["body"].append(submission.selftext)
    print("Retrieval completed. ")

    df = pd.DataFrame(dict)
    df["created"] = df['created'].apply(get_date)
    df.drop_duplicates(subset=['id'], inplace=True)

    df.to_csv('RedditDataSpecificSR.csv')

#Search all of Reddit
elif optionchecker == "2":
    keyword = input("Enter keyword to search: ")
    print("This will return the 'relevant' Reddit posts including: " + keyword)

    no_subreddit = reddit.subreddit("all").search(keyword, limit=None)
    print("Retrieving data...(this may take a while)")
    for submission in no_subreddit:
        dict["title"].append(submission.title)
        dict['subreddit'].append(submission.subreddit)
        dict["votes"].append(submission.score)
        dict["id"].append(submission.id)
        dict["url"].append(submission.url)
        dict["comms_num"].append(submission.num_comments)
        dict["created"].append(submission.created)
        dict["body"].append(submission.selftext)
    print("Retrieval completed.")

    df = pd.DataFrame(dict)
    df["created"] = df['created'].apply(get_date)
    df.drop_duplicates(subset=['id'], inplace=True)

    df.to_csv('RedditDataNoSR.csv')
