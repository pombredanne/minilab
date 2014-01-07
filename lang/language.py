import os

# os.environ['LANG'] = 'pt_PT.UTF-8'

import os.path
import gettext
import re

TRANSLATION_DOMAIN = "lang"
LOCALE_DIR = os.path.join(os.path.dirname(__file__), "locale")

gettext.install(TRANSLATION_DOMAIN, LOCALE_DIR)

def translate(text):
    pattern = '\{\%\s*trans\s+"(.*)"\s*\%\}'
    pattern_replace = ['\{\%\s*trans\s+"', '' , '"\s*\%\}']

    c = re.compile(pattern)
    for i in c.findall(text):
        pattern_replace[1] = i
        text = re.sub(''.join(pattern_replace), _(i), text)

    return text
