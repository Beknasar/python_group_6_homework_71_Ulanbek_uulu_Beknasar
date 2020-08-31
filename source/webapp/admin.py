from django.contrib import admin
from webapp.models import Category, Product, Order
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'phone', 'date_create']
    ordering = ['-date_create']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'amount', 'price']
    list_display_links = ('pk', 'name')
    list_filter = ('category',)
    search_fields = ('name',)

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)


