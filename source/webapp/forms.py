from django import forms
from .models import Product, Order, Basket


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'address', 'phone']
        widgets = {'phone': forms.NumberInput}


class BasketAddForm(forms.ModelForm):
    class Meta:
        model = Basket
        # fields = []
        fields = ['amount']  # бонус


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []
        # 'name', 'description', 'category', 'amount', 'price'
