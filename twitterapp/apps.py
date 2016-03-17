# -*- coding: utf-8 -*-
from django.apps import AppConfig


class TwitterappConfig(AppConfig):
    name = 'twitterapp'
    def ready(self):
        print 'test'


        
