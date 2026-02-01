from django.shortcuts import render
from .models import Store, Product  # Nhớ import cả Product
import json
import math

# --- 1. TOOL XỬ LÝ GIS: HÀM TÍNH KHOẢNG CÁCH (Công thức Haversine) ---
def haversine_distance(lat1, lon1, lat2, lon2):
    # Bán kính trái đất (km)
    R = 6371
    
    # Chuyển đổi độ sang radian
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dlon / 2) * math.sin(dlon / 2)
        
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Kết quả khoảng cách (km), làm tròn 2 số lẻ
    distance = R * c
    return round(distance, 2)

# --- 2. VIEW CHÍNH (XỬ LÝ LOGIC) ---
def home(request):
    # Lấy danh sách váy cưới để hiển thị
    products = Product.objects.all()
    
    # Lấy danh sách cửa hàng
    stores = Store.objects.all()
    
    # Tọa độ mặc định của khách (Ví dụ: Chợ Bến Thành), phòng khi khách chưa nhập gì
    user_lat = 10.7721
    user_lon = 106.6983
    
    # Xử lý khi khách bấm nút "Tìm quanh đây" (Gửi dữ liệu qua POST)
    if request.method == 'POST':
        try:
            # Lấy tọa độ khách nhập vào
            user_lat = float(request.POST.get('lat'))
            user_lon = float(request.POST.get('lon'))
        except (ValueError, TypeError):
            pass # Nếu nhập sai thì giữ nguyên mặc định

    # Danh sách chứa thông tin cửa hàng đã tính toán khoảng cách
    store_list = []
    
    for s in stores:
        # Gọi Tool GIS để tính khoảng cách
        dist = haversine_distance(user_lat, user_lon, s.latitude, s.longitude)
        
        store_list.append({
            'name': s.name,
            'address': s.address,
            'phone': s.phone,
            'lat': s.latitude,
            'lon': s.longitude,
            'distance': dist  # Lưu khoảng cách vào để hiển thị
        })
    
    # Sắp xếp danh sách: Gần nhất lên đầu (Sort theo 'distance')
    store_list.sort(key=lambda x: x['distance'])
    
    # Chuyển thành JSON để bản đồ Javascript đọc được
    stores_json = json.dumps(store_list)
    
    return render(request, 'home.html', {
        'stores_json': stores_json, # Dùng cho Bản đồ (Map)
        'stores': store_list,       # Dùng cho Danh sách bên trái (List)
        'products': products,       # Dùng cho Danh sách váy cưới
        'user_lat': user_lat,       # Để điền lại vào ô input sau khi tìm
        'user_lon': user_lon
    })