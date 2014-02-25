from __future__ import division, print_function
from threading import Thread
from multiprocessing import Process
from Queue import Queue
import time

BUFFER = range(10)

def do_work(item):
    print(id(BUFFER))


def worker():
    while True:
        item = q.get()
        do_work(item)
        q.task_done()

def source():
    return range(10)

if __name__ == '__main__':
    num_worker_threads = 4
    q = Queue()
    for i in range(num_worker_threads):
         t = Thread(target=worker)
         t.daemon = True
         t.start()

    for item in source():
        q.put(item)

    time.sleep(2)

    for item in source():
        q.put(item)

    time.sleep(2)