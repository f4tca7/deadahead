from django.db import models
from enum import Enum

class ABTestModel(models.Model):
    var_1_input = models.CharField(max_length=10000)
    var_2_input = models.CharField(max_length=10000)
    num_permutations = models.CharField(max_length=200)
    ttest_equal_var = models.BooleanField()

class Word2VecChoice(Enum):   # A subclass of Enum
    DIST = "Distance"
    N_MOST_SIM = "Similarity"
    

class Word2VecModel(models.Model):
    term_1 = models.CharField(max_length=255)
    term_2 = models.CharField(max_length=255)
    corpus = models.CharField(max_length=255)



