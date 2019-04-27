from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.utils.http import urlencode
import json 
from .models import ABTestModel
from .forms import ABTestForm
from .utils import split_and_convert


def index(request):
    context = {}
    return render(request, 'deadahead_app/index.html', context)

def abtesting(request):
    
    if request.method == "POST":        
        form = ABTestForm(request.POST)
        if form.is_valid():
            abtest_request = form.save(commit=False)
            var_1 = abtest_request.var_1_input
            var_2 = abtest_request.var_2_input
            num_permutations = abtest_request.num_permutations
            
            print(abtest_request.var_1_input)

            query_kwargs={'var_1':var_1, 'var_2':var_2, 'num_permutations':num_permutations,}
            base_url = reverse('deadahead_app:abtesting')
            url = '{}?{}'.format(base_url, urlencode(query_kwargs))
            return HttpResponseRedirect(url)
        else:
            return render(request, 'deadahead_app/abtesting.html', {'form': form, 'error_message': "You didn't select a choice.",})
    else:
        var_1 = request.GET.get('var_1', '')
        num_permutations = 10000
        var_2 = request.GET.get('var_2', '')
        form = ABTestForm(initial={'var_1_input': var_1, 'var_2_input': var_2, 'num_permutations': num_permutations, })
    return render(request, 'deadahead_app/abtesting.html', {'form': form})

def calc_stats(request):
    if request.method == 'POST':
        form = ABTestForm(request.POST)
        if form.is_valid():
            abtest_request = form.save(commit=False)
            var_1 = abtest_request.var_1_input
            var_2 = abtest_request.var_2_input
            num_permutations = abtest_request.num_permutations
            var_1_split = split_and_convert(var_1)
            var_2_split = split_and_convert(var_2)
            response_data = {}
            response_data['result'] = 'Create post successful!'
            response_data['var_1'] = ', '.join(str(x) for x in var_1_split)
            response_data['var_2'] = ', '.join(str(x) for x in var_2_split)
            
            print(var_1_split)
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            errors = form.errors
            
            return HttpResponse(
                json.dumps(errors),
                content_type="application/json",
                status=500
            )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )