import pandas as pd
import numpy as np
from scipy import stats
import re

def chi_sq(data1, data2):
    p_val = -1
    if len(data1) == len(data2):
        z_val, p_val = stats.chisquare(data1, f_exp=data2)
    return p_val

def ttest(data1, data2, equal_var):

    if (len(data1) < 2) | (len(data2) < 2) :
        return -1
    t_stat, p_val = stats.ttest_ind(data1, data2, equal_var = equal_var)
    return p_val

def int_or_else(value, else_value=None):
    """Given a value, returns the value as an int if possible. 
    If not, returns else_value which defaults to None.
    """
    try:
        return int(value)
    # I don't like catch-all excepts, but since objects can raise arbitrary
    # exceptions when executing __int__(), then any exception is
    # possible here, even if only TypeError and ValueError are 
    # really likely.
    except Exception:
        return else_value

def permutation_sample(data1, data2):
    """Generate a permutation sample from two data sets."""

    # Concatenate the data sets: data
    data = np.concatenate((data1, data2))

    # Permute the concatenated array: permuted_data
    permuted_data = np.random.permutation(data)

    # Split the permuted array into two: perm_sample_1, perm_sample_2
    perm_sample_1 = permuted_data[:len(data1)]
    perm_sample_2 = permuted_data[len(data1):]

    return perm_sample_1, perm_sample_2

def draw_perm_reps(data_1, data_2, func, size=1):
    """Generate multiple permutation replicates."""

    # Initialize array of replicates: perm_replicates
    perm_replicates = np.empty(size)

    for i in range(size):
        # Generate permutation sample
        perm_sample_1, perm_sample_2 = permutation_sample(data_1, data_2)

        # Compute the test statistic
        perm_replicates[i] = func(perm_sample_1, perm_sample_2)

    return perm_replicates

def diff_of_means(data_1, data_2):
    """Difference in means of two arrays."""

    # The difference of means of data_1, data_2: diff
    diff = np.mean(data_1) - np.mean(data_2)
    return diff

def calc_bootstrap_hypo_p(data_1, data_2, num_rep):
    # Compute the observed difference in mean inter-no-hitter times: nht_diff_obs
    diff_obs = diff_of_means(data_1, data_2)

    # Acquire 10,000 permutation replicates of difference in mean no-hitter time: perm_replicates
    perm_replicates = draw_perm_reps(data_1, data_2, diff_of_means, num_rep)


    # Compute and print the p-value: p
    p = np.sum(perm_replicates >=  diff_obs) / len(perm_replicates)
    return p


def split_and_convert(str):

    s = pd.Series([str])
    delimiters = " ", ",", ";", "\n"
    regexPattern = '|'.join(map(re.escape, delimiters))
    split_str =  re.split(regexPattern, str)
    num = pd.to_numeric(split_str, errors='coerce')
    num = num[~np.isnan(num)]
    return num

def calc_summary(arr):
    summary = pd.DataFrame(arr).describe(percentiles=[.05, .25, .5, .75, .95])
    return summary

def calc_min_sample_size(data1, data2):
    d1_mean = np.mean(data1)
    d2_mean = np.mean(data2)
    if (d1_mean > 1) & (d2_mean > 1):
        d1_mean = d1_mean / 100.0
        d2_mean = d2_mean / 100.0
    pooled_var_estimator = d1_mean * (1 - d1_mean) + d2_mean * (1 - d2_mean)
    n = (pooled_var_estimator / (d1_mean - d2_mean)**2) * (1.96 + 0.8)**2
    return n