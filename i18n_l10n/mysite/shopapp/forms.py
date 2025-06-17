from django import forms
from multiupload.fields import MultiFileField
from shopapp.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount", "preview"

    images = MultiFileField(
        min_num=0,
        max_num=10,
        max_file_size=1024*1024*5,  # 5MB
        required=False
    )
