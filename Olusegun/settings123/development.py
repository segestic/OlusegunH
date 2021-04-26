#seg
from .base import *


# from .base import INSTALLED_APPS

INSTALLED_APPS = INSTALLED_APPS + ['debug_toolbar',]

 # 'django_extensions'
DEBUG = True


#seg


import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '%123!@$%ee^$%^&134567&^klljhgfghjjhgfdgjhf%ggjjj$%12')


MIDDLEWARE = MIDDLEWARE + [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']

ALLOWED_HOSTS += ['127.0.0.1','localhost']