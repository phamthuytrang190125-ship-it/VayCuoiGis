from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Store, Product, Booking # THÊM Booking vào đây
from django.contrib import messages # THÊM messages để báo thành công
import json
import math

# ==========================================
# PHẦN 1: CÔNG CỤ TÍNH TOÁN (GIỮ NGUYÊN)
# ==========================================
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
    if distance_km < 5:
        return 0
    elif 5 <= distance_km <= 10:
        return distance_km * 5000
    else:
        return distance_km * 10000

# ==========================================
# PHẦN 2: CÁC VIEW HIỂN THỊ TRANG WEB
# ==========================================

def home(request):
    """ GIỮ NGUYÊN TOÀN BỘ LOGIC CỦA BẠN """
    products = Product.objects.all()
    stores = Store.objects.all()
    user_lat = 10.7721
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
            'name': s.name, 'address': s.address, 'phone': s.phone,
            'lat': s.latitude, 'lon': s.longitude, 'distance': dist,
            'fee': fee, 'formatted_fee': "{:,.0f}".format(fee).replace(",", ".") 
        })
    
    store_list.sort(key=lambda x: x['distance'])
    stores_json = json.dumps(store_list)
    
    return render(request, 'home.html', {
        'stores_json': stores_json, 'stores': store_list,
        'products': products, 'user_lat': user_lat, 'user_lon': user_lon
    })

def product_detail(request, pk):
   
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('customer_name')
        phone_input = request.POST.get('phone_number') 
        date = request.POST.get('booking_date') # Sẽ nhận dạng 2026-02-04T14:30
        note = request.POST.get('note')

        # Kiểm tra dữ liệu cơ bản trước khi lưu
        if name and phone_input and date:
            Booking.objects.create(
                product=product,
                customer_name=name,
                phone=phone_input,  
                booking_date=date,
                note=note
            )
            # Thông báo thành công sang trọng hơn
            messages.success(request, f"✨ Chúc mừng {name}! Lịch hẹn thử váy tại {product.store.name} đã được ghi nhận.")
            # Sau khi đặt thành công, nên redirect để tránh việc khách F5 trang bị gửi form 2 lần
            return redirect('product_detail', pk=pk)
        else:
            messages.error(request, "Vui lòng điền đầy đủ thông tin để chúng tôi liên hệ.")

    return render(request, 'product_detail.html', {'product': product})
# ==========================================
# PHẦN 3: API (GIỮ NGUYÊN)
# ==========================================
def api_calculate_shipping(request):
    store_id = request.GET.get('store_id')
    user_lat = request.GET.get('lat')
    user_lon = request.GET.get('lon')

    if not store_id or not user_lat or not user_lon:
        return JsonResponse({'error': 'Thiếu dữ liệu!'}, status=400)

    try:
        store = Store.objects.get(pk=store_id)
        u_lat, u_lon = float(user_lat), float(user_lon)
        dist = haversine_distance(store.latitude, store.longitude, u_lat, u_lon)
        fee = calculate_fee_logic(dist)
        
        return JsonResponse({
            'store': store.name, 'distance_km': dist, 'shipping_fee': fee,
            'formatted_fee': "{:,.0f}".format(fee).replace(",", ".")
        })
    except Store.DoesNotExist:
        return JsonResponse({'error': 'Không tìm thấy cửa hàng'}, status=404)
    except ValueError:
        return JsonResponse({'error': 'Tọa độ lỗi'}, status=400)