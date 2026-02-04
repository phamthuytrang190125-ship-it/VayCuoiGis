import os
import django
import io
import sys
from django.core.management import call_command

# 1. Thêm thư mục hiện tại vào danh sách tìm kiếm của Python
# Điều này giúp script "nhìn thấy" các thư mục như VayCuoiGis hay store
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 2. Thiết lập môi trường Django
# Đảm bảo 'VayCuoiGis' khớp với tên thư mục chứa file settings.py của bạn
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VayCuoiGis.settings')

try:
    django.setup()

    # 3. Ghi file với mã hóa utf-8 tường minh
    with io.open('dulieu_vay.json', 'w', encoding='utf-8') as f:
        call_command('dumpdata', 'store', indent=2, stdout=f)

    print("✨ Đã xuất dữ liệu thành công vào file dulieu_vay.json với chuẩn UTF-8!")

except Exception as e:
    print(f"❌ Lỗi: {e}")
    print("Mẹo: Hãy kiểm tra xem thư mục con chứa settings.py có đúng tên là 'VayCuoiGis' không?")