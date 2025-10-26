import os
import dj_database_url # pyright: ignore[reportMissingImports]
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Bu ayarlar doğru, Render Environment Variables'dan okunacak
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# ALLOWED_HOSTS'u güncelledim
ALLOWED_HOSTS = ['localhost', '127.0.0.1'] # <-- GÜNCELLENDİ
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    ALLOWED_HOSTS.append('acusinema.onrender.com') # <-- EKLENDİ (Render URL'niz)


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Kendi uygulamalarınız
    'core',
    'users',

    # Üçüncü parti uygulamalar
    'storages',  # <-- EKLENDİ (Dosya depolama için)
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Bu satır doğru yerde
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'acusinema_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'acusinema_project.wsgi.application'

# Veritabanı ayarınız doğru (Render için)
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------------------
# AWS S3, STATIC VE MEDIA AYARLARI (KOMPLE GÜNCELLENDİ)
# -------------------------------------------------------------------

# AWS S3 AYARLARI (Değerleri Render'dan okuyacak)
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_FILE_OVERWRITE = False # Aynı isimli dosya yüklenirse üzerine yazmasın

# STATİK DOSYALAR (CSS, JS)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles' # collectstatic buraya toplar

# MEDYA DOSYALARI (Kullanıcı Yüklemeleri)
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/" # <-- GÜNCELLENDİ
MEDIA_ROOT = BASE_DIR / 'media' 

# STORAGES SÖZLÜĞÜ (Hatanızı düzelten kısım)
STORAGES = {
    # Medya dosyaları (upload) için S3 kullanılacak
    "default": { # <-- EKLENDİ (Bu eksikti)
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "location": "media", # Dosyalar S3 bucket'ında 'media' klasörüne yüklensin
            "file_overwrite": False,
        },
    },
    # Statik dosyalar (css/js) için WhiteNoise kullanılacak
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
# -------------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_URL = 'account'
LOGOUT_REDIRECT_URL = 'homepage'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# LOGGING AYARLARINIZ (Dokunulmadı)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                         'pathname=%(pathname)s lineno=%(lineno)d ' +
                         'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}