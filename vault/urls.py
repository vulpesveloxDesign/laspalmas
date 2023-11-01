from django.urls import path
from django.views.generic import TemplateView
from .views import contact

app_name = 'vault'

urlpatterns = [
    path('about/', contact, name='about'),
    # path('about/', TemplateView.as_view(template_name='vault/about.html'), name='about'),
    path('articles/run-cmd/', TemplateView.as_view(template_name='vault/articles/run_cmd.html'), name='run-cmd'),
    path('articles/terminal_tricks/', TemplateView.as_view(template_name='vault/articles/linux.html'), name='linux'),
    path('articles/python-0/', TemplateView.as_view(template_name='vault/articles/python_0.html'), name='python-0'),
    ]
