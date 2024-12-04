from django.urls import path

from .views import create_edit_view, detail_view, list_view


urlpatterns = [
    path('create/', create_edit_view, name='create'),
    path('edit/<str:pk>', create_edit_view, name='edit'),
    path('detail/<str:pk>', detail_view, name='detail'),
    path('', list_view, name='list'),
]
