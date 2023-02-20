"""
Django settings for elearn project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from django.conf import settings
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+5==jc04m-)o#nn*^_z)bdgb7u7q0l9!321sr($i8pr2@9$@b)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'general',
    'django_countries',
    'resource',
    'ckeditor',
    'quiz',
    'virtual_class',
    'django_summernote',
    'faculty',
    'crispy_forms',
    'mathfilters',
    'materializecssform',
    'college',
    'widget_tweaks',
    'import_export',
    'accounts',    
    'api',
    'rest_framework',
    'rest_framework.authtoken',
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

ROOT_URLCONF = 'elearn.urls'

ADMIN_REORDER = (
    # Keep original label and models
    'auth',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
            'login_form_tags': 'templatetags.login_form_tags',
            'multioptions_tags' : 'templatetags.multioptions_tags',
            'status_tags'   : 'templatetags.status_tags',
            'answered_option_tags' : 'templatetags.answered_option_tags',
            'school_tags':'templatetags.school_tags',
            }
        },
    },
]

WSGI_APPLICATION = 'elearn.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
       'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kahe',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '',
        'OPTIONS': {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = 'ckeditor/uploads/'


CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'width': 'auto',
        'height': '100px',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
       
        'toolbar_Custom': [
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike','Superscript', 'Subscript',  '-',]},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},           
            {'name': 'links', 'items': ['Link']},
             {'name': 'insert',
             'items': ['Image', 'Smiley']},
      
            {'name': 'clipboard', 'items': ['Undo', 'Redo']},
             {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList',  'Blockquote', 
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', 
                       ]},
            {'name': 'math', 'items': ['Mathjax', ]},
        ],
        'toolbar': 'Custom',
        'mathJaxLib': '//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML',
        'extraPlugins': ','.join(['mathjax',]),
    },
}



# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "static_collect")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#login redirect 
LOGIN_REDIRECT_URL = '/home'
