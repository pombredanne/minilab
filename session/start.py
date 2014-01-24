try:
    # python 2
    import __builtin__
    __builtin__.session = None
except:
    # python 3
    import builtins
    builtins.session = None

from session_mmap import Session
from printing import print_session

__builtin__.session = Session
session = Session
session.modify('nome', 'Ivan')
print_session('nome')