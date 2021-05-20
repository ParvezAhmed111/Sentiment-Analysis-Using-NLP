# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 21:03:07 2020

@author: parve
"""

#Importing all libraries
from tkinter import *
import praw
import tweepy
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import json
from os.path import join, dirname
import paralleldots
from ibm_watson import SpeechToTextV1
from praw.models import MoreComments
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('2GLz9FSNQKpCutmiRtpVMG3AJQPh_DItUe89rTwy4QJC')
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)
speech_to_text.set_service_url('https://gateway-lon.watsonplatform.net/speech-to-text/api')

#Client details for Twitter API
consumer_key = "pZb2PizxEsB1eyMcMtPKt0"
consumer_secret = "MLAIqKyYVkdykZ6eibeoWcPOX56gOgfV0vkWIVzmKEVxGQ"
access_key = "3046753945-qtQ26I5KlW9Ng1LmX44OxdbJTQ8vpcDBPBE"
access_secret = "yxNsmJMzxB7WumR5u2HB9NYM5Cdftj3pRSwwaxQCTw"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

#Client details Sentiment Analysis API service
paralleldots.set_api_key("SLlVzk4on9gsErs1SUKzIAgotNmB33j7HcZT77Lo")
#Client details for Reddit API
reddit = praw.Reddit(client_id = "bqa8w7IjEhQw",
                         client_secret = "e-nSLf7A6gP1U4U4K15BoArM8",
                         password= "thisisword",
                         username="dotthrowaway123",
                         user_agent="taining",)

#Code for the main Window
root=Tk()
frame=Frame(root)
#Code for functioning of "Checking Personality"
def window1():
    first_window=Toplevel(frame, width=400, height=300)
    def UserSentiment():
        #taking input from text field
        twitteruser = e1.get()
        reddituser = e2.get()
#Code for extracting User's Input Twitter data
        tmp=[]
        b = ""
        thetweet = []
        #in case there's no input
        if len(twitteruser)==0 and len(reddituser)==0:
            c=Label(first_window).config(text="")
            c=Label(first_window, text = "Enter at least one ID")
            c.grid(row=2, columnspan=3)
        else:
            if len(twitteruser)>0:
                number_of_tweets=200
                try:

                    #calling API
                    tweets = api.user_timeline(screen_name=twitteruser, count=number_of_tweets, tweet_mode="extended")
                    tweets_for_csv = [tweet.full_text for tweet in tweets]
                    #making the tweets into coherent sentences
                    for j in tweets_for_csv:
                        thetweet = j.split()
                        thetweet.pop(-1)
                        for word in thetweet:
                            b = b + " " + str(word)
                    tmp.append(b)
                    twerror=False
                except Exception:
                    c=Label(first_window).config(text="")
                    c=Label(first_window, text = "Make sure that the ID you entered is correct")
                    c.grid(row=2, columnspan=3)
                    twerror=True
            else:
                twerror=False

    #Code for extracting User's Input data
            commentvar = ""
            if len(reddituser)>0:
                try:
                    #calling Reddit's API
                    for comment in reddit.redditor(reddituser).comments.new(limit=None):
                        commentvar = commentvar + " " + str(comment.body)
                    rederror=False
                except Exception:
                    c=Label(first_window).config(text="")
                    c=Label(first_window, text = "Make sure that the ID you entered is correct")
                    c.grid(row=2, columnspan=3)
                    rederror=True
            else:
                rederror=False
            #join words from both reddit and twitter
            text = str(tmp) + " " + commentvar
    #Code for the functioning of Personality Insight using Extarcted Data for Checking Personality
            if twerror==False and rederror==False and len(text.split())>25:
                try:
                    UserDict = paralleldots.emotion(text)['emotion']
                    df = pd.DataFrame.from_dict(UserDict, orient = 'index')
                    df.reset_index(inplace=True)
                    df.columns=['Sentiment', 'Percentile']
                    plt.figure(figsize=(15,5))
                    sns.barplot(x="Sentiment", y="Percentile", data = df)
                    plt.show()
                except Exception:
                    c=Label(first_window).config(text="")
                    c=Label(first_window, text = "Not enough words to scan, please enter ID of a different
person")
                    c.grid(row=2, columnspan=3)

            else:

                c=Label(first_window).config(text="")
                c=Label(first_window, text = "Not enough words to scan, please enter ID of a different person")
                c.grid(row=2, columnspan=3)

#Code for "Checking Personality" GUI Window
    a = Label(first_window,text="Twitter Username")
    a.grid(row=0, column=0)
    b = Label(first_window,text="Reddit Username")
    b.grid(row=1, column=0)
    c = Label(first_window, text="")
    c.grid(row=2, columnspan=3)

    e1 = Entry(first_window)
    e2 = Entry(first_window)
    e1.grid(row=0, column=2, pady=10, padx=15)
    e2.grid(row=1, column=2)
    Button(first_window,text='Begin analysis', command=UserSentiment).grid(row=3,sticky=W,pady=4,column=2,padx=20)

#Code for "Checking your Interest" using Stack Overflow data
def window2():
    third_window=Toplevel(frame)

#Code for "Check your Interest" GUI Window excluding Button
    stackidlabel=Label(third_window, text="Enter Reddit post url")
    stackidlabel.grid(row=0, column=0, padx=10, pady=10)
    stackidentry=Entry(third_window)

    stackidentry.grid(row=0, column=2, padx=10, pady=10)
    exceptionlabel=Label(third_window)
    exceptionlabel.grid(row=2, column=1)
    def getuserdatared():
#Code for getting User Input's data and extracting data from Stack Overflow with Try Exception Handling
        try:
            redurl=stackidentry.get()
            submission = reddit.submission(url=redurl)
            SenDict = {"negative":0, "neutral":0, "positive":0}
            for top_level_comment in submission.comments:
                if isinstance(top_level_comment, MoreComments):
                    continue
                text = top_level_comment.body
                #print(text)
                RedditPostSentiment = paralleldots.sentiment(text)['sentiment']
                LoopSen=max(RedditPostSentiment, key = lambda x: RedditPostSentiment.get(x))
                if LoopSen == "negative":
                    SenDict["negative"]+=1
                elif LoopSen == "positive":
                    SenDict["positive"]+=1
                elif LoopSen == "neutral":
                    SenDict["neutral"]+=1
                else:
                    pass
            df = pd.DataFrame.from_dict(SenDict, orient = 'index')
            df.reset_index(inplace=True)
            df.columns=['Sentiment', 'Frequency']
            plt.figure(figsize=(15,5))
            sns.barplot(x="Sentiment", y="Frequency", data = df)
            plt.show()
        except Exception:
            errortext=Label(fourth_window).config(text="")
            errortext=Label(fourth_window, text="Please enter a correct url")
            errortext.grid(row=2, column=1)

#Code for Submit Button and it's command
    enterstackdata=Button(third_window, text="Submit", command=getuserdatared)
    enterstackdata.grid(row=1, column=1, padx=10, pady=10)

#Code for the functioning of "Analyze via Audio"
def window3():
    fourth_window=Toplevel(frame)

#Code for "Analyze via Audio" GUI Window excluding Button
    audiolabel=Label(fourth_window, text="Please enter the file path for your audio file")
    audiolabel.grid(row=0, column=0, padx=10, pady=10)
    errortext=Label(fourth_window, text="")
    errortext.grid(row=1)
    audfilepath=Entry(fourth_window)
   audfilepath.grid(row=0, column=2, padx=10, pady=10)
   wait=Label(fourth_window, text="Please wait patiently after clicking Submit, transcribing audio will take as long as the audio is")
    wait.grid(row=2, columnspan=4)
    def transcribe():
#Code for getting the Audio file and coverting the speech into text and then analyzing it using Personality Insight with Try Exception Handling
        script=audfilepath.get()
        try:
            with open(script,
            'rb') as audio_file:
                prof = speech_to_text.recognize(audio_file, content_type="audio/mp3").result
            a = json.dumps(prof, indent = 4)
            z=0
            y=0
            for i in prof['results']:
                z=z+1
            trlist=[]
            for i in range(z):
                transcripts = prof['results'][i]['alternatives'][0]['transcript']
                trlist.append(transcripts)
            trstr=""
            for j in trlist:
                trstr = trstr + " " + j
            UserDict = paralleldots.emotion(trstr)['emotion']
            print(trstr)
            df = pd.DataFrame.from_dict(UserDict, orient = 'index')
            df.reset_index(inplace=True)
            df.columns=['Sentiment', 'Percentile']
            plt.figure(figsize=(15,5))
            sns.barplot(x="Sentiment", y="Percentile", data = df)
            plt.show()
        except Exception:
            errortext=Label(fourth_window).config(text="")
            errortext=Label(fourth_window, text="Error in finding file, please make sure the path is correct and the format is mp3")
            errortext.grid(row=2, column=1)

#Code for Submit button and it's command
    speechtotext=Button(fourth_window, text="Submit", command=transcribe)
    speechtotext.grid(row=1, column=1, padx=10, pady=10)

#Code for the main GUI Window
checkpersonality=Button(frame, text="Check sentiments of a person", command=window1)
checkpersonality.grid(row=0, column=0, padx=10, pady=10)
comparetwopeople=Button(frame, text="Analyse a Reddit post", command=window2)
comparetwopeople.grid(row=0, column=1, padx=10, pady=10)
analyzeaudio=Button(frame, text="Analyze via audio", command=window3)
analyzeaudio.grid(row=0, column=3, padx=10, pady=10)
cleargraph=Label(frame, text="If there are any graph open, please close them before preeceding")
cleargraph.grid(row=1,columnspan=5)
frame.pack()
root.mainloop()
