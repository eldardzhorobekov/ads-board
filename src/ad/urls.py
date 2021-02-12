from django.contrib import admin
from django.urls import path, include
from ad import views as ads_views

app_name = 'ads'
urlpatterns = [
    path('', ads_views.HomeView.as_view(), name='home'),
    path('<slug:slug>', ads_views.CategoryDetailView.as_view(), name='category'),
    path('ads/<int:pk>/', ads_views.AdvertisementDetailView.as_view(), name='ads-details'),
    path('ads/post/', ads_views.AdvertisementCreateView.as_view(), name='ads-create'),
    path('ads/edit/<int:pk>/', ads_views.AdvertisementUpdateView.as_view(), name='ads-edit'),
    path('myads/', ads_views.UserAdvertisementListView.as_view(), name='ads-user-list')
]