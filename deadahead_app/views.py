from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.utils.http import urlencode

from .models import ABTestModel
from .forms import ABTestForm



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
        var_1 = request.GET.get('var_1', '')
        num_permutations = request.GET.get('num_permutations', '')
        var_2 = request.GET.get('var_2', '')
        form = ABTestForm(initial={'var_1_input': var_1, 'var_2_input': var_2, 'num_permutations': num_permutations, })
    return render(request, 'deadahead_app/abtesting.html', {'form': form})

def hypo_boot(request):
    context = {}
    print(request)
    #return render(request, 'deadahead_app/abtesting.html', context)
    return HttpResponseRedirect(reverse('deadahead_app:abtesting'))