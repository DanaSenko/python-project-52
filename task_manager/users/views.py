from django.shortcuts import render
from django.views import View
from .models import User
from django.views.generic import ListView, CreateView
from django.views.generic.edit import DeleteView, UpdateView
from django.urls import reverse_lazy

# Create your views here.
class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

class CreateUserView(CreateView):
    model = User
    fields = ['username']
    template_name = 'users/create_user.html'
    success_url = reverse_lazy('users_list')

class UpdateUserView(UpdateView):
    pass


class DeleteUserView(DeleteView):
    pass