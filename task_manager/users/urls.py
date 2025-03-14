from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserListView.as_view(), name="users_list"),
    path("create/", views.CreateUserView.as_view(), name="create_user"),
    path("<int:pk>/update/", views.UpdateUserView.as_view(), name="update_user"),
    path("<int:pk>/delete/", views.DeleteUserView.as_view(), name="delete_user"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]
