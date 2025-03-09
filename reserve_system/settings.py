# 在文件顶部添加以下代码
from pathlib import Path
import os

# 构建基础目录路径
BASE_DIR = Path(__file__).resolve().parent.parent


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reservation',  # 你的应用
    'rest_framework',  # DRF
    'corsheaders',  # 如果使用CORS
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 如果使用CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True  # 开发环境使用，生产环境应该指定允许的域名

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.example.com'  # 请更改为你的SMTP服务器
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'  # 请更改为你的邮箱
EMAIL_HOST_PASSWORD = 'your-password'  # 请更改为你的密码
DEFAULT_FROM_EMAIL = 'your-email@example.com'  # 请更改为你的邮箱

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static' 
# 设置默认主键字段类型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 安全密钥 - 在生产环境中应该保密
SECRET_KEY = 'django-insecure-your-secret-key-here'

# 调试模式 - 生产环境应设为False
DEBUG = True

# 允许的主机
ALLOWED_HOSTS = []

# 国际化设置
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# URL配置
ROOT_URLCONF = 'reserve_system.urls'