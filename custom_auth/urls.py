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
    # path('dashboard/', views.dashboard_view, name='dashboard'),
    path('create-user/', views.register_view, name='create_user'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('update-product/<int:product_id>/', views.update_product, name='update_product'),
    path('view-product/<int:product_id>/', views.view_product, name='view_product'),
]