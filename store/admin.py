from django.contrib import admin
from .models import Store, Product, Booking, ProductImage 
from django.utils import timezone

# 1. Quản lý Ảnh phụ
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
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
    
    # Dòng này phải thụt lề vào trong class BookingAdmin mới đúng bạn nhé!
    formatted_date.short_description = 'Ngày giờ hẹn'