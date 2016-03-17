# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
#from .tasks import fetch
from django.core.urlresolvers import reverse
from urlparse import urlparse

import simplejson
import json 
import re
# import nltk
# from nltk.tag import pos_tag
# from nltk.tokenize import word_tokenize

import pymongo 
from pymongo import MongoClient
from datetime import datetime

from .tools import *
client = MongoClient()
db = client.twitterdb
collection = db.stream
collection2 = db.label


'''
@csrf_exempt
def index(request):

	if request.method=='POST':
		keyword = request.POST['keyword']
		fetch.delay(keyword)
		
		collection.delete_many({})
		print 'All Documents are deleted'
		
		return HttpResponseRedirect(reverse('query',kwargs={'keyword':keyword}))
    
	context= {
        'title': 'Twitter App - Home',  
	}

	return render(request,'index.html', context)
'''

@csrf_exempt
def index(request):
        
        keyword = [u'uob',u'#uob',u'جامعة البحرين',u'#جامعة_البحرين']
        #keyword = u'uob,#uob,جامعة البحرين,#جامعة_البحرين'
        #keyword = u'#uob'
        #collection.delete_many({})

        '''
        if 's' not in request.session:
                print 'stream'
                fetch.delay(keyword)
                request.session['s'] = True
        '''     
        #fetch.delay(keyword)
        #fetch.apply_async(args=[keyword])
        #fetch.name
	context= {
        'title': 'Twitter App - Home',  
	}

	return render(request,'index.html', context)
@csrf_exempt
def query(request,keyword):
	context = {
		'title': 'UOBtweets',
		'keyword':keyword,
	}
	return render(request,'query.html',context)
def callD(i):
        query = collection.find({ 'time': { '$exists': 'true' } , 'label': None }).sort('time',-1).limit(i)#{'keyword': keyword})
        tweets=list()
        for j in query:
                i =  j['data']
                try:
                        tweet_json = { 'img' : i['user']['profile_image_url'],
                                       'username' : i['user']['name'],
                                       'screen_name' : i['user']['screen_name'],
                                       'text' : i['text'],
                                       'created_at' : j['time'],
                                       'tweet_id' : i['id_str']
                                       }
                        tweets.append(tweet_json)
                except:
                        print 'twitter data error..'
        return tweets
@csrf_exempt
def data(request):
        date = datetime.now()
        print 'date1: ' ,date
        if request.method == "POST" and request.is_ajax():
                tid = request.POST['id']
                #tid = str(tid)
                print 'tweet_id: ' ,tid
                query = collection.find({'data.id_str': tid }).sort('time',-1)
                tweets=list()
                for j in query:
                    i =  j['data']
                    try:
                        tweet_json = { 'img' : i['user']['profile_image_url'],
                                       'username' : i['user']['name'],
                                       'screen_name' : i['user']['screen_name'],
                                       'text' : i['text'],
                                       'created_at' : j['time'],
                                       'tweet_id' : i['id_str']
                                       }
                        tweets.append(tweet_json)
                    except:
                        print 'twitter data error..'

                t = tweets[0]['created_at']


                query = collection.find({ 'time': { '$gte': t } ,'label':None }).sort('time',-1)

                stream=list()
                for j in query:
                    i =  j['data']
                    if i['id_str'] == tid:
                      continue
                    try:
                        tweet_json = { 'img' : i['user']['profile_image_url'],
                                       'username' : i['user']['name'],
                                       'screen_name' : i['user']['screen_name'],
                                       'text' : i['text'],
                                       'created_at' : j['time'],
                                       'tweet_id' : i['id_str']
                                       }
                        stream.append(tweet_json)
                    except:
                        print 'twitter data error..'
                #a = callD(3)
                return render(request,'tweets.html',{'tweets':stream})
                

                
                        
                

        else:
                print 'no ID'
                a = callD(50)
                
                return render(request,'tweets.html',{'tweets': a})


@csrf_exempt
def label(request):
        date = datetime.now()
        print 'label date: ' ,date
        if request.method == "POST" and request.is_ajax():
                tid = request.POST['id']
                sent = request.POST['sent']
                main = request.POST['main']
                subt = request.POST['subt']
                #tid = str(tid)
                print 'label tweet_id: ' ,tid
                query = collection.update_one({'data.id_str': tid},{'$set': {'label':'label'}})
                if query.matched_count == 1 and query.modified_count == 1:
                        print 'ok label'
                        a = { 'id': tid,
                          'sent': sent,
                          'main': main,
                          'subt': subt,
                          'date':date,
                          }
                        result = collection2.insert_one(a)
                

                        if result.inserted_id:
                                print 'ok insert'
                                return HttpResponse("Success")
                else:
                    return HttpResponse("Fail")
                

                
                        
                

        else:
                print 'no ID'
                a = callD(50)
                
                return render(request,'tweets.html',{'tweets': a})


###############################################################################
#improve



tool = tools()
def callT(i):
        
        query = collection.find({ 'time': { '$exists': 'true' } , 'label': None }).sort('time',-1).limit(i)#{'keyword': keyword})
        tweets=list()
        for j in query:
                i =  j['data']
                try:
                        sent,main,subt = tool.preText(i['text'])
                        tweet_json = { 'img' : i['user']['profile_image_url'],
                                       'username' : i['user']['name'],
                                       'screen_name' : i['user']['screen_name'],
                                       'text' : i['text'],
                                       'created_at' : j['time'],
                                       'tweet_id' : i['id_str'],
                                       'sent' : sent,
                                       'main' : main,
                                       'subt' : subt
                                       }
                        tweets.append(tweet_json)
                except:
                        print 'twitter data error..'
        return tweets

@csrf_exempt
def i(request):
	context= {
        'title': 'Twitter App - Home',  
	}
	return render(request,'i.html', context)

@csrf_exempt
def improve(request):
        
        date = datetime.now()
        print 'date1: ' ,date
        if request.method == "POST" and request.is_ajax():
                tid = request.POST['id']
                #tid = str(tid)
                print 'tweet_id: ' ,tid
                query = collection.find({'data.id_str': tid }).sort('time',-1)
                tweets=list()
                for j in query:
                    i =  j['data']
                    try:

                        tweet_json = { 'img' : i['user']['profile_image_url'],
                                       'username' : i['user']['name'],
                                       'screen_name' : i['user']['screen_name'],
                                       'text' : i['text'],
                                       'created_at' : j['time'],
                                       'tweet_id' : i['id_str']
                                       }
                        tweets.append(tweet_json)
                    except:
                        print 'twitter data error..'

                t = tweets[0]['created_at']


                query = collection.find({ 'time': { '$gte': t }}).sort('time',-1)

                stream=list()
                for j in query:
                    i =  j['data']
                    if i['id_str'] == tid:
                      continue
                    
                    try:
                        sent,main,subt = tool.preText(i['text'])
                        tweet_json = { 'img' : i['user']['profile_image_url'],
                                       'username' : i['user']['name'],
                                       'screen_name' : i['user']['screen_name'],
                                       'text' : i['text'],
                                       'created_at' : j['time'],
                                       'tweet_id' : i['id_str'],
                                       'sent' : sent,
                                       'main' : main,
                                       'subt' : subt
                                       }
                        stream.append(tweet_json)
                    except:
                            print 'twitter data error..'

                        
                #a = callD(3)
                return render(request,'improve.html',{'tweets':stream})
                

                
                        
                

        else:
                print 'no ID'
                a = callT(50)
                
                return render(request,'improve.html',{'tweets': a})
