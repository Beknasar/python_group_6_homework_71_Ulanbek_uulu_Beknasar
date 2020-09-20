from django.urls import path
from django.contrib.auth.views import LoginView
from accounts.views import RegisterView, UserDetailView, UserListView, UserChangeView, UserPasswordChangeView, \
    BasketClearLogoutView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', BasketClearLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='create'),
    path('<int:pk>/', UserDetailView.as_view(), name='detail'),
    path('list/', UserListView.as_view(), name='list'),
    path('<int:pk>/update/', UserChangeView.as_view(), name='change'),
    path('<int:pk>/password_change', UserPasswordChangeView.as_view(), name='password_change'),
]
