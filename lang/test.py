import re
import language

pattern = '\{\%\s*trans\s+"(.*)"\s*\%\}'
pattern_replace = ['\{\%\s*trans\s+"', '' , '"\s*\%\}']

text = open('public/index.html').read()

c = re.compile(pattern)
for i in c.findall(text):
    pattern_replace[1] = i
    text = re.sub(''.join(pattern_replace), _(i), text)

print(text)
