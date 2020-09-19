from django.contrib import admin
from .models import Product, Basket, Order, OrderProduct


class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'amount', 'price')
    list_display_links = ('pk', 'name')
    list_filter = ('category',)
    search_fields = ('name',)


# Бонус
class OrderProductAdmin(admin.TabularInline):
    model = OrderProduct
    fields = ('product', 'amount')
    extra = 0


# Бонус
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'phone', 'date_create')
    list_display_links = ('pk', 'name')
    ordering = ('-date_create',)
    inlines = (OrderProductAdmin,)


admin.site.register(Product, ProductAdmin)
admin.site.register(Basket)
admin.site.register(Order, OrderAdmin)
