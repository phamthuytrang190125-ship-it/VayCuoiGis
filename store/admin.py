from django.contrib import admin
from .models import Store, Product, Booking, ProductImage 
from django.utils import timezone

# 1. Quản lý Ảnh phụ (Hiện theo dạng hàng ngang trong trang Product)
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3 # Hiện sẵn 3 ô trống để chọn ảnh cho nhanh
    verbose_name = "Ảnh chi tiết"

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'latitude', 'longitude')
    search_fields = ('name', 'address')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'store', 'description_short')
    list_filter = ('store',)
    search_fields = ('name',)
    ordering = ('-price',)
    
    # Hiện chỗ upload nhiều ảnh cùng lúc trong trang chỉnh sửa sản phẩm
    inlines = [ProductImageInline]

    def description_short(self, obj):
        return obj.description[:50] + "..." if obj.description else "Không có mô tả"
    description_short.short_description = 'Mô tả ngắn'

# 3. Quản lý đặt lịch (Booking)
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'phone', 'product', 'get_store', 'formatted_date', 'status')
    list_filter = ('status', 'booking_date')
    search_fields = ('customer_name', 'phone')
    list_editable = ('status',)

    def get_store(self, obj):
        return obj.product.store.name
    get_store.short_description = 'Tiệm'

    def formatted_date(self, obj):
        if obj.booking_date:
            return obj.booking_date.strftime("%H:%M - %d/%m/%Y")
        return "Chưa chọn ngày"
    formatted_date.short_description = 'Ngày giờ hẹn'