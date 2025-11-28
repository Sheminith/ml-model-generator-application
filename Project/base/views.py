from django.shortcuts import render, redirect
from base.models import Dataset
from base.forms import DatasetForm
from base.utils import perform_sampling, remove_duplicated_cols, remove_empty_or_constant_cols, handle_missing_value_cols, remove_sensitive_cols, fix_data_types, train_val_test_split

import pandas as pd
import numpy as np

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

    raw_df = perform_sampling(raw_df, SAMPLING_THRESHOLD, SAMPLE_FRACTION)

    # ------------ Data Cleaning For Entire Dataset ------------ #
    raw_df = remove_duplicated_cols(raw_df)
    raw_df = remove_empty_or_constant_cols(raw_df)
    raw_df = handle_missing_value_cols(raw_df)
    raw_df = remove_sensitive_cols(raw_df)
    raw_df = fix_data_types(raw_df)

    # ------------ Train, Validation, and Test sets ------------ #
    train_df, val_df, test_df = train_val_test_split(dataset=raw_df, test_size=0.2, val_size=0.25)

    # ------------ Identify Input & Target columns ------------- #
    target_col = dataset.target_column
    input_cols = [col for col in raw_df.columns if col != target_col]

    # To train the model
    train_inputs = train_df[input_cols].copy()
    train_targets = train_df[target_col].copy()

    # To validate the model
    val_inputs = val_df[input_cols].copy()
    val_targets = val_df[target_col].copy()

    # To test the model
    test_inputs = test_df[input_cols].copy()
    test_targets = test_df[target_col].copy()

    # ---------- Identify Numerical & Categorical data --------- #
    numeric_cols = train_inputs.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = train_inputs.select_dtypes('object').columns.tolist()

    context = {'dataset':dataset, 'numeric_cols':numeric_cols, 'categorical_cols':categorical_cols}
    return render(request, 'base/train_model_page.html', context)