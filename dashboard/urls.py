from django.urls import path
from . import views
app_name = 'dashboard'
urlpatterns = [ 
    path('', views.dashboard_home, name='home'),
    path('create/', views.create_post, name='create'),
    path('delete/<int:pk>/', views.delete_post, name='delete'),
    path('edit/<int:pk>/', views.edit_post, name='edit'),
]