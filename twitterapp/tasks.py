# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

import json
import celery
from celery import shared_task
from celery import task
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import json

import pymongo
from pymongo import MongoClient
from datetime import datetime 


client = MongoClient()
db = client.twitterdb
collection = db.stream

consumer_key="mzujlzzfhJLnCKVx9sWP4otIi"
consumer_secret="MdN2nx9kgXVq6sWPMkStedfSWwPVPTLkKWJD947muCdHAWycVy"
access_token="376667192-xcRIUoGpbhha7NXpdSqvGEaUq7z1edzZePx6icgM"
access_token_secret="CXTZRvzX8y9sDd3WmpTDN03P6sUyQFWjpYiFBT4xpycnP"

@task
def my_old_task():
   pass
'''
@shared_task(name='fetch',bind=True)#,rate_limit='1/h')
def fetch(self,keyword):
        #keyword = ['uob','#uob',u'جامعة البحرين',u'#جامعة_البحرين'] 
	#Create a class inheriting from StreamListener
        print 'Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(self.request)

        class StdOutListener(StreamListener):
                """ A listener handles tweets that are received from the stream.
                This is a basic listener that just prints received tweets to stdout.
                """
                def on_data(self, data):
                        data = json.loads(data)
                        cursor =  collection.transactions.find({'data.id_str':str(data['id_str'])})
                        for a in cursor :
                                return True


                        dtime = ''

                        x = -1
                        if any(k in data['text'] for k in keyword):
                                x += 1

                        else:
                                print 'not in our target'
                                return True
                                
                        if 'created_at' in data:
                                print data['created_at']
                                dtime = datetime.strptime(data['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                                print dtime
                        if 'text' in data:
                                collection.insert({'keyword':keyword,'data':data,'time':dtime})
                                print data['text']
                                print 'every thing is ok !'
                        return True

                def on_error(self, status):
                        print status
                        return True
                        
                def on_timeout(self):
                        print 'Timeout...'
                        return True # Don't kill the stream

                def on_status(self, status):
                        print status.text
	l = StdOutListener()
		
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
    
	#Using that class create a Stream object
	stream = Stream(auth, l)
	stream.filter(track=keyword,languages=['ar'])

	
'''

	    
	
