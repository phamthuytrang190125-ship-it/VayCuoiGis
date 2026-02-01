from django.shortcuts import render
from .models import Store
import json

def home(request):
    # Lấy tất cả cửa hàng từ Database
    stores = Store.objects.all()
    
    # Chuẩn bị dữ liệu GIS để vẽ lên bản đồ (dạng JSON)
    store_list = []
    for s in stores:
        store_list.append({
            'name': s.name,
            'lat': s.latitude,
            'lon': s.longitude,
            'address': s.address
        })
    
    # Chuyển thành chuỗi JSON để Javascript đọc được
    stores_json = json.dumps(store_list)
    
    return render(request, 'home.html', {'stores_json': stores_json})