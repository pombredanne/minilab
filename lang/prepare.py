#!/usr/bin/python

import os
import re

# prepare html
lang_pot = os.getcwd() + '/locale/lang.pot'
pot_content = open(lang_pot).read()

exp = re.compile('\{\%\s*trans\s+"(.*)"\s*\%\}')

for root, subFolders, files in os.walk(os.getcwd() + '/public'):
    for _file in files:
        header = _file
        text = open(os.path.join(root, _file)).read()
        for tag in exp.findall(text):
            pattern = 'msgid\s"%s"' % tag
            exp_pot = re.compile(pattern)
            if not exp_pot.findall(pot_content):
                if header:
                    pot_content += '\n#: %s' % header
                    header = None
                pot_content += '\nmsgid "%s"\n' % tag
                pot_content += 'msgstr ""\n'

open(lang_pot, 'w').write(pot_content)

c = 'xgettext --default-domain=lang --output=locale/lang.pot *.py '
out = os.popen(c).read()
print(out)

c = 'msgmerge --output-file=locale/es/lang.po locale/es/lang.po locale/lang.pot'
out = os.popen(c).read()
print(out)

c = 'msgmerge --output-file=locale/pt/lang.po locale/pt/lang.po locale/lang.pot'
out = os.popen(c).read()
print(out)

c = 'msgfmt --output-file=locale/es/LC_MESSAGES/lang.mo locale/es/lang.po'
out = os.popen(c).read()
print(out)

c = 'msgfmt --output-file=locale/pt/LC_MESSAGES/lang.mo locale/pt/lang.po'
out = os.popen(c).read()
print(out)
