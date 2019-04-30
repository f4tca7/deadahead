from django.db import models


class ABTestModel(models.Model):
    var_1_input = models.CharField(max_length=10000)
    var_2_input = models.CharField(max_length=10000)
    num_permutations = models.CharField(max_length=200)
    ttest_equal_var = models.BooleanField()
    

