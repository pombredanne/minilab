# -*- coding: utf-8 -*-
from collections import defaultdict
from random import randint
from threading import Thread
from Queue import Queue
import time

class Session(object):
    session = {}

    @staticmethod
    def set(name, value):
        Session.session[name] = value

    @staticmethod
    def get(name):
        return Session.session[name]

def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        cr.next()
        return cr
    return start


class Task(object):
    taskid = 0
    def __init__(self,target):
        Task.taskid += 1
        self.tid = Task.taskid  # Task ID
        self.target = target  # Target coroutine
        self.sendval = None  # Value to send

    def run(self):
        return self.target.send(self.sendval)


class SystemCall(object):
    def handle(self):
        """
        Abstract method

        """
        pass


class GetTid(SystemCall):
    def handle(self):
        self.task.sendval = self.task.tid
        self.sched.schedule(self.task)


class NewTask(SystemCall):
    def __init__(self, target):
        self.target = target

    def handle(self):
        tid = self.sched.new(self.target)
        self.task.sendval = tid
        self.sched.schedule(self.task)


class KillTask(SystemCall):
    def __init__(self,tid):
        self.tid = tid

    def handle(self):
        task = self.sched.taskmap.get(self.tid,None)

        if task:
            task.target.close()
            self.task.sendval = True
        else:
            self.task.sendval = False
            self.sched.schedule(self.task)

class WaitTask(SystemCall):
    def __init__(self,tid):
        self.tid = tid
    def handle(self):
        result = self.sched.waitforexit(self.task,self.tid)
        self.task.sendval = result
        # If waiting for a non-existent task,
        # return immediately without waiting
        if not result:
            self.sched.schedule(self.task)


class Scheduler(object):
    def __init__(self):
        self.ready = Queue()
        self.taskmap = {}
        self.exit_waiting = {}

    def new(self,target):
        newtask = Task(target)
        self.taskmap[newtask.tid] = newtask
        self.schedule(newtask)
        return newtask.tid

    def schedule(self,task):
        self.ready.put(task)

    def exit(self,task):
        print "Task %d terminated" % task.tid
        del self.taskmap[task.tid]
        # Notify other tasks waiting for exit
        for task in self.exit_waiting.pop(task.tid,[]):
            self.schedule(task)

    def waitforexit(self,task,waittid):
        if waittid in self.taskmap:
            self.exit_waiting.setdefault(waittid,[]).append(task)
            return True
        else:
            return False

    def mainloop(self):
        while self.taskmap:
            task = self.ready.get()
            try:
                result = task.run()
                if isinstance(result,SystemCall):
                    result.task = task
                    result.sched = self
                    result.handle()
                    continue
            except StopIteration:
                self.exit(task)
                continue
            self.schedule(task)

def daq(name):
    Session.set('acq', [])
    while True:
        value = Session.get('acq')
        if len(value) > 10:
            value.pop(0)
        value.append(randint(0, 9))
        Session.set('', value)
        yield

def seg(name):
    while True:
        value = Session.get('acq')
        print(value)
        yield

def main():
    child = yield NewTask(daq('daq'))
    child2 = yield NewTask(seg('seg'))
    print "Waiting for child"
    yield WaitTask(child)
    print "Child done"

sched = Scheduler()
sched.new(main())
sched.mainloop()