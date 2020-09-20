from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum, F, ExpressionWrapper as E


class Order(models.Model):
    products = models.ManyToManyField('webapp.Product', related_name='orders', verbose_name='Товары',
                                      through='webapp.OrderProduct', through_fields=['order', 'product'])
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.CharField(max_length=100, verbose_name='Адрес')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders', null=True)
    def __str__(self):        return f'{self.name} -- {self.phone}'

    def format_time(self):
        return self.date_create.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание')
    category = models.ForeignKey('webapp.Category', related_name='product', on_delete=models.PROTECT, verbose_name='Категория')
    amount = models.IntegerField(verbose_name='Остаток', validators=(MinValueValidator(0),))
    price = models.DecimalField(verbose_name='Цена', max_digits=7, decimal_places=2, validators=(MinValueValidator(0),))

    def __str__(self):
        return f'{self.name} -- {self.amount}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Category(models.Model):
    name = models.CharField(default='1', max_length=20, null=False, blank=False, verbose_name='Название категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Basket(models.Model):
    product = models.ForeignKey('webapp.Product', related_name='basket', on_delete=models.CASCADE,
                                 verbose_name='Корзина')
    amount = models.IntegerField(verbose_name='Количество в корзине', validators=(MinValueValidator(0),))

    def __str__(self):
        return '{} -- {}'.format(self.product.name, self.amount)

    @classmethod
    def get_with_total(cls):
        # запрос, так быстрее
        total_output_field = models.DecimalField(max_digits=10, decimal_places=2)
        total_expr = E(F('amount') * F('product__price'), output_field=total_output_field)
        return cls.objects.annotate(total=total_expr)

    @classmethod
    def get_with_product(cls):
        return cls.get_with_total().select_related('product')

    # @classmethod
    # def get_cart_total(cls):
    #     total = 0
    #     for item in cls.objects.all():
    #         total += item.get_total()
    #     return total

    @classmethod
    def get_basket_total(cls, ids=None):
        # запрос, так быстрее
        basket_products = cls.get_with_total()
        if ids is not None:
            basket_products = basket_products.filter(pk__in=ids)
        total = basket_products.aggregate(basket_total=Sum('total'))
        return total['basket_total']

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class OrderProduct(models.Model):
    product = models.ForeignKey('webapp.Product', related_name='ordering_product', on_delete=models.CASCADE, verbose_name='Продукты в заказах')
    amount = models.IntegerField(verbose_name='Количество заказанных продуктов')
    order = models.ForeignKey('webapp.Order', related_name='product_order', on_delete=models.CASCADE, verbose_name='Заказы продуктов')

    def __str__(self):
        return '{}. {}'.format(self.pk, self.amount)