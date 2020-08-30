from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.base import View, TemplateView

from webapp.models import Product, Basket, Category

from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
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



class CategoryView(ListView):
        template_name = 'product_categories.html'

        context_object_name = 'products'

        def get_queryset(self, **kwargs):
            pk = self.kwargs.get('pk')
            return Product.objects.filter(category__pk=pk).order_by('category', 'name')

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


class ProductCreateView(CreateView):
    template_name = 'product_create.html'
    form_class = ProductForm
    model = Product

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    template_name = 'product_delete.html'
    model = Product
    success_url = reverse_lazy('index')


class BasketDeleteView(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        product = get_object_or_404(Product, pk=pk)
        bucket = Basket.objects.get(product__pk=product.pk)
        bucket.delete()
        return redirect('basket_view')


class BasketCountView(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        product = get_object_or_404(Product, pk=pk)
        try:
            basket_product = Basket.objects.get(product__pk=product.pk)
        except Basket.DoesNotExist:
            basket_product = None
        if basket_product:
            if basket_product.amount <= product.amount:
                basket_product.amount += 1
            basket_product.save()
        elif basket_product is None:
            if product.amount > 0:
                basket_product = Basket.objects.create(
                    product=product,
                    amount=1
                )
                basket_product.save()
                print(Basket.objects.all())
        return redirect('index')


class BasketView(TemplateView):
    template_name = 'basket.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total = 0
        for item in Basket.objects.all():
            total += item.product.price * item.amount

        context['basket'] = Basket.objects.all().distinct()
        context['total'] = total
        return context
