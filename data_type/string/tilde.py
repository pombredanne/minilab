# -*- coding: utf-8 -*-
import unicodedata
import string

from unidecode import unidecode

def remove_accents(data):
    return ''.join(
        x for x in unicodedata.normalize('NFKD', data)
        if x in string.ascii_letters or x == '_'
    ).lower()

def remove_accents2(data):
    return filter(lambda char: char in string.ascii_uppercase, data.upper())

s = 'Números_distântes'.encode('utf8')
print(s)
print(unidecode(s.decode('utf-8')))