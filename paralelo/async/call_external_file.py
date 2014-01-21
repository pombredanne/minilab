from paralelo.async.manage_call import ManageCall

# some code here
pid = ManageCall.create_subprocess('wait.py', ['arg1'])

print('pid %s' % pid.pid)
print('exit')