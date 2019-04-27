from django.urls import path
 
from . import views
app_name = 'deadahead_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('abtesting/', views.abtesting, name='abtesting'),
    path('hypo_boot/', views.hypo_boot, name='hypo_boot'),
]