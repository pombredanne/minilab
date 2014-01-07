#!/usr/bin/python

import language
from language import translate

response = open('public/index.html').read()

print translate(response)
