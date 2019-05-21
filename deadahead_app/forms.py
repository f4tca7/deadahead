
from django.forms import ModelForm, Textarea, TextInput
from .models import ABTestModel

class ABTestForm(ModelForm):
    class Meta:
        model = ABTestModel
        fields = ('var_1_input', 'var_2_input', 'num_permutations','ttest_equal_var',)
        widgets = {
            'var_1_input': Textarea(attrs={'cols': 80, 'rows': 5, 'id': 'var_1_input'}),
            'var_2_input': Textarea(attrs={'cols': 80, 'rows': 5, 'id': 'var_2_input'}),
            'num_permutations': TextInput(attrs={'id': 'num_permutations'}),
        }
        labels = {
            "var_1_input": "Control",
            "var_2_input": "Treatment",
            "num_permutations": "Number of permutations for bootstrap hypothesis test",
            "ttest_equal_var": "For t-test: Equal variance?"
        }