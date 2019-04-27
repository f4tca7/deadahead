
from django.forms import ModelForm, Textarea
from .models import ABTestModel

class ABTestForm(ModelForm):
    class Meta:
        model = ABTestModel
        fields = ('var_1_input', 'var_2_input', 'num_permutations',)
        widgets = {
            'var_1_input': Textarea(attrs={'cols': 80, 'rows': 5}),
            'var_2_input': Textarea(attrs={'cols': 80, 'rows': 5}),
            #'num_permutations': Textarea(attrs={'cols': 80, 'rows': 1}),
        }
        labels = {
            "var_1_input": "Variant 1 Data",
            "var_2_input": "Variant 2 Data",
            "num_permutations": "Number of Permutations",
        }