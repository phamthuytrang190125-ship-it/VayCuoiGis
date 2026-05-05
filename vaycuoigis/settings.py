"""
Django settings for vaycuoigis project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-72h212q^-h#g9h36#jp)wr$_-ecwqris5m)#z1mk&rkzxb8&="

DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    "jazzmin", # Admin Theme
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "store",
    "django.contrib.humanize",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "vaycuoigis.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "store.context_processors.trial_cart_count",
            ],
        },
    },
]

WSGI_APPLICATION = "vaycuoigis.wsgi.application"

# Database - PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "vaycuoigis",
        "USER": "postgres",
        "PASSWORD": "123456",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

# Internationalization
LANGUAGE_CODE = "vi"
TIME_ZONE = "Asia/Ho_Chi_Minh"
USE_I18N = True
USE_TZ = True
USE_L10N = True
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = '.'

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Media files (Uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Jazzmin Admin Configuration
JAZZMIN_SETTINGS = {
    "site_title": "Quản trị Váy Cưới GIS",
    "site_header": "Bridal Admin",
    "site_brand": "Bridal Luxury",
    "welcome_sign": "Chào mừng đến với hệ thống quản trị Váy Cưới",
    "copyright": "Bridal GIS Team",
    
    # Custom CSS
    "custom_css": "css/admin_royal.css",

    # Search models
    "search_model": ["store.Product", "store.Store", "store.Booking"],
    
    # Top menu links
    "topmenu_links": [
        {"name": "Trang chủ bản đồ", "url": "home", "permissions": ["auth.view_user"]},
    ],

    "show_sidebar": True,
    "navigation_expanded": True,
    "show_ui_builder": False, 
    
    # Icons configuration
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "store.Product": "fas fa-female",
        "store.Store": "fas fa-store-alt",
        "store.Booking": "fas fa-calendar-check",
    },
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "sidebar": "sidebar-light-primary", 
    "navbar": "navbar-dark",
    "accent": "accent-primary",
    "brand_colour": "navbar-primary",
    "no_navbar_border": True,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

# Cấu hình chuyển hướng Đăng nhập / Đăng xuất
LOGIN_REDIRECT_URL = '/manager/'  
LOGOUT_REDIRECT_URL = '/'    

# CẤU HÌNH GỬI EMAIL BẰNG MAILTRAP (TESTING)
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_HOST_USER = '2b25a6db0e5988'
EMAIL_HOST_PASSWORD = '6319fbbf80a516'
EMAIL_PORT = '2525'

# CẤU HÌNH ĐỊNH DẠNG TIỀN TỆ VIỆT NAM
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = '.'
NUMBER_GROUPING = 3