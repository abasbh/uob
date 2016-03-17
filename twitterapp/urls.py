from django.conf.urls import url
from django.conf import settings
from . import views
from . import tasks


urlpatterns = [
	
	url(r'^$', views.index, name='index'),
        url(r'^improve/$', views.i, name='improve'),
	#url(r'^fetch/$', tasks.fetch, name='fetch'),
	url(r'^i/$', views.improve, name='improve'),
        url(r'^data/$', views.data, name='data'),
        url(r'^label/$', views.label, name='label'),
	url(r'^streamapi/(?P<keyword>\w+)$', views.query, name='query'),
]
