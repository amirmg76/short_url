from django.urls import path
from .views import firstPage, site_redirection


urlpatterns = [
        path('', firstPage, name='first_page'),
        path('link/<slug:slug>/', site_redirection, name='site_redirection'),
]
