from django.urls import path
from .views import UserListView, CreateUserView

urlpatterns = [
    path('', UserListView.as_view(), name='users_list'),
    path('create/', CreateUserView.as_view(), name='create_user'),
]