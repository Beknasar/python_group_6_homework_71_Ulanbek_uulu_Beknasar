from django import forms
from .models import Product, Order


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'address', 'phone']
        widgets = {'phone': forms.NumberInput, 'address': forms.EmailInput}


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'amount', 'price']

