from django.db import models

# Bảng Cửa hàng (Quan trọng để hiện bản đồ)
class Store(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tên cửa hàng")
    address = models.CharField(max_length=500, verbose_name="Địa chỉ")
    phone = models.CharField(max_length=20, verbose_name="Điện thoại")
    
    # Tọa độ GIS (Lấy từ Google Maps)
    latitude = models.FloatField(verbose_name="Vĩ độ (Lat)")
    longitude = models.FloatField(verbose_name="Kinh độ (Lon)")
    
    def __str__(self):
        return self.name

# Bảng Váy cưới (Sản phẩm)
class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name="Thuộc cửa hàng")
    name = models.CharField(max_length=200, verbose_name="Tên váy")
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Giá thuê")
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
# Bảng Đặt lịch hẹn (Booking)
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ duyệt'),
        ('confirmed', 'Đã duyệt'),
        ('done', 'Đã xong'),
        ('cancelled', 'Đã hủy'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Váy muốn thử")
    customer_name = models.CharField(max_length=100, verbose_name="Tên khách")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    booking_date = models.DateTimeField(verbose_name="Ngày giờ hẹn")
    note = models.TextField(blank=True, null=True, verbose_name="Ghi chú thêm")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đặt")

    def __str__(self):
        return f"{self.customer_name} - {self.product.name}"
    
    