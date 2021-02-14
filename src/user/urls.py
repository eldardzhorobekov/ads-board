from django.urls import path
from .views import SignUpView, LoginView, UserDetails

app_name = 'custom_user'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/<int:pk>', UserDetails.as_view(), name='details'),
    # path('ads/', AdminPanel.as_view(), name='ads'),
]