from django import forms
from .models import Product


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")

#
# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['name', 'description', 'category', 'amount', 'price']

