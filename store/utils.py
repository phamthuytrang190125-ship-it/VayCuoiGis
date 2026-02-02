import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Hàm tính khoảng cách giữa 2 điểm (theo đường chim bay)
    Dựa trên công thức Haversine nổi tiếng trong GIS.
    Trả về: Kilometers (km)
    """
    R = 6371  # Bán kính trái đất (km)

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    
    return round(distance, 2) # Làm tròn 2 số lẻ

def calculate_shipping_fee(distance_km):
    """
    Hàm tính tiền dựa trên quy tắc đã đề ra.
    """
    if distance_km < 5:
        return 0  # Miễn phí
    elif 5 <= distance_km <= 10:
        return distance_km * 5000
    else:
        return distance_km * 10000