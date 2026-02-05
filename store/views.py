from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Store, Product, Booking
from django.contrib import messages
import json
import math

#Tính khoảng cách 
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
def home_shop(request):
    #Sắp xếp theo ID mới nhất lên đầu
    products = Product.objects.all().order_by('-id') 
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html')


# 2. Trang bản đồ 
def map_view(request):
    products = Product.objects.all()
    stores = Store.objects.all()
    user_lat = 10.7721 #mặc định CBT 
    user_lon = 106.6983
    
    if request.method == 'POST':
        try:
            user_lat = float(request.POST.get('lat'))
            user_lon = float(request.POST.get('lon'))
        except (ValueError, TypeError):
            pass 

    store_list = []
    for s in stores:
        dist = haversine_distance(user_lat, user_lon, s.latitude, s.longitude)
        fee = calculate_fee_logic(dist)
        store_list.append({
            'id': s.id,
            'name': s.name, 'address': s.address, 'phone': s.phone,
            'lat': s.latitude, 'lon': s.longitude, 'distance': dist,
            'fee': fee, 'formatted_fee': "{:,.0f}".format(fee).replace(",", ".") 
        })
    
    store_list.sort(key=lambda x: x['distance'])
    stores_json = json.dumps(store_list)
    
    #Trả về file map.html
    return render(request, 'map.html', {
        'stores_json': stores_json, 'stores': store_list,
        'products': products, 'user_lat': user_lat, 'user_lon': user_lon
    })

# 3. Trang chi tiết sản phẩm 
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        name = request.POST.get('customer_name')
        phone_input = request.POST.get('phone_number') 
        date = request.POST.get('booking_date')
        note = request.POST.get('note')

        if name and phone_input and date:
            Booking.objects.create(
                product=product, customer_name=name, phone=phone_input,  
                booking_date=date, note=note
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

#5. Hệ thống cửa hàng
#Danh sách tất cả cửa hàng
def store_list(request):
    stores = Store.objects.all()
    return render(request, 'store_list.html', {'stores': stores})

#Chi tiết cửa hàng (Hiện các váy của cửa hàng đó)
def store_detail_view(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    # Lấy tất cả sản phẩm thuộc cửa hàng này
    products = Product.objects.filter(store=store) 
    return render(request, 'store_detail_view.html', {'store': store, 'products': products})


#6. Trang liên hệ 
def contact(request):
    if request.method == 'POST':
        # Xử lý khi người dùng bấm Gửi
        name = request.POST.get('name')
        # Ở đây bạn có thể code thêm logic gửi email thật nếu cần
        # Hiện tại mình chỉ hiện thông báo thành công cho đẹp
        messages.success(request, f"Cảm ơn {name}! Chúng tôi đã nhận được tin nhắn và sẽ phản hồi sớm nhất.")
        return redirect('contact')
        
    return render(request, 'contact.html')