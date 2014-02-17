from random import randrange, randint
from collections import defaultdict

import multiprocessing


class DAQ(object):
    def __init__(self, device_name):
        self.device_name = device_name

    def listening_device(self):
        return {self.device_name: randrange(0, 10, 1)}


class Consumer(multiprocessing.Process):
    """

    """
    def __init__(self, device_name, task_queue, result_queue):
        multiprocessing.Process.__init__(self)

        self._task_queue = task_queue
        self._result_queue = result_queue
        self._daq = DAQ(device_name)

    def run(self):
        print id(self)
        while True:
            next_task = self._task_queue.get()

            if next_task is None:
                self._task_queue.task_done()
                break

            answer = next_task(daq=self._daq)
            self._task_queue.task_done()
            self._result_queue.put(answer)

        return


class DaqBuffer(object):
    data = defaultdict(list)

    def append(self, group_name, data):
        self.data[group_name] += data


class SegmentTask(object):
    def __call__(self, daq):
        return daq.listening_device()


if __name__ == '__main__':

    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    consumers = [
        Consumer(i, tasks, results) for i in ['Dev1', 'Dev2']
    ]

    for w in consumers:
        w.start()

    # loop
    seg_task = SegmentTask()
    while True:


        tasks.put(seg_task)

        result = results.get()

        print result