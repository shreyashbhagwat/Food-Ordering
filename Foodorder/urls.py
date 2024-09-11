"""
URL configuration for Foodorder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from home.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('addcart/<str:pizza_id>/', add_cart, name='addcart'),
    path('', base, name='base'),
    path('cartorder/',order,name='cartorder'),
    path('delete/<uuid:cart_item_uid>/', delete_cart_item, name='delete_cart_item'),
    path('confirmorder/',confrim_order,name='confirmorder'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()