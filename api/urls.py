from django.urls import path
from api import views


urlpatterns = [
    path('home/cached/', views.home_cached, name='home_cached'),
    path('home/cacheless/', views.home_cacheless, name='home_cacheless'),
    path('cache_books/', views.cache_books, name='cache_books'),
    path('generate_fake_books/', views.generate_fake_books, name='generate_fake_books'),
]