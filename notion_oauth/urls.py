from django.urls import path

from . import views

app_name = 'notion_oauth'

urlpatterns = [
    path('', views.notion_auth_start, name='notion_auth_start'),
    path('redirect/', views.notion_redirect, name='notion_redirect'),
]