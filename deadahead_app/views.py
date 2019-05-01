from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.utils.http import urlencode
import pandas as pd
import json 
from .models import ABTestModel
from .forms import ABTestForm
from .utils import split_and_convert
from .utils import calc_summary
from .utils import int_or_else
from .utils import calc_bootstrap_hypo_p
from .utils import ttest
from .utils import chi_sq
from .plot_helpers import plot_box_swarm
from .plot_helpers import plot_hist

def index(request):
    context = {}
    return render(request, 'deadahead_app/index.html', context)

def abtesting(request):    
    var_1 = request.GET.get('var_1', '1.1,.6,6.8')
    var_2 = request.GET.get('var_2', '1,2.3,3')
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
                hypo_p = calc_bootstrap_hypo_p(var_1_split, var_2_split, num_permutations_num)
                num_permutations = num_permutations_num

            ttest_p = ttest(var_1_split, var_2_split, False)

            response_data['hypo_p'] = hypo_p
            response_data['num_perm'] = num_permutations
            response_data['ttest_p'] = ttest_p
            response_data['equal_var'] = abtest_request.ttest_equal_var
            response_data['chi_sq_p'] = chi_sq(var_1_split, var_2_split)

            boxplot_img = plot_box_swarm(var_1_split, var_2_split)
            response_data['boxplot_img'] = boxplot_img
            
            hist_img = plot_hist(var_1_split, var_2_split)                
            
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


def box_swarm_plot(request):                
    return HttpResponse(
        json.dumps({"nothing to see": "this isn't happening"}),
        content_type="application/json"
    )    