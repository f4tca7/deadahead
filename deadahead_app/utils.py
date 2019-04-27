import pandas as pd
import numpy as np
import re

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