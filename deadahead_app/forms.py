
from django.forms import ModelForm, Textarea, TextInput, ChoiceField, RadioSelect
from .models import ABTestModel, Word2VecModel, Word2VecChoice

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

CHOICES=[('FB_COMMON','Facebook Common Crawl 600B'),
         ('FB_WIKI','English Wikipedia 2017 16B'),
         ('GOGGLE_NEWS','Google News 100B'),
         ('NYT','New York Times Article Snippets 2000 - 2019 '),
         ]

class Word2VecForm(ModelForm):
    corpus = ChoiceField(choices=CHOICES, widget=RadioSelect(), initial=1)

    class Meta:
        model = Word2VecModel
        fields = ('term_1', 'term_2', 'corpus',)
        widgets = {
            'term_1': TextInput(attrs={'id': 'term_1'}),
            'term_2': TextInput(attrs={'id': 'term_2'}),
        }
        labels = {
            "term_1": "Term 1",
            "term_2": "Term 2",
            "corpus": "Corpus"
        }        