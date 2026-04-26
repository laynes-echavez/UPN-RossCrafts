from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('acceso-denegado/', views.access_denied, name='access_denied'),

    # Gestión de usuarios del sistema
    path('usuarios/', views.UserListView.as_view(), name='user_list'),
    path('usuarios/nuevo/', views.UserCreateView.as_view(), name='user_create'),
    path('usuarios/<int:pk>/editar/', views.UserUpdateView.as_view(), name='user_update'),
    path('usuarios/<int:pk>/toggle/', views.user_toggle_active, name='user_toggle'),
    path('usuarios/<int:pk>/password/', views.user_reset_password, name='user_reset_password'),
]
