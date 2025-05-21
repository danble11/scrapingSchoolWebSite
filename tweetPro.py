from hashlib import new
import tweepy
import csv
import os
import pandas as pd
from bs4 import BeautifulSoup

import schoolList
import exeptionList

consumer_key = 'UmPKnpStvqROoSK1C9ZPoz4xb'
consumer_secret = '6D03uEESvC6cfNjeGao98f7kkonjnRIxroIVNSaDEZ8qoIA67S'
access_token = '1531825263881129984-w2rq2lgHywJi7DXy4MvFqaJS9s3LcJ'
access_token_secret = 'IQ7xt0U0s4OGJVAS4hHUZpBLry6HOXQBkMUSL3NeBLOfK'

tewwtdedDaraPath = '/home/fumanishizawa/SchoolPageCrowring/TweetedContents.csv'

def tweetNewinfo(newInfo,schoolName):
    client = tweepy.Client(
        consumer_key = consumer_key,
        consumer_secret = consumer_secret,
        access_token = access_token,
        access_token_secret = access_token_secret
    )
    for tweetContent in newInfo:
        tweetContent = ",".join(map(str, tweetContent))
        tweetContent = tweetContent.replace('[','')
        tweetContent = tweetContent.replace(']','')
        tweetContent = tweetContent.replace(' ','')
        tweetContent = tweetContent.replace('　','')
        tweetContent = tweetContent.replace("\\u3000",'')
        tweetContent = tweetContent.replace("\\n",'')
        tweetContent = tweetContent.replace("'",'')
        tweetContent = tweetContent.replace(',','\n\n'+schoolName+'\n')

        tweetedcontents = pd.read_csv("TweetedContents.csv")


        if(tweetContent not in exeptionList.exceptionList and tweetContent != '' and tweetContent not in tweetedcontents.values):
            print(tweetContent)
            try:
                client.create_tweet(text = '新しいお知らせが掲載されました\n\n'+tweetContent)
                with open('TweetedContents.csv','a') as f:
                    writer = csv.writer(f)
                    writer.writerow([tweetContent])
            
            except:
                print(schoolName + 'Error')
                """f = open('exeptionList.py' , 'a')
                print(f.read())
                f.close"""
                
            

        
    


