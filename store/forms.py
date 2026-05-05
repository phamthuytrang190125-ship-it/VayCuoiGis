from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class KhachHangRegisterForm(UserCreationForm):
    # Thêm trường email và bắt buộc (required=True)
    email = forms.EmailField(required=True, label="Địa chỉ Email")

    class Meta:
        model = User
        fields = ['username', 'email'] # Kéo thêm email vào form