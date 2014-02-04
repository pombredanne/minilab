import math


def check(c, t, r):
    # R = outer radio
    # r = inner radio
    R = r + c['w']
    # y
    # |
    # . _ x 
    P1 = (r, t['h'] / 2.)
    P2 = (r + t['w'], t['h'] / 2.)
    P3 = (r, -(t['h'] / 2.))
    P4 = (r + t['w'], -(t['h'] / 2.))
    # a**2 = b**2 + c**2
    hypo1 = math.sqrt(((t['h']/2.)**2) + ((r + t['w'])**2))

    return (
        False if t['w'] > c['w'] else
        False if r > (P1[0] or P3[0]) else
        False if hypo1 > R else
        True 
    )
    
def calc(c, t):
    
    r = ((-c['w']**2) + ((t['h']/2)**2) + (t['w']**2) / 
         (2.*(c['w'] - t['w'])))
         
    return {r: check(c, t, r)}


def test(c, t):
    R = 0 # outer radio
    r = 0 # inner radio
    tests = {}
    for r in range(1000):
        tests[r] = check(c, t, float(r))
        
    return tests

curve = {}
truck = {}

truck['h'] = 6.0
truck['w'] = 3.0

curve['w'] = 3.3

ts = test(curve, truck)

print(filter(lambda v: v[1], ts.items())[0])
print(calc(curve, truck))