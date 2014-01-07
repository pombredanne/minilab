from manage_call import ManageCall

import time
import sys

try:
    pid = sys.argv[1]
except:
    print('No pid informed.')
    exit()

while True:
    status, text = ManageCall.read_message(pid)

    status_text = (
        'true' if status == ManageCall.status_ok else
        'pending' if status == ManageCall.status_pending else
        'false'
    )

    if text:
        print('{"status": "%s", "message": "%s"}' % (status_text, text))

    if not status == ManageCall.status_pending:
        break

    time.sleep(1)