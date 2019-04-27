from django.db import models


class ABTestModel(models.Model):
    var_1_input = models.CharField(max_length=2000)
    var_2_input = models.CharField(max_length=200)
    num_permutations = models.CharField(max_length=200)
