from django.contrib import admin
from .models import Store, Product

# 1. Quản lý Cửa hàng (Store)
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    # Hiển thị các cột: Tên, Địa chỉ, SĐT, Tọa độ
    list_display = ('name', 'address', 'phone', 'latitude', 'longitude')
    
    # Tạo ô tìm kiếm: Tìm theo tên cửa hàng hoặc địa chỉ
    search_fields = ('name', 'address')

# 2. Quản lý Váy cưới (Product)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Hiển thị: Tên váy, Giá tiền, Thuộc cửa hàng nào
    list_display = ('name', 'price', 'store')
    
    # Tạo bộ lọc bên phải: Giúp lọc váy theo từng Cửa hàng
    list_filter = ('store',)
    
    # Tạo ô tìm kiếm: Giúp tìm nhanh tên váy
    search_fields = ('name',)
    
    # (Tùy chọn) Sắp xếp danh sách theo giá giảm dần (váy đắt nhất lên đầu)
    ordering = ('-price',)