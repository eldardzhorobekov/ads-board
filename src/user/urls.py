from django.urls import path
from .views import SignUpView, LoginView

app_name = 'custom_user'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    # path('ads/', AdminPanel.as_view(), name='ads'),
]