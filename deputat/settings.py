import os

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'ur_4&s!%8awdfa!z+_60jrbfbfbg!%i7m14z%drhg*v*!=1rpou5ebfb%$8ji3ngthbghbghj'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'taggit',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.vk',
    'ckeditor',
    'ckeditor_uploader',
    'easy_thumbnails',

    'blog_cat',
    'blog',
    'elect',
    'lists',
    'search',
    'users',
    'about',
    'contacts',
    'terms',
    'policy',
    'stst',
    'common',
    'notify',
    'city',
    'region',
]

CKEDITOR_UPLOAD_PATH = 'media/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
       'default': {
           'toolbar': 'none',
           'height': 400,
           'width': 900,
           'removePlugins': 'stylesheetparser',
           'extraPlugins': 'codesnippet',
       },
    }

REST_AUTH_REGISTER_SERIALIZERS = {
        'REGISTER_SERIALIZER': 'deputat.serializers.RegisterSerializer',
}

AUTHENTICATION_BACKENDS = (
    #'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_ADAPTER = 'deputat.adapter.MyAccountAdapter'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
    'users.middleware.UpdateLastActivityMiddleware',
]

ROOT_URLCONF = 'deputat.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_PATH, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
            ],
        },
    },
]

WSGI_APPLICATION = 'deputat.wsgi.application'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'deputat_9',
        'USER': 'serg',
        'PASSWORD': 'ulihos46',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}



#AUTH_PASSWORD_VALIDATORS = [
#    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
#    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
#    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
#    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
#]


LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

MANAGERS = (("admin", "ochkarik1983@mail.ru"),)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 2525
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

AUTH_USER_MODEL = 'users.User'


THUMBNAIL_DEFAULT_OPTIONS = {"crop":"smart","detail":True}

SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}

ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_USERNAME_REQUIRED = False

THUMBNAIL_DEFAULT_OPTIONS = {"crop":"smart","detail":True}

THUMBNAIL_ALIASES = {
    "":{
        "avatar": {"size":(200,250)},
        "small_avatar": {"size":(100,100)},
    },
}
