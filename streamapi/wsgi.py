# -*- coding: utf-8 -*-
"""
WSGI config for streamapi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamapi.settings")

application = get_wsgi_application()
from .celery import fetch
from .celery import clear_twitter
print 'finally OK!'
clear_twitter()
keyword = [u'#uob',u'جامعة البحرين',u'#جامعة_البحرين',u'#artsuob',u'#insan_uob',u'#UOB', u'#COBS',u'#enguob',u'#uober',
           u'#uober_life',u'uober',u'#uobers',u'#uob_students',u'#uob_ask',u'‎#uob_تبادل',u'#ask_uob',u'#uob_student',
           u'#uob_info',u'#uob_law',u'#scsuob',u'#uob_library',u'#uobelections',u'#uob_elections',u'‎#uob_ايجابي',
           u'#UOBcouncil',u'#شباب_جامعة_البحرين',u'#uob_arts',u'#uob_exams',u'#uob_exam',u'#uobcouncil',u'طلبة جامعة البحرين']
a = fetch.apply_async(args=[keyword])
print a.task_id
 
