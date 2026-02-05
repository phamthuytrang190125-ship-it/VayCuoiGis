"""
URL configuration for vaycuoigis project.

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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from store import views

urlpatterns = [
    # Admin 
    path('admin/', admin.site.urls),
    #Trang chính
    path('', views.home_shop, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    #Cửa hàng & Sản phẩm 
    path('stores/', views.store_list, name='store_list'),
    path('stores/<int:store_id>/', views.store_detail_view, name='store_detail_view'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    #Bản đồ & Tính phí
    path('map/', views.map_view, name='map_view'),
    path('api/shipping-fee/', views.api_calculate_shipping, name='api_shipping'),
]

# Cấu hình phục vụ file Media (Ảnh upload)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)