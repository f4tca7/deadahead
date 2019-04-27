from django.urls import path
 
from . import views
app_name = 'deadahead_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('abtesting/', views.abtesting, name='abtesting'),
    path('abtesting/calc_stats/', views.calc_stats, name='calc_stats'),
]