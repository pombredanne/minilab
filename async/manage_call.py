import sys
import os
import subprocess
import platform

class ManageCall(object):
    status_ok = 1001
    status_pending = 1002
    status_pid_not_exists = 1003

    @classmethod
    def create_subprocess(cls, process, args=[]):
        if platform.system() == 'Windows':
            DETACHED_PROCESS = 0x00000008
            # call subprocess
            pid = subprocess.Popen(
                [sys.executable, process] + args,
                 creationflags=DETACHED_PROCESS
            ).pid
        else:
            pid = subprocess.Popen([sys.executable, process] + args)
        return pid

    @classmethod
    def start(cls, pid):
        with open('pid/sessions', 'a') as f:
            f.write('%s\n' % pid)

        with open('pid/%s' % pid, 'w') as f:
            f.write('')
        return pid

    @classmethod
    def append_message(cls, pid=None, message=None):
        with open('pid/%s' % pid, 'a') as f:
            f.write('%s\n' % message)

    @classmethod
    def read_message(cls, pid):
        """

        @param pid:
        @return status, text: status of process and text message
        """
        with open('pid/sessions', 'r') as f:
            sessions = f.read().splitlines()

        if not pid in os.listdir('pid/'):
            return cls.status_pid_not_exists, 'No pid founded.'

        with open('pid/%s' % pid, 'r') as f:
            text = f.read()

        if pid in sessions:
            with open('pid/%s' % pid, 'w') as f:
                f.write('')
            return cls.status_pending, text
        else:
            os.system('rm pid/%s' % pid)
            return cls.status_ok, text

    @classmethod
    def done(cls, pid):
        sessions = []
        with open('pid/sessions', 'r') as f:
            sessions = f.read().splitlines()
        sessions.pop(sessions.index(str(pid)))
        print('done.')

        with open('pid/sessions', 'w') as f:
            f.write('\n'.join(sessions))
        return

