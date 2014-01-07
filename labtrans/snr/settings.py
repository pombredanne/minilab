# -*- coding: utf-8 -*-
"""
Local Settings file

"""
DEBUG = True

_PATH_ROOT = __file__[:-len(__name__) + 2]

DEFAULT_FROM_EMAIL = 'ivan.ogassawara@gmail.com'

DATABASE = {
        'ENGINE':   'postgresql',
        'NAME':     'labdb',
        'USER':     'lab',
        'PASSWORD': 'lab',
        'HOST':     '150.162.176.112',
        'PORT':     '5432',
        'SCHEMA':   'mswim'
}