from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

def index(request):
    context = {}
    return render(request, 'deadahead_app/index.html', context)

def abtesting(request):
    context = {}
    return render(request, 'deadahead_app/abtesting.html', context)
