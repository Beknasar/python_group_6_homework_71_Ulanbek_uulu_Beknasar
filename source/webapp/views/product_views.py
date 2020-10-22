from django.contrib.auth.mixins import PermissionRequiredMixin
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

    def dispatch(self, request, *args, **kwargs):
        self.test_session_key()
        self.test_session_data()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(amount__gt=0)

    def test_session_data(self):
        if 'check' not in self.request.session:
            self.request.session['check'] = 0
        self.request.session['check'] += 1
        # print(self.request.session['check'])

    def test_session_key(self):
        # print(self.request.session.session_key)
        if not self.request.session.session_key:
            self.request.session.save()


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


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'products/product_update.html'
    form_class = ProductForm
    model = Product
    context_object_name = 'product'
    permission_required = 'webapp.change_product'

    def has_permission(self):
        return super().has_permission()

    def get_queryset(self):
        return super().get_queryset().filter(amount__gt=0)

    def get_success_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.object.pk})


class ProductCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'products/product_create.html'
    form_class = ProductForm
    model = Product
    permission_required = 'webapp.add_product'

    def has_permission(self):
        return super().has_permission()

    def get_success_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.object.pk})


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'products/product_delete.html'
    model = Product
    success_url = reverse_lazy('webapp:index')
    permission_required = 'webapp.delete_product'

    def has_permission(self):
        return super().has_permission()

    def get_queryset(self):
        return super().get_queryset().filter(amount__gt=0)