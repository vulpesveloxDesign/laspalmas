from django.urls import path, re_path
from django.conf.urls import include
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
]
