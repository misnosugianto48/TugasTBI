from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('search_results/', views.results, name='search_results')
]