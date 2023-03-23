from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MatrixAForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in range(3):
            for j in range(3):
                self.fields[f'matrix_a_{i}{j}'] = forms.FloatField(label=f"A{i+1}{j+1}")

class MatrixBForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in range(3):
            for j in range(3):
                self.fields[f'matrix_b_{i}{j}'] = forms.FloatField(label=f"B{i+1}{j+1}", required=False)

class MatrixAnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in range(3):
            for j in range(3):
                self.fields[f'matrix_b_{i}{j}'] = forms.FloatField(label=f"B{i+1}{j+1}")

        

