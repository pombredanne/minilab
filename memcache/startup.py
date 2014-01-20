"""
try:
    # python 2
    import __builtin__
    builtin_module = __builtin__
except:
    # python 3
    import builtins
    builtin_module = builtins
"""

from shared_memory import SharedMemory

SharedMemory = SharedMemory