from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Store, Product, Booking, ProductImage
from django.contrib import messages
import json
import math
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.core.mail import send_mail

# Tính khoảng cách 
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    try:
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + \
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
            math.sin(dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return round(R * c, 2)
    except:
        return 0

def calculate_fee_logic(distance_km):
    if distance_km < 5: return 0
    elif 5 <= distance_km <= 10: return distance_km * 5000
    else: return distance_km * 10000

# 1. Trang chủ 
# 1. Trang chủ (ĐÃ BỔ SUNG TÍNH NĂNG TÌM KIẾM VÀ LỌC GIÁ)
def home_shop(request):
    # Lấy toàn bộ váy cưới (sắp xếp mới nhất)
    products_list = Product.objects.all().order_by('-id') 
    
    # === BẮT ĐẦU: XỬ LÝ LỌC TÌM KIẾM ===
    query = request.GET.get('q')
    price_range = request.GET.get('price_range')

    # Lọc theo tên (nếu có gõ chữ)
    if query:
        products_list = products_list.filter(name__icontains=query)

    # Lọc theo giá (nếu có chọn khoảng giá)
    if price_range == 'under_5':
        products_list = products_list.filter(price__lt=5000000)
    elif price_range == '5_to_10':
        products_list = products_list.filter(price__gte=5000000, price__lte=10000000)
    elif price_range == 'over_10':
        products_list = products_list.filter(price__gt=10000000)
    # === KẾT THÚC: XỬ LÝ LỌC TÌM KIẾM ===

    # Giữ nguyên code chia trang của bạn
    paginator = Paginator(products_list, 4) # Lưu ý: Bạn đang để 4 váy/trang. Nếu muốn hiển thị 16 váy/trang như thiết kế giao diện thì đổi số 4 thành 16 nha.
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html')

# 2. Trang bản đồ 
def map_view(request):
    products = Product.objects.all()
    stores = Store.objects.all()
    user_lat = 10.7721 
    user_lon = 106.6983
    is_default = True  
    
    if request.method == 'POST':
        try:
            lat_str = str(request.POST.get('lat', '')).replace(',', '.')
            lon_str = str(request.POST.get('lon', '')).replace(',', '.')
            
            user_lat = float(lat_str)
            user_lon = float(lon_str)
            is_default = False 
        except (ValueError, TypeError):
            pass 

    store_list = []
    for s in stores:
        if not is_default:
            dist = haversine_distance(user_lat, user_lon, s.latitude, s.longitude)
            fee = calculate_fee_logic(dist)
            formatted_fee = "{:,.0f} đ".format(fee).replace(",", ".") if fee > 0 else "Miễn phí"
        else:
            dist = 0
            fee = 0
            formatted_fee = "---" 
        store_list.append({
            'id': s.id,
            'name': s.name, 'address': s.address, 'phone': s.phone,
            'lat': s.latitude, 'lon': s.longitude, 'distance': dist,
            'fee': fee, 'formatted_fee': formatted_fee,
            'image': s.image.url if s.image else 'https://dummyimage.com/400x150/fff0f3/d88a9a&text=Bridal+Luxury'        })
    
    if not is_default:
        store_list.sort(key=lambda x: x['distance'])
        
    stores_json = json.dumps(store_list)
    
    return render(request, 'map.html', {
        'stores_json': stores_json, 'stores': store_list,
        'products': products, 'user_lat': user_lat, 'user_lon': user_lon,
        'is_default': is_default 
    })

# 3. Trang chi tiết sản phẩm 
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, "Vui lòng đăng nhập để hệ thống giữ chỗ thử váy cho bạn nhé!")
            return redirect('login')
        name = request.POST.get('customer_name')
        phone_input = request.POST.get('phone_number') 
        date = request.POST.get('booking_date')
        note = request.POST.get('note')

        if name and phone_input and date:
            Booking.objects.create(
                product=product, customer_name=name, phone=phone_input,  
                booking_date=date, note=note
            )
            #Mailtrap
            tieu_de = f"[Bridal Luxury] Có khách đặt lịch: {name}"
            noi_dung = f"Hệ thống vừa nhận 1 đơn đặt lịch mới:\n\n- Khách hàng: {name}\n- Số điện thoại: {phone_input}\n- Ngày hẹn: {date}\n- Váy muốn thử: {product.name}\n- Ghi chú: {note}\n\nVui lòng vào trang Quản lý để duyệt đơn!"
            
            send_mail(
                subject=tieu_de,
                message=noi_dung,
                from_email='hethong@bridalluxury.com', # Mail ảo của hệ thống
                recipient_list=['admin_test@gmail.com'], # Mail ảo người nhận
                fail_silently=False,
            )
            messages.success(request, f"✨ Chúc mừng {name}! Đã đặt lịch tại {product.store.name}.")
            return redirect('product_detail', product_id=product.id)
        else:
            messages.error(request, "Vui lòng điền đầy đủ thông tin.")

    return render(request, 'product_detail.html', {'product': product})

