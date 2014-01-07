from manage_call import ManageCall

import time
import sys
import os

pid = os.getpid()
ManageCall.start(pid)

ManageCall.append_message(pid=pid, message='Slepping ...')
time.sleep(5)
ManageCall.append_message(pid=pid, message='It\'ve been slepping along 5s')
time.sleep(5)
ManageCall.append_message(pid=pid, message='It\'ve been slepping along 10s')
time.sleep(5)
ManageCall.append_message(pid=pid, message='It\'ve been slepping along 15s')
time.sleep(5)
ManageCall.append_message(pid=pid, message='It\'ve been slepping along 20s')
time.sleep(5)
ManageCall.append_message(pid=pid, message='It\'ve been slepping along 25s')
time.sleep(5)
ManageCall.append_message(pid=pid, message='Wake up!')
ManageCall.done(pid)