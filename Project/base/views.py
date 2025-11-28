from django.shortcuts import render, redirect
from base.models import Dataset
from base.forms import DatasetForm
from base.utils import remove_duplicated_cols, remove_empty_or_constant_cols, handle_missing_value_cols, remove_sensitive_cols, fix_data_types
import pandas as pd

def upload_dataset(request):
    if request.method == 'POST':
        form = DatasetForm(request.POST, request.FILES)

        if form.is_valid():
            dataset = form.save()
            return redirect('train_model', pk=dataset.id)
            
    else:
        form = DatasetForm()
    
    context = {'form':form}
    return render(request, 'base/home.html', context)

def train_model(request, pk):
    dataset = Dataset.objects.get(id=pk)
    raw_df = pd.read_csv(dataset.csv_file.path)

    # -------------------- Perform Sampling -------------------- #
    SAMPLING_THRESHOLD = 1_000_000 # one-million
    SAMPLE_FRACTION = 0.1

    use_sample = len(raw_df) > SAMPLING_THRESHOLD # returns True or False

    if use_sample:
        raw_df = raw_df.sample(frac=SAMPLE_FRACTION).copy()

    # ------------ Data Cleaning For Entire Dataset ------------ #
    remove_duplicated_cols(raw_df)
    remove_empty_or_constant_cols(raw_df)
    handle_missing_value_cols(raw_df)
    remove_sensitive_cols(raw_df)
    fix_data_types(raw_df)

    context = {'dataset': dataset}
    return render(request, 'base/train_model_page.html', context)