# 4. API tính phí  
def api_calculate_shipping(request):
    store_id = request.GET.get('store_id')
    user_lat = request.GET.get('lat')
    user_lon = request.GET.get('lon')
    if not store_id or not user_lat: return JsonResponse({'error': 'Thiếu dữ liệu'}, status=400)
    try:
        store = Store.objects.get(pk=store_id)
        dist = haversine_distance(store.latitude, store.longitude, float(user_lat), float(user_lon))
        fee = calculate_fee_logic(dist)
        return JsonResponse({'store': store.name, 'distance_km': dist, 'shipping_fee': fee, 'formatted_fee': "{:,.0f}".format(fee).replace(",", ".")})
    except: return JsonResponse({'error': 'Lỗi'}, status=400)

# 5. Hệ thống cửa hàng

# Danh sách tất cả cửa hàng (Đã thêm phân trang và sắp xếp)
def store_list(request):
    # Lấy danh sách cửa hàng, sắp xếp theo ID giảm dần (mới nhất lên đầu)
    store_queryset = Store.objects.all().order_by('-id')
    
    # Chia trang: 6 cửa hàng trên mỗi trang (bạn có thể đổi thành 9 hoặc 12 tùy ý)
    paginator = Paginator(store_queryset, 6) 
    page_number = request.GET.get('page')
    stores = paginator.get_page(page_number)
    
    return render(request, 'store_list.html', {'stores': stores})

# Chi tiết các váy tại cửa hàng (Có sắp xếp sản phẩm mới nhất)
def store_detail_view(request, store_id):
    # Lấy thông tin cửa hàng, nếu không có trả về 404
    store = get_object_or_404(Store, pk=store_id)
    
    # Lấy danh sách sản phẩm thuộc cửa hàng này, ưu tiên mẫu mới nhất
    products = Product.objects.filter(store=store).order_by('-id')
    
    # Nếu cửa hàng có quá nhiều váy, bạn cũng có thể cân nhắc thêm Paginator ở đây
    # Hiện tại tui giữ nguyên danh sách sản phẩm để khách xem hết một lượt
    
    return render(request, 'store_detail_view.html', {
        'store': store, 
        'products': products
    })
# 6. Trang liên hệ 
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        send_mail(
            subject=f"[Liên hệ mới] Khách hàng: {name}",
            message=f"Bạn vừa nhận được một yêu cầu liên hệ từ khách hàng tên là {name}. Vui lòng kiểm tra lại hệ thống/hộp thư nhé.",
            from_email='hethong@bridalluxury.com',
            recipient_list=['admin_test@gmail.com'],
            fail_silently=False,
        )
        messages.success(request, f"Cảm ơn {name}! Chúng tôi đã nhận được tin nhắn và sẽ phản hồi sớm nhất.")
        return redirect('contact')
    return render(request, 'contact.html')

#7. Chức năng tài khoản 
#đăng ký 
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            login(request, user) 
            messages.success(request, f"Chào mừng {user.username}! Bạn đã đăng ký thành công.")
            return redirect('home') 
    else:
        form = UserCreationForm()
    form.fields['username'].help_text = "Nhập tên tài khoản viết liền không dấu (VD: thuytrang123)"
    return render(request, 'register.html', {'form': form})

#8. Trang quản lý shop 
def custom_manager(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, "Cảnh báo: Bạn không có quyền truy cập trang quản trị!")
        return redirect('home')
    #Lấy ds từ database 
    bookings = Booking.objects.all().order_by('-id') 
    products = Product.objects.all().order_by('-id') 
    stores = Store.objects.all().order_by('-id')     

    context = {
        'bookings': bookings,
        'products': products,  
        'stores': stores,      
        'total_bookings': bookings.count(),
        'total_products': products.count(),
        'total_stores': stores.count(),
    }
    return render(request, 'manager.html', context)

