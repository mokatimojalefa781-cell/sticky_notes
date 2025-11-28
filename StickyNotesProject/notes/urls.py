from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_note, name='add-note'),
    path('edit/<int:id>/', views.edit_note, name='edit-note'),
    path('delete/<int:id>/', views.delete_note, name='delete-note'),
]
