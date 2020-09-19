from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy

from webapp.models import Product, Category
from .base_views import SearchView
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from webapp.forms import SearchForm, ProductForm


class IndexView(SearchView):
    model = Product
    template_name = 'products/index.html'
    ordering = ['category', 'name']
    search_fields = ['name__icontains']
    paginate_by = 5
    context_object_name = 'products'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        data = Category.objects.all()
        context['categories'] = data
        return context

    def get_queryset(self):
        return super().get_queryset().filter(amount__gt=0)


class CategoryView(ListView):
    template_name = 'products/product_categories.html'
    context_object_name = 'products'

    def get_queryset(self, **kwargs):
        pk = self.kwargs.get('pk')
        return Product.objects.filter(category__pk=pk).order_by('category', 'name')


class ProductView(DetailView):
    model = Product
    template_name = 'products/product_view.html'

    # чтоб товары, которых не осталось нельзя было и просмотреть
    # это можно добавить вместо model = Product в Detail, Update и Delete View.
    def get_queryset(self):
        return super().get_queryset().filter(amount__gt=0)


class ProductUpdateView(UpdateView):
    template_name = 'products/product_update.html'
    form_class = ProductForm
    model = Product
    context_object_name = 'product'

    def get_queryset(self):
        return super().get_queryset().filter(amount__gt=0)

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class ProductCreateView(CreateView):
    template_name = 'products/product_create.html'
    form_class = ProductForm
    model = Product

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    template_name = 'products/product_delete.html'
    model = Product
    success_url = reverse_lazy('index')

    def get_queryset(self):
        return super().get_queryset().filter(amount__gt=0)