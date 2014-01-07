import sys
from manage_call import ManageCall
import time

# some code here
pid = ManageCall.create_subprocess('wait.py', ['arg1'])

print('pid %s' % pid.pid)
print('exit')