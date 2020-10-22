from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api_v1.views import get_token_view, ProductViewSet, UserViewSet

app_name = 'api_v1'

router = DefaultRouter()
router.register(r'product', ProductViewSet)
router.register(r'user', UserViewSet)
# router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('get-token/', get_token_view, name='get_token'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
