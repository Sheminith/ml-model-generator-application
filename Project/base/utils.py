import pandas as pd

def drop_single_val_columns(dataset):
    for column in dataset.columns:
        if dataset[column].nunique() == 1:
            new_dataset = dataset.drop(column, axis=1)
            
    return new_dataset