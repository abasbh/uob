# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'streamapi.settings')

from django.conf import settings  # noqa

app = Celery('streamapi')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

import json
from celery import shared_task
from celery import task
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from celery.events import state
from celery.app.control import Control
import pymongo
from pymongo import MongoClient
from datetime import datetime 
from celery.task.control import discard_all
from celery.app.control import Inspect
from celery.worker.consumer import Consumer
from celery.backends.cache import CacheBackend


client = MongoClient()
db = client.twitterdb
collection = db.stream

consumer_key="mzujlzzfhJLnCKVx9sWP4otIi"
consumer_secret="MdN2nx9kgXVq6sWPMkStedfSWwPVPTLkKWJD947muCdHAWycVy"
access_token="376667192-xcRIUoGpbhha7NXpdSqvGEaUq7z1edzZePx6icgM"
access_token_secret="CXTZRvzX8y9sDd3WmpTDN03P6sUyQFWjpYiFBT4xpycnP"

import time
from celery.app.control import Control
#from myapp.tasks import celery # my application's Celery app


def task_e(tid):
    control = Control(app)     
    inspect = control.inspect()
    if True:
        active = inspect.active()
        running_jobs = []
        if active != None:
            for key, value in active.items():
                running_jobs.extend(value)
            if len(running_jobs) == 1:
                control.revoke(tid,terminate=True)
                print 'revoke ', tid
        
def clear_twitter():
    control = Control(app)
    #control.cancel_consumer('streamapi') # queue name, must probably be specified once per queue, but my app uses a single queue
     
    inspect = control.inspect()
    if True:
        active = inspect.active()
        print active
        running_jobs = []
        if active != None:
            for key, value in active.items():
                running_jobs.extend(value)
            if len(running_jobs) > 0:
                print("{} jobs running: {}".format(len(running_jobs), ", ".join(job["name"] for job in running_jobs)))
                for job in running_jobs:
                    #if job['name'] == 'fetch':
                    control.revoke(job["id"],terminate=True)
                discard_all()
                #time.sleep(10)
            else:
                print("No running jobs")
         
        
    app2 = state.State()
    cont = Control()
    i = Inspect()
    query = app2.tasks_by_type('fetch')
    print 'query ' ,query

    for uuid, task in query:
        #cont.revoke(uuid, terminate=True)
        print uuid, task

    #cont.purge() 
    a = discard_all() 
    print a
    #cache = CacheBackend(self.request.id, "Running")

    #co = Consumer()
    #b = co.stop()



@shared_task(name='fetch',bind=True)
def fetch(self,keyword):
        #keyword = ['uob','#uob',u'جامعة البحرين',u'#جامعة_البحرين'] 
	#Create a class inheriting from StreamListener
        print 'Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(self.request)
        taskid = '{0.id}'.format(self.request)
        #task_e(taskid)
        
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
                                collection.insert({'keyword':keyword,'data':data,'time':dtime,'label': None})
                                print data['text']
                                print 'every thing is ok !'
                                #print taskid
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

