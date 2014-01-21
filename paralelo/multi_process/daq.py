from __future__ import generators
import sys, time

threads = []
TOTALSWITCHES = 10**2
NUMTHREADS    = 10**1

def null_factory(i):
    def empty():
        while 1:
            yield None
            print i
    return empty()

def quitter():
    for n in xrange(TOTALSWITCHES/NUMTHREADS):
        yield None
        print 'q'

def scheduler():
    global threads
    T = None
    try:
        while 1:
            for thread in threads:
                T = thread
                thread.next()
    except StopIteration:
        print thread
        pass

if __name__ == "__main__":
    for i in range(NUMTHREADS):
        threads.append(null_factory(i))
    threads.append(quitter())
    starttime = time.clock()
    scheduler()
    print "TOTAL TIME:    ", time.clock()-starttime
    print "TOTAL SWITCHES:", TOTALSWITCHES
    print "TOTAL THREADS: ", NUMTHREADS