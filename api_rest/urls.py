from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('user/', views.get_users, name='get_all_users'),
    path('user/<int:id>', views.get_by_id),
    path('user/create', views.post_create_user),
    path('user/update/<int:id>', views.put_edit_user),
    path('user/delete/<int:id>', views.delete_user),
]