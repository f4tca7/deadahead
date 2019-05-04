from django.urls import include, path, re_path
from django.conf.urls import url
from .models import ABTestModel
 
from . import views
app_name = 'deadahead_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('abtesting/', views.abtesting, name='abtesting'),
    #path('abtesting/?<institution>', views.abtesting, name='abtesting'),
    #path('abtesting/(?P<institution>\\d+)/$', views.abtesting, name="abtesting"),
    path('abtesting/calc_stats/', views.calc_stats, name='calc_stats'),
    path('abtesting/box_swarm_plot/', views.box_swarm_plot, name='box_swarm_plot')
]