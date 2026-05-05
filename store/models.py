from django.db import models
from django.contrib.auth.models import User
# Bảng Cửa hàng
class Store(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tên cửa hàng")
    address = models.CharField(max_length=500, verbose_name="Địa chỉ")
    phone = models.CharField(max_length=20, verbose_name="Điện thoại")
    latitude = models.FloatField(verbose_name="Vĩ độ (Lat)")
    longitude = models.FloatField(verbose_name="Kinh độ (Lon)")
    image = models.ImageField(upload_to='store_images/', null=True, blank=True)
    def __str__(self):
        return self.name

# Bảng Váy cưới (Sản phẩm)
class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name="Thuộc cửa hàng")
    name = models.CharField(max_length=200, verbose_name="Tên váy")
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Giá thuê")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Hình ảnh")
    short_description = models.CharField(max_length=255, blank=True, null=True) 
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả sản phẩm")
    
    STATUS_CHOICES = (
        ('available', 'Sẵn sàng'),
        ('rented', 'Đang thuê'),
        ('washing', 'Đang giặt'),
    )
    
    quantity = models.IntegerField(default=1, verbose_name="Tồn kho")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name="Tình trạng")
    def __str__(self):
        return f"{self.name} ({self.store.name})" 

# Bảng chứa nhiều ảnh cho một sản phẩm
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Sản phẩm")
    image = models.ImageField(upload_to='products/gallery/', verbose_name="Ảnh chi tiết")

    def __str__(self):
        return f"Ảnh của {self.product.name}"
# Bảng Đặt lịch hẹn (Booking)
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ duyệt'),
        ('confirmed', 'Đã duyệt'),
        ('done', 'Đã xong'),
        ('cancelled', 'Đã hủy'),
    ]

    products = models.ManyToManyField(Product, verbose_name="Các váy muốn thử")
    customer_name = models.CharField(max_length=100, verbose_name="Tên khách")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    booking_date = models.DateTimeField(verbose_name="Ngày giờ hẹn")
    note = models.TextField(blank=True, null=True, verbose_name="Ghi chú thêm")
    address = models.CharField(max_length=500, blank=True, null=True, verbose_name="Địa chỉ giao váy")
    latitude = models.FloatField(blank=True, null=True, verbose_name="Vĩ độ (Lat)")
    longitude = models.FloatField(blank=True, null=True, verbose_name="Kinh độ (Lon)")
    shipping_fee = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Phí ship")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đặt")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Tài khoản đặt")

    def __str__(self):
        return f"{self.customer_name} - {self.product.name} ({self.booking_date.strftime('%H:%M %d/%m')})"
    
# Bảng lưu nội dung chính của trang Giới Thiệu
class AboutUsContent(models.Model):
    # Phần Mở Đầu
    main_title = models.CharField(max_length=255, default="Câu Chuyện Của Chúng Tôi", verbose_name="Tiêu đề chính")
    slogan = models.CharField(max_length=500, default="Nơi những giấc mơ lấp lánh hóa thành hiện thực...", verbose_name="Slogan")
    
    # Phần 1: Khởi Nguồn
    origin_title = models.CharField(max_length=255, default="Khởi Nguồn Của Cái Đẹp", verbose_name="Tiêu đề Khởi Nguồn")
    origin_content = models.TextField(verbose_name="Nội dung Khởi Nguồn")
    origin_image = models.ImageField(upload_to='about_images/', null=True, blank=True, verbose_name="Ảnh cô dâu")
    
    # Phần 2: Cảm Xúc Giao Thoa Công Nghệ
    tech_title = models.CharField(max_length=255, default="Cảm Xúc Giao Thoa Công Nghệ", verbose_name="Tiêu đề Công Nghệ")
    tech_content = models.TextField(verbose_name="Nội dung phần GIS")
    tech_image = models.ImageField(upload_to='about_images/', null=True, blank=True, verbose_name="Ảnh bản đồ")
    tech_quote = models.CharField(max_length=500, blank=True, null=True, verbose_name="Câu Quote")

    class Meta:
        verbose_name = "Nội dung trang giới thiệu"
        verbose_name_plural = "Nội dung trang giới thiệu"

    def __str__(self):
        return "Cấu hình trang Giới Thiệu"

# Bảng lưu các thẻ Tiêu chí (Tại sao chọn chúng tôi)
class AboutFeature(models.Model):
    icon_image = models.ImageField(upload_to='about_icons/', null=True, blank=True, verbose_name="Icon")
    title = models.CharField(max_length=100, verbose_name="Tiêu đề thẻ")
    description = models.TextField(verbose_name="Mô tả chi tiết")
    
    class Meta:
        verbose_name = "Tiêu chí nổi bật"
        verbose_name_plural = "Các tiêu chí nổi bật"

    def __str__(self):
        return self.title