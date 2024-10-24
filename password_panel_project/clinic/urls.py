from django.urls import path
from . import views

app_name = 'clinic'

urlpatterns = [
    path('', views.home, name='home'),
    path('manage_passwords/<str:clinic>/', views.manage_passwords, name='manage_passwords'),
    path('display_panel/<str:clinic>/', views.display_panel, name='display_panel'),
    path('get_last_password/<str:clinic>/', views.get_last_password, name='get_last_password'),
    path('call_next_password/<str:clinic>/', views.call_next_password, name='call_next_password'),
    path('get_recent_passwords/<str:clinic>/', views.get_recent_passwords, name='get_recent_passwords'),
]
