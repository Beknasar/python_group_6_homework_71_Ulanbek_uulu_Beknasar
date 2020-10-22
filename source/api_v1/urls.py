from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api_v1.views import get_token_view, ProductViewSet, UserViewSet, OrderViewSet
    # OrderListView, OrderCreateView


app_name = 'api_v1'

router = DefaultRouter()
router.register(r'product', ProductViewSet)
router.register(r'user', UserViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('get-token/', get_token_view, name='get_token'),
    path('', include(router.urls)),
    # path('order/', include([
    #     path('', OrderListView.as_view(), name='order_list'),
    #     path('create/', OrderCreateView.as_view(), name="order_create"),
    # ])),
]

