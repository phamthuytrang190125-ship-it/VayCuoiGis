from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Store, Product
import json
import math

# ==========================================
# PHẦN 1: CÔNG CỤ TÍNH TOÁN (HELPER FUNCTIONS)
# ==========================================

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Hàm tính khoảng cách giữa 2 tọa độ (Haversine Formula)
    Trả về: km (làm tròn 2 số lẻ)
    """
    R = 6371  # Bán kính trái đất (km)
    
    try:
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + \
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
            math.sin(dlon / 2) * math.sin(dlon / 2)
            
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return round(distance, 2)
    except:
        return 0

def calculate_fee_logic(distance_km):
    """
    Logic tính tiền ship:
    - < 5km: Free
    - 5 - 10km: 5k/km
    - > 10km: 10k/km
    """
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
    """
    Trang chủ: Hiển thị Bản đồ + Danh sách Váy + Cửa hàng gần nhất
    """
    products = Product.objects.all()
    stores = Store.objects.all()
    
    # Tọa độ mặc định (Chợ Bến Thành)
    user_lat = 10.7721
    user_lon = 106.6983
    
    # Nếu khách bấm nút "Tìm quanh đây"
    if request.method == 'POST':
        try:
            user_lat = float(request.POST.get('lat'))
            user_lon = float(request.POST.get('lon'))
        except (ValueError, TypeError):
            pass 

    store_list = []
    for s in stores:
        # 1. Tính khoảng cách
        dist = haversine_distance(user_lat, user_lon, s.latitude, s.longitude)
        
        # 2. TÍNH TIỀN SHIP (Đã thêm mới đoạn này)
        fee = calculate_fee_logic(dist)
        
        store_list.append({
            'name': s.name,
            'address': s.address,
            'phone': s.phone,
            'lat': s.latitude,
            'lon': s.longitude,
            'distance': dist,
            # 3. Gửi tiền ra JSON (Đã thêm mới đoạn này)
            'fee': fee,
            'formatted_fee': "{:,.0f}".format(fee).replace(",", ".") 
        })
    
    # Sắp xếp từ gần đến xa
    store_list.sort(key=lambda x: x['distance'])
    
    stores_json = json.dumps(store_list)
    
    return render(request, 'home.html', {
        'stores_json': stores_json,
        'stores': store_list,
        'products': products,
        'user_lat': user_lat,
        'user_lon': user_lon
    })

def product_detail(request, pk):
    """
    Trang chi tiết váy cưới
    """
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

# ==========================================
# PHẦN 3: API (ĐỂ JAVASCRIPT GỌI NGẦM)
# ==========================================

def api_calculate_shipping(request):
    """
    API nhận tọa độ khách -> Trả về phí ship (JSON)
    Link gọi: /api/shipping-fee/?store_id=1&lat=10.123&lon=106.123
    """
    store_id = request.GET.get('store_id')
    user_lat = request.GET.get('lat')
    user_lon = request.GET.get('lon')

    if not store_id or not user_lat or not user_lon:
        return JsonResponse({'error': 'Thiếu dữ liệu!'}, status=400)

    try:
        # 1. Tìm cửa hàng để lấy tọa độ gốc
        store = Store.objects.get(pk=store_id)
        
        # 2. Tính khoảng cách
        u_lat = float(user_lat)
        u_lon = float(user_lon)
        dist = haversine_distance(store.latitude, store.longitude, u_lat, u_lon)
        
        # 3. Tính tiền
        fee = calculate_fee_logic(dist)
        
        return JsonResponse({
            'store': store.name,
            'distance_km': dist,
            'shipping_fee': fee,
            'formatted_fee': "{:,.0f}".format(fee).replace(",", ".") # Định dạng 50.000
        })

    except Store.DoesNotExist:
        return JsonResponse({'error': 'Không tìm thấy cửa hàng'}, status=404)
    except ValueError:
        return JsonResponse({'error': 'Tọa độ lỗi'}, status=400)