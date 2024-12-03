from django.urls import path
from . import views

urlpatterns = [
    path('', views.sticky_notes_list, name='sticky_notes_list'),
    path('create/', views.sticky_note_create, name='sticky_note_create'),
    path('edit/<int:pk>/', views.sticky_note_edit, name='sticky_note_edit'),
    path('delete/<int:pk>/', views.sticky_note_delete, name='sticky_note_delete'),
]
