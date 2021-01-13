from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
# from django.contrib.auth.views import logout

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('users/', include('user.urls')),
    path('auth/', include('django.contrib.auth.urls'), name='django-auth'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
