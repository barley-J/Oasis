"""
Django settings for Oasis project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from datetime import timedelta
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jfmw@w)02@dfk9)8g7#0cjg52!%=2w#1%^j$@d(k_lr=*^n0@6'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'user',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Oasis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'Oasis.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'oasis',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'POST': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 安全警告：生产环境中不可置DEBUG为True
DEBUG = True
ALLOWED_HOSTS = ['*']

# 汉语 上海时区
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
# 国际化支持
USE_I18N = True
USE_L10N = True
# 存储至数据库不使用UTC时间
USE_TZ = False

# REST_FRAMEWORK设置
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # SessionAuthentication将允许DRF网页认证登陆
        # 会在AllowAny时导致 403 CSRF Failed: CSRF token missing or incorrect
        # 'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'sms': '1/min',
    },
    'DEFAULT_FILTER_BACKENDS': (
        # 多重条件过滤
        'django_filters.rest_framework.DjangoFilterBackend',
        # 排序
        'rest_framework.filters.OrderingFilter',
        # 搜索
        'rest_framework.filters.SearchFilter'
    ),
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'common.pagination.Pagination',
    'PAGE_SIZE': 5,
    # 设置全局时间格式化格式
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'ORDERING_PARAM': 'ordering',
    'SEARCH_PARAM': 'search',
}

# token auth 配置
JWT_AUTH = {
    # Token可用时长
    'JWT_EXPIRATION_DELTA': timedelta(days=7),
    # 允许以旧Token换取新Token
    'JWT_ALLOW_REFRESH': True,
    # 7天内下发的Token可以以旧Token换取新Token
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),
    # Authorization:Token xxx
    'JWT_AUTH_HEADER_PREFIX': 'Token',
}

# 设置user model
AUTH_USER_MODEL = "user.User"

# 静态文件 (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '/')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# 用户上传文件
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 输出日志
LOG_PATH = os.path.join(BASE_DIR, "log/")
DJANGO_LOG = os.path.dirname(LOG_PATH + 'django.log')
INFO_LOG = os.path.dirname(LOG_PATH + 'info.log')

if not os.path.exists(DJANGO_LOG):
    os.mkdir(DJANGO_LOG)

if not os.path.exists(INFO_LOG):
    os.mkdir(INFO_LOG)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s]- %(message)s'}
        # 日志格式
    },
    'handlers': {
        'django_error': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH + 'django.log',
            'formatter': 'standard'
        },
        'app_info': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH + 'info.log',
            'formatter': 'standard'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {
        'app_info': {
            'handlers': ['app_info', "console"],
            'level': 'DEBUG',
            'propagate': True
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['django_error', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        }
    },
}
