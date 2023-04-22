"""
URL configuration for furniture_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from advuser.views import EmailLoginView
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import never_cache
from django.contrib.staticfiles.views import serve


urlpatterns = [
    path("admin/login/", EmailLoginView.as_view(template_name="advuser/admin-login.html")),
    path("admin/", admin.site.urls),
    path("auth/", include('advuser.urls')),
    path("cart/", include('cart.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path("api/", include('main.urls_api')),
    path('captcha/', include('captcha.urls')),
    path("", include('main.urls')),
]


if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve))) # Запрет на кеширование статики
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)