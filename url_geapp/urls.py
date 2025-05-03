from django.urls import path
from . import views

app_name = 'url_geapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('success/<slug:slug>/', views.success, name='success'),
    path('page/<slug:slug>/', views.dynamic_page, name='dynamic_page'),
    path('chat/<slug:slug>/', views.chat, name='chat'),
]