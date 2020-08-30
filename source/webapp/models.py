from django.db import models
from django.core.validators import MinValueValidator


class Order(models.Model):
    products = models.ManyToManyField('webapp.Product', related_name='orders', blank=True, verbose_name='Товары')
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.CharField(max_length=100, verbose_name='Телефон')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')

    def __str__(self):
        return f'{self.name} -- {self.phone}'

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
    product = models.ForeignKey('webapp.Product', related_name='basket', on_delete=models.PROTECT,
                                 verbose_name='Корзина')
    amount = models.IntegerField(verbose_name='Количество в корзине', validators=(MinValueValidator(0),))

    def __str__(self):
        return '{} -- {}'.format(self.product, self.amount)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'