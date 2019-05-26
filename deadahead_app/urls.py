from django.urls import include, path, re_path
from django.conf.urls import url
from .models import ABTestModel
 
from . import views
app_name = 'deadahead_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('abtesting/', views.abtesting, name='abtesting'),
    path('word2vec/', views.word2vec, name='word2vec'),
    #path('abtesting/?<institution>', views.abtesting, name='abtesting'),
    #path('abtesting/(?P<institution>\\d+)/$', views.abtesting, name="abtesting"),
    path('abtesting/calc_stats/', views.calc_stats, name='calc_stats'),
    path('word2vec/calc_word2vec/', views.calc_word2vec, name='calc_word2vec'),
    path('contact/', views.contact, name='contact'),
]