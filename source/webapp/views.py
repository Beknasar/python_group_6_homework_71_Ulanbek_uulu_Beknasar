from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from webapp.models import Product

from django.views.generic import ListView, DetailView, UpdateView
from django.http import HttpResponseNotAllowed
from .forms import SearchForm, ProductForm


class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'products'
    paginate_by = 5
    paginate_orphans = 0
    ordering = ['category', 'name']

    def get_context_data(self, *, object_list=None, **kwargs):
        form = SearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            kwargs['search'] = search
        kwargs['form'] = form
        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self):
        data = Product.objects.all()

        form = SearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            if search:
                data = data.filter(Q(name__icontains=search) | Q(description__icontains=search))
        return data

class ProductView(DetailView):
    template_name = 'product_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        product = get_object_or_404(Product, pk=pk)

        context['product'] = product
        return context

    def get_queryset(self):
        return Product.objects.all()

class ProductUpdateView(UpdateView):
    template_name = 'product_update.html'
    form_class = ProductForm
    model = Product
    context_object_name = 'product'

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})