from django.contrib import admin
from webapp.models import Category, Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'amount', 'price']
    list_display_links = ('pk', 'name')
    list_filter = ('category',)
    search_fields = ('name',)

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
