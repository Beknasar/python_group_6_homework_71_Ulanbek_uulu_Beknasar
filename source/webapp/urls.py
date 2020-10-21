from django.urls import path, include
from webapp.views import IndexView, ProductView, ProductUpdateView, ProductCreateView, ProductDeleteView, CategoryView, \
    BasketView, OrderCreateView, BasketDeleteOneView, BasketDeleteView, BasketAddView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('product/', include([
        path('<int:pk>/', include ([
            path('', ProductView.as_view(), name='product_view'),
            path('update/', ProductUpdateView.as_view(), name='product_update'),
            path('delete/', ProductDeleteView.as_view(), name='product_delete'),
            path('add-to-basket/', BasketAddView.as_view(), name='product_add_to_basket'),
        ])),

        path('create/', ProductCreateView.as_view(), name='product_create'),
        path('category/<int:pk>/', CategoryView.as_view(), name='product_category'),
    ])),
    path('cart/', include([
        path('<int:pk>/', include([
        path('<delete/', BasketDeleteView.as_view(), name='basket_delete'),
        path('delete-one/', BasketDeleteOneView.as_view(), name='basket_delete_one'),
         ])),
    ])),
    path('basket/', BasketView.as_view(), name='basket_view'),
    path('order/create/', OrderCreateView.as_view(), name='order_create'),
]