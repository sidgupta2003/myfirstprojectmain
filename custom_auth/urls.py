from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('superadmin_dashboard/', views.superadmin_dashboard_view, name='superadmin_dashboard'),
    path('admin_dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('user_dashboard/', views.user_dashboard_view, name='user_dashboard'),
    path('create-product/', views.create_product, name='create_product'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]