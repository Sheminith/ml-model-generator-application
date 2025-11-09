from django.db import models
from django.core.validators import FileExtensionValidator
from shortuuid.django_fields import ShortUUIDField

class Dataset(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False, length=8)
    name = models.CharField(max_length=100)
    csv_file = models.FileField(upload_to='datasets/', validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    target_column = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class MLModel(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False, length=8)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    model_file = models.FileField(upload_to='models/')
    accuracy = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Model | {self.dataset.name}'