from django.urls import path

from .views import create_edit_view, detail_view, my_list_view


urlpatterns = [
    path('create/', create_edit_view, name='create'),
    path('edit/<str:pk>', create_edit_view, name='edit'),
    path('detail/<str:pk>', detail_view, name='detail'),
    path('my-list/', my_list_view, name='my-list'),
]
