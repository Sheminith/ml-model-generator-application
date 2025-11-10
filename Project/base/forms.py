from django import forms
from base.models import Dataset

class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['name', 'csv_file', 'target_column']