from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.utils.http import urlencode
import pandas as pd
import numpy as np
import json 
from .models import ABTestModel
from .forms import ABTestForm
from .utils import split_and_convert
from .utils import calc_summary
from .utils import int_or_else
from .utils import calc_bootstrap_hypo_p
from .utils import ttest
from .utils import chi_sq
from .utils import calc_min_sample_size
from .plot_helpers import plot_box_swarm
from .plot_helpers import plot_hist

DEFAULT_VAR_A = [13.71, 14.57, 12.07, 14.41, 15.11, 14.5, 14.21, 14.15, 13.85, 13.54, 14.24, 14.52, 13.99, 14.28, 13.74, 14.04, 14.47, 13.87, 14.25, 15.42, 13.28, 12.82, 13.84, 13.83, 14.54, 14.63, 13.35, 14.37, 14.63, 14.43]
DEFAULT_VAR_B = [13.82, 13.33, 11.74, 14.19, 14.84, 14.18, 12.43, 13.69, 12.75, 13.51, 13.7, 13.6, 13.87, 13.02, 14.48, 13.78, 13.29, 13.9, 14.51, 13.21, 13.66, 13.52, 13.45, 12.88, 14.81, 14.82, 12.98, 12.94, 13.37, 15.14]

def index(request):
    context = {}
    return render(request, 'deadahead_app/index.html', context)

def contact(request):
    context = {}
    return render(request, 'deadahead_app/contact.html', context)

def abtesting(request):    
    var_1 = request.GET.get('var_1', ', '.join(str(x) for x in DEFAULT_VAR_A))
    var_2 = request.GET.get('var_2', ', '.join(str(x) for x in DEFAULT_VAR_B))

    ttest_equal_var = request.GET.get('ttest_equal_var', 'true')
    num_permutations = request.GET.get('num_permutations', '100')
    form = ABTestForm(initial={'var_1_input': var_1, 'var_2_input': var_2, 'num_permutations': num_permutations, 'ttest_equal_var': ttest_equal_var, })
    var_1_split = split_and_convert(var_1)
    var_2_split = split_and_convert(var_2)

    var_1_summary = calc_summary(var_1_split)
    var_2_summary = calc_summary(var_2_split)
    var_1_json = var_1_summary.to_dict(orient='split')
    var_2_json = var_2_summary.to_dict(orient='split')
    stats_summary = zip(var_1_json["index"], var_1_json["data"], var_2_json["data"])

    print(stats_summary)
    
    return render(request, 'deadahead_app/abtesting.html', {'form': form, 'stats_summary': stats_summary})

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

            var_1_summary = calc_summary(var_1_split).to_json(orient='split')
            var_2_summary = calc_summary(var_2_split).to_json(orient='split')
            response_data = {}

            response_data['var_1'] = ', '.join(str(x) for x in var_1_split)
            response_data['var_2'] = ', '.join(str(x) for x in var_2_split)

            response_data['var_1_summary'] = var_1_summary
            response_data['var_2_summary'] = var_2_summary
            hypo_p = 0.0
            num_permutations_num = int_or_else(num_permutations)
            if num_permutations_num != None:
                if num_permutations_num > 5000 :
                    num_permutations_num = 5000
                if num_permutations_num < 1:
                    num_permutations_num = 100
                hypo_p = calc_bootstrap_hypo_p(var_1_split, var_2_split, num_permutations_num)
                num_permutations = num_permutations_num

            ttest_p = ttest(var_1_split, var_2_split, False)
            min_sample_size = calc_min_sample_size(var_1_split, var_2_split)
            chi_squared = chi_sq(var_1_split, var_2_split)
            if np.isnan(ttest_p):
                ttest_p = -1
            if np.isnan(min_sample_size):
                min_sample_size = -1    
            if np.isnan(hypo_p):
                hypo_p = -1        
            if np.isnan(chi_squared):
                chi_squared = -1  
            response_data['hypo_p'] = hypo_p
            response_data['num_perm'] = num_permutations
            response_data['ttest_p'] = ttest_p
            response_data['equal_var'] = abtest_request.ttest_equal_var
            response_data['chi_sq_p'] = chi_squared

            boxplot_img = plot_box_swarm(var_1_split, var_2_split)
            response_data['boxplot_img'] = boxplot_img
            
            hist_img = plot_hist(var_1_split, var_2_split)                
            response_data['min_sample_size'] = min_sample_size
            response_data['hist_img'] = hist_img
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
