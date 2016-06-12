from django.conf.urls import patterns, url

from outlookmanager import views

urlpatterns = patterns('',
                       url(r'^$', views.home, name='home'),
                       url(r'^home/$', views.home, name='home'),
                       url(r'^gettoken/$', views.gettoken, name='gettoken'),
                       url(r'^mail/$', views.mail, name='mail')
                       )
