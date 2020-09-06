from django.urls import path
from .views import login, register, logout, dashboard, url_view

urlpatterns = [
        path('login/', login, name='login'),
        path('register/', register, name='register'),
        path('logout/', logout, name='logout'),
        path('dashboard/', dashboard, name='dashboard'),
        path('url_view/<slug:slug>', url_view, name='url_view'),
]
