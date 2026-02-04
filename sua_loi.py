import os
import django
import io
import sys
from django.core.management import call_command

# 1. Tự động lấy đường dẫn thư mục hiện tại
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# 2. KIỂM TRA TÊN THƯ MỤC SETTINGS
# Mình sẽ in ra danh sách thư mục để bạn xem tên nào mới đúng
subfolders = [f.name for f in os.scandir(BASE_DIR) if f.is_dir() and not f.name.startswith('.')]
print(f"--- Thư mục hiện tại có các folder: {subfolders} ---")

# THAY THẾ: Bạn hãy nhìn trong danh sách trên, folder nào chứa settings.py?
# Thử thay 'VayCuoiGis' bằng tên folder đó (ví dụ: 'config' hoặc 'core')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaycuoigis.settings') 

try:
    django.setup()
    with io.open('dulieu_vay_chuan.json', 'w', encoding='utf-8') as f:
        call_command('dumpdata', 'store', indent=2, stdout=f)
    print("✨ CHÚC MỪNG! Đã xuất file dulieu_vay_chuan.json thành công!")
except Exception as e:
    print(f"❌ Vẫn lỗi: {e}")
    print("Gợi ý: Nếu danh sách folder phía trên không có tên 'VayCuoiGis', hãy sửa lại dòng số 16!")