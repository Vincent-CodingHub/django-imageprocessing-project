from unicodedata import name
from django.conf.urls import url
from main_app import views

# TEMPLATE TAGGING
app_name = 'main_app'

urlpatterns = [
  url(r'^information/$', views.information, name='information'),
  url(r'predictImage/$', views.predictImage, name='predictImage'),
]