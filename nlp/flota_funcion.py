import re


def distance_function(description):
    """
    
    """
    # convert Portuguese preposition 'e' to 'and'
    text = description.replace(' e ', ' and ')
    # identify variables
    pattern = re.compile('d[0-9]+')
    l_var_ori = pattern.findall(text)

    # remove meters unit
    text = text.replace(' m', '')
    # converts to float
    text = re.sub(r'([0-9]+)(,)([0-9]+)', r'\1.\3', text)
    # process all variables founded
    for v in  l_var_ori:
        # converts to list format
        _v = 'd[%s] - d[%s]' % (v[2], v[1])
        text = text.replace(v, _v)

    new_function = text.split(' and ')
    new_function_final = []

    for v in new_function:
        # replace comma to " and "
        _v = v
        _v = v.replace(',', ' and ')
        # group expressions
        _v = re.sub(r'(.+)([><])(.*)', r'(\1)\2(\3)', _v)
        new_function_final.append(_v)

    _lambda = 'lambda d:' + ' and '.join(new_function_final)

    return eval(_lambda)

s = 'd12, d34 > 2,40 m e 1,20 m < d23, d45 < 2,40 m'
_d = [0, 1, 4, 6, 9, 11.3]
f = distance_function(s)
print(f(_d))