#8.1 Hàm Xóa Đơn Đặt Lịch
def delete_booking(request, id):
    if request.user.is_staff:
        Booking.objects.filter(id=id).delete()
        messages.success(request, "Đã xóa đơn đặt lịch thành công!")
    return redirect('custom_manager')

#8.2 Hàm Sửa Đơn Đặt Lịch 
def edit_booking(request, id):
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, "Cảnh báo: Bạn không có quyền!")
        return redirect('home')
    #lấy đơn cần sửa 
    booking = get_object_or_404(Booking, pk=id)
    if request.method == 'POST':
        booking.customer_name = request.POST.get('customer_name')
        booking.phone = request.POST.get('phone')
        booking.note = request.POST.get('note', '')
        booking.status = request.POST.get('status') 
        booking.save() 
        messages.success(request, f"Đã cập nhật trạng thái đơn của {booking.customer_name}!")
        return redirect('custom_manager')

    return render(request, 'edit_booking.html', {'booking': booking})

#8.3 Hàm Xóa Váy Cưới
def delete_product(request, id):
    if request.user.is_staff:
        Product.objects.filter(id=id).delete()
        messages.success(request, "Đã xóa váy cưới khỏi hệ thống!")
    return redirect('custom_manager')

#8.4 Hàm Thêm Váy Cưới Mới
def add_product(request):
    if request.method == 'POST' and request.user.is_staff:
        name = request.POST.get('name')
        price = request.POST.get('price')
        store_id = request.POST.get('store')
        description = request.POST.get('description', '') 
        image = request.FILES.get('image') # Lấy ảnh chính
        quantity = request.POST.get('quantity', 1) 
        status = request.POST.get('status', 'available')
        
        try:
            store = Store.objects.get(pk=store_id)
            
            # 1. Tạo váy cưới và gán vào biến 'product' thay vì chỉ create trống
            product = Product.objects.create(
                name=name, price=price, store=store, description=description, image=image,
                quantity=quantity, status=status 
            )
            
            # 2. lưu nhìu ảnh phụ chi tiết 
            extra_images = request.FILES.getlist('extra_images')
            if extra_images: 
                for img in extra_images:
                    ProductImage.objects.create(product=product, image=img)
            
            messages.success(request, f"Đã thêm váy cưới '{name}' và ảnh chi tiết thành công!")
        except Store.DoesNotExist:
            messages.error(request, "Lỗi: Không tìm thấy cửa hàng này!")
        except Exception as e:
            messages.error(request, f"Lỗi hệ thống khi lưu ảnh: {str(e)}")
            
    return redirect('custom_manager')

#8.5 Hàm Sửa Váy Cưới
def edit_product(request, id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('home')
    # lấy váy cần sửa 
    product = get_object_or_404(Product, pk=id)
    stores = Store.objects.all()
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description', '')
        product.quantity = request.POST.get('quantity', 1)
        product.status = request.POST.get('status', 'available')
        store_id = request.POST.get('store')
        if store_id:
            product.store = Store.objects.get(pk=store_id)

        image = request.FILES.get('image')
        if image:
            product.image = image

        product.save() 
        messages.success(request, f"Đã cập nhật váy cưới '{product.name}' thành công!")
        return redirect('custom_manager')

    return render(request, 'edit_product.html', {'product': product, 'stores': stores})


#8.6 Hàm Xóa Cửa Hàng
def delete_store(request, id):
    if request.user.is_staff:
        Store.objects.filter(id=id).delete()
        messages.success(request, "Đã xóa cửa hàng!")
    return redirect('custom_manager')

#8.7 Hàm Thêm Cửa Hàng Mới
def add_store(request):
    if request.method == 'POST' and request.user.is_staff:
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')
        image = request.FILES.get('image') 
        Store.objects.create(
            name=name, address=address, phone=phone, 
            latitude=lat, longitude=lon, image=image
        )
        messages.success(request, f"Đã thêm cửa hàng {name} thành công!")
    return redirect('custom_manager')

#8.8 Hàm Sửa Cửa Hàng
def edit_store(request, id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('home')

    store = get_object_or_404(Store, pk=id)
    if request.method == 'POST':
        store.name = request.POST.get('name')
        store.phone = request.POST.get('phone')
        store.address = request.POST.get('address')
        store.latitude = request.POST.get('lat')
        store.longitude = request.POST.get('lon')
        image = request.FILES.get('image')
        if image:
            store.image = image
        store.save()
        messages.success(request, f"Đã cập nhật cửa hàng '{store.name}' thành công!")
        return redirect('custom_manager')

    return render(request, 'edit_store.html', {'store': store})


