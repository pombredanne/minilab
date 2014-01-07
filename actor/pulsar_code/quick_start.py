# -*- coding: utf-8 -*-
from pulsar import spawn

import pulsar
import random

class PeriodicTask:
    def __call__(self, actor):
        actor.event_loop.call_repeatedly(2, self.task)

    def task(self):
        print(random.randint(0, 9))

arbiter = pulsar.arbiter()

ap = spawn(start=PeriodicTask())