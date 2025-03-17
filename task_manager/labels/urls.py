from django.urls import path
import .views

app_name = 'labels'

urlpatterns = [
    path("", views.LabelListView.as_view(), name='label_list'),
    path("", views.LabelCreateView.as_view(), name='label_create'),
    path("", views.LabelUpdateView.as_view(), name='label_update'),
    path("", views.LabelDeleteView.as_view(), name='label_delete'),
]