from django.contrib import admin
from django.urls import path, include
from ad.views import HomeView, CategoryDetailView

app_name = 'ads'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<slug:slug>', CategoryDetailView.as_view(), name='category')
]