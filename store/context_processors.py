# file: store/context_processors.py

def trial_cart_count(request):
    """
    Hàm này đếm số lượng váy đang có trong danh sách thử (Session).
    Nó sẽ tự động gửi biến 'trial_count' đến TẤT CẢ các file HTML.
    """
    # Lấy danh sách ID váy từ session, nếu chưa có thì trả về list rỗng []
    trial_list = request.session.get('trial_list', [])
    
    # Trả về độ dài của list (chính là số lượng váy)
    return {
        'trial_count': len(trial_list)
    }