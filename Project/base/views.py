from django.shortcuts import render, redirect
from base.models import Dataset
from base.forms import DatasetForm
from base.utils import drop_single_val_columns
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

    # Take the dataset and remove unnecessary columns
    raw_df = pd.read_csv(dataset.csv_file.path)

    # stopped here
    context = {'dataset': dataset}
    return render(request, 'base/train_model_page.html', context)