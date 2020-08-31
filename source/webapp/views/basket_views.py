from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.base import View
from webapp.models import Product, Basket, OrderProduct

from django.views.generic import FormView
from webapp.forms import OrderForm


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
        return redirect('index')


class BasketOrderView(FormView):
    template_name = 'baskets/basket.html'
    form_class = OrderForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total = 0
        for item in Basket.objects.all():
            total += item.product.price * item.amount

        context['basket'] = Basket.objects.all().distinct()
        context['total'] = total
        context['form']=OrderForm
        return context

    def form_valid(self, form):
        self.order = form.save()
        for product in Product.objects.all():
            for tovar in Basket.objects.all():
                if product.pk == tovar.product.pk:
                    self.order.products.add(product)

        for tovar in Basket.objects.all():
            product = Product.objects.get(pk=tovar.product.pk)
            product.amount = tovar.product.amount - tovar.amount
            product.save()
            OrderProduct.objects.create(amount=tovar.amount,
                                        order_id=self.order.pk,
                                        product_id=tovar.product.pk)
        Basket.objects.all().delete()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')
