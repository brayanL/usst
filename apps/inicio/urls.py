from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', indexView, name='index'),
    url(r'^login/$', loginView, name='login'),
    url(r'^logout/$', logoutView, name='logout'),
]
