# need to start the dio task first!
import time
import numpy as np
from PyDAQmx import *
import multiprocessing as mp
import sys

# some useful parameters
nsamples    = 5000 # about 1 sec
samplerate  = 5000
# consider 'rse' (referenced single-ended),'nrse' (non-referenced single ended)
# 'diff', or 'pseudodiff' as other options, can look at panel for hints
TERMINALEND = 'nrse'

# connect analog input to this terminal, customize as you wish

analog_input_dev5 = r'Dev5/ai0'
analog_input_dev4 = r'Dev4/ai0' 
analog_input_dev2 = r'Dev3/ai0'
analog_input_dev1 = r'Dev1/ai0'
nchannels = 1

ndigital = 1 # number of digital channels
digital_input_dev5 = r'Dev5/port0/line0'
digital_input_dev4 = r'Dev4/port0/line0'
digital_input_dev1 = r'Dev1/port0/line0'

samplemode = 'continuous'

run = True

"""
prof_a = open('c:/tmp/prof_a', 'w')
prof_a.write('')
prof_a.close()
prof_a = open('c:/tmp/prof_a', 'a')

prof_d = open('c:/tmp/prof_d', 'w')
prof_d.write('')
prof_d.close()
prof_d = open('c:/tmp/prof_d', 'a')
"""

def analog_dev1(asamples_dev1,go):
    # Analog dev 1
    print "\nCreating analog task."
    # name='AIN'
    aitask = Task()
    aitask.CreateAIVoltageChan(
        analog_input_dev1, '',
        minVal=-10.0,maxVal=10.0, terminalConfig=DAQmx_Val_NRSE, 
        units=DAQmx_Val_Volts, customScaleName=None
    )
    aitask.CfgSampClkTiming(
        'OnboardClock',
        samplerate,
        DAQmx_Val_Rising,
        DAQmx_Val_ContSamps,
        nsamples*10
    )
    #print "\naitask info:", aitask.get_info_str()
    sys.stdout.flush()
    aitask.StartTask()
    go.wait()
    while run:
        t = time.time()
        total_samps = int32()
        adata = np.zeros((nsamples*nchannels,), dtype=np.float64)
        
        aitask.ReadAnalogF64(
            nsamples, 
            10.0,
            DAQmx_Val_GroupByChannel,
            adata,
            nsamples*nchannels,
            byref(total_samps),        
            None
        )
        asamples_dev1.put(adata)
        #prof_a.write('%f\n' % (time.time()-t))
        print "Read %s ANALOG  samples ... queue size = %s, %f" % (
            nsamples,asamples_dev1.qsize(), time.time()-t
        )
        sys.stdout.flush()
    aitask.stop()
    del aitask
    asamples_dev1.task_done()

def analog_dev2(asamples_dev2,go):
    # Analog dev 4
    print "\nCreating analog task."
    # name='AIN'
    aitask = Task()
    aitask.CreateAIVoltageChan(
        analog_input_dev2, 'A2',
        minVal=-10.0,maxVal=10.0, terminalConfig=DAQmx_Val_NRSE, 
        units=DAQmx_Val_Volts, customScaleName=None
    )
    aitask.CfgSampClkTiming(
        r'',
        samplerate,
        DAQmx_Val_Rising,
        DAQmx_Val_ContSamps,
        nsamples*10
    )
    #print "\naitask info:", aitask.get_info_str()
    sys.stdout.flush()
    aitask.StartTask()
    go.wait()
    while run:
        t = time.time()
        total_samps = int32()
        adata = np.zeros((nsamples*nchannels,), dtype=np.float64)
        
        aitask.ReadAnalogF64(
            nsamples, 
            10.0,
            DAQmx_Val_GroupByChannel,
            adata,
            nsamples*nchannels,
            byref(total_samps),        
            None
        )
        asamples_dev2.put(adata)
        #prof_a.write('%f\n' % (time.time()-t))
        print "Read %s ANALOG  samples ... queue size = %s, %f" % (
            nsamples,asamples_dev2.qsize(), time.time()-t
        )
        sys.stdout.flush()
    aitask.stop()
    del aitask
    asamples_dev2.task_done()
    
def analog_dev4(asamples_dev4,go):
    # Analog dev 4
    print "\nCreating analog task."
    # name='AIN'
    aitask = Task()
    aitask.CreateAIVoltageChan(
        analog_input_dev4, '',
        minVal=-10.0,maxVal=10.0, terminalConfig=DAQmx_Val_NRSE, 
        units=DAQmx_Val_Volts, customScaleName=None
    )
    aitask.CfgSampClkTiming(
        r'/Dev1/ai/SampleClock',
        samplerate,
        DAQmx_Val_Rising,
        DAQmx_Val_ContSamps,
        nsamples*10
    )
    #print "\naitask info:", aitask.get_info_str()
    sys.stdout.flush()
    aitask.StartTask()
    go.wait()
    while run:
        t = time.time()
        total_samps = int32()
        adata = np.zeros((nsamples*nchannels,), dtype=np.float64)
        
        aitask.ReadAnalogF64(
            nsamples, 
            10.0,
            DAQmx_Val_GroupByChannel,
            adata,
            nsamples*nchannels,
            byref(total_samps),        
            None
        )
        asamples_dev4.put(adata)
        #prof_a.write('%f\n' % (time.time()-t))
        print "Read %s ANALOG  samples ... queue size = %s, %f" % (
            nsamples,asamples_dev4.qsize(), time.time()-t
        )
        sys.stdout.flush()
    aitask.stop()
    del aitask
    asamples_dev4.task_done()
    
def analog_dev5(asamples_dev5,go):
    # Analog
    print "\nCreating analog task."
    # name='AIN'
    aitask = Task()
    aitask.CreateAIVoltageChan(
        analog_input_dev5, '',
        minVal=-10.0,maxVal=10.0, terminalConfig=DAQmx_Val_NRSE, 
        units=DAQmx_Val_Volts, customScaleName=None
    )
    
    aitask.CfgSampClkTiming(
        r'',
        samplerate,
        DAQmx_Val_Rising,
        DAQmx_Val_ContSamps,
        nsamples*10
    )
    #print "\naitask info:", aitask.get_info_str()
    sys.stdout.flush()
    aitask.StartTask()
    go.wait()
    
    while run:
        t = time.time()
        total_samps = int32()
        adata = np.zeros((nsamples*nchannels,), dtype=np.float64)
        
        aitask.ReadAnalogF64(
            nsamples, 
            10.0,
            DAQmx_Val_GroupByChannel,
            adata,
            nsamples*nchannels,
            byref(total_samps),        
            None
        )
        
        asamples_dev5.put(adata)
        #prof_a.write('%f\n' % (time.time()-t))
        print "Read %s ANALOG  samples ... queue size = %s, %f" % (
            nsamples,asamples_dev5.qsize(), time.time()-t
        )
        sys.stdout.flush()
    aitask.stop()
    del aitask
    asamples_dev5.task_done()


def digital_dev1(dsamples_dev1,go):
    # Digital
    print "\nCreating digital task."
    ditask = Task()
    ditask.CreateDIChan(digital_input_dev1, '', DAQmx_Val_ChanPerLine)
    ditask.CfgSampClkTiming(
        r'/Dev1/ai/SampleClock', samplerate,
        DAQmx_Val_Rising, DAQmx_Val_ContSamps, nsamples*10*ndigital
    )
    #print "digital task info:", ditask.get_info_str()
    sys.stdout.flush()
    ditask.StartTask()
    go.wait()
    while run:
        t = time.time()
        total_samps = int32()
        total_bytes = int32()
        
        ddata = np.zeros((nsamples*nchannels,), dtype=np.uint8)
        
        ditask.ReadDigitalLines(
            nsamples,
            2.0,
            DAQmx_Val_GroupByChannel,
            ddata,
            nsamples,
            byref(total_samps),
            byref(total_bytes),
            None
        )
        dsamples_dev1.put(ddata)
        #prof_d.write('%f\n' % (time.time()-t))
        print "Read %s DIGITAL samples ... queue size = %s, %f" % (
            nsamples, dsamples_dev1.qsize(), time.time()-t
        )
        sys.stdout.flush()
    ditask.stop()
    del ditask
    dsamples_dev1.task_done()
    
def digital_dev4(dsamples_dev4,go):
    # Digital
    print "\nCreating digital task."
    ditask = Task()
    ditask.CreateDIChan(digital_input_dev4, 'line0', DAQmx_Val_ChanPerLine)
    ditask.CfgSampClkTiming(
        r'/Dev1/ai/SampleClock', samplerate,
        DAQmx_Val_Rising, DAQmx_Val_ContSamps, nsamples*10*ndigital
    )
    #print "digital task info:", ditask.get_info_str()
    sys.stdout.flush()
    ditask.StartTask()
    go.wait()
    while run:
        t = time.time()
        total_samps = int32()
        total_bytes = int32()
        
        ddata = np.zeros((nsamples*nchannels,), dtype=np.uint8)
        
        ditask.ReadDigitalLines(
            nsamples,
            2.0,
            DAQmx_Val_GroupByChannel,
            ddata,
            nsamples,
            byref(total_samps),
            byref(total_bytes),
            None
        )
        dsamples_dev4.put(ddata)
        #prof_d.write('%f\n' % (time.time()-t))
        print "Read %s DIGITAL samples ... queue size = %s, %f" % (
            nsamples, dsamples_dev4.qsize(), time.time()-t
        )
        sys.stdout.flush()
    ditask.stop()
    del ditask
    dsamples_dev4.task_done()

def digital_dev5(dsamples_dev5,go):
    # Digital
    print "\nCreating digital task."
    ditask = Task()
    ditask.CreateDIChan(digital_input_dev5, 'line0', DAQmx_Val_ChanPerLine)
    ditask.CfgSampClkTiming(
        r'/Dev1/ai/SampleClock', samplerate,
        DAQmx_Val_Rising, DAQmx_Val_ContSamps, nsamples*10*ndigital
    )
    #print "digital task info:", ditask.get_info_str()
    sys.stdout.flush()
    ditask.StartTask()
    go.wait()
    while run:
        t = time.time()
        total_samps = int32()
        total_bytes = int32()
        
        ddata = np.zeros((nsamples*nchannels,), dtype=np.uint8)
        
        ditask.ReadDigitalLines(
            nsamples,
            2.0,
            DAQmx_Val_GroupByChannel,
            ddata,
            nsamples,
            byref(total_samps),
            byref(total_bytes),
            None
        )
        dsamples_dev5.put(ddata)
        #prof_d.write('%f\n' % (time.time()-t))
        print "Read %s DIGITAL samples ... queue size = %s, %f" % (
            nsamples, dsamples_dev5.qsize(), time.time()-t
        )
        sys.stdout.flush()
    ditask.stop()
    del ditask
    dsamples_dev5.task_done()

if __name__ == '__main__':
    go = mp.Event()
    asamples_dev4 = mp.Queue()
    asamples_dev5 = mp.Queue()
    asamples_dev2 = mp.Queue()
    asamples_dev1 = mp.Queue()
    dsamples_dev1 = mp.Queue()
    dsamples_dev4 = mp.Queue()
    dsamples_dev5 = mp.Queue()
    
    analog_dev1_proc = mp.Process(target=analog_dev1, args=(asamples_dev1, go))
    analog_dev2_proc = mp.Process(target=analog_dev2, args=(asamples_dev2, go))
    analog_dev4_proc = mp.Process(target=analog_dev4, args=(asamples_dev4, go))
    analog_dev5_proc = mp.Process(target=analog_dev5, args=(asamples_dev5, go))
    digital_dev1_proc = mp.Process(
        target=digital_dev1, args=(dsamples_dev1, go)
    )

    analog_dev1_proc.daemon = True
    analog_dev2_proc.daemon = True
    analog_dev4_proc.daemon = True
    analog_dev5_proc.daemon = True
    digital_dev1_proc.daemon = True

    print "Starting Processes"
    
    analog_dev2_proc.start()
    print "Analog Dev2 process PID  = %s" % analog_dev2_proc.pid
    
    digital_dev1_proc.start()
    print "Digital Dev1 process PID = %s" % digital_dev1_proc.pid
    
    '''
    
    analog_dev4_proc.start()
    print "Analog Dev4 process PID  = %s" % analog_dev4_proc.pid
    
    analog_dev5_proc.start()
    print "Analog Dev5 process PID  = %s" % analog_dev5_proc.pid
    '''
    
    analog_dev1_proc.start()
    print "Analog Dev1 process PID  = %s" % analog_dev1_proc.pid
    
    #time.sleep(3)

    af = open('/tmp/ana.txt', 'w')
    df = open('/tmp/dig.txt', 'w')

    print "\nWriting files..."
    sys.stdout.flush()
    
    #Syncronize reads in both threads
    print "Sending sync signal"
    go.set()

    while run:
        t = time.time()
        
        asamp = asamples_dev1.get()
        #asamp += asamples_dev1.get()
        #asamp += asamples_dev1.get()
        for a_s in asamp:
            af.write('%s\n' % a_s)
        
        asamp = asamples_dev2.get()
        #asamp += asamples_dev2.get()
        #asamp += asamples_dev2.get()
        for a_s in asamp:
            af.write('%s\n' % a_s)
        '''
        asamp = asamples_dev4.get()
        asamp += asamples_dev4.get()
        asamp += asamples_dev4.get()
        for a_s in asamp:
            af.write('%s\n' % a_s)
            
        asamp = asamples_dev5.get()
        asamp += asamples_dev5.get()
        asamp += asamples_dev5.get()
        for a_s in asamp:
            af.write('%s\n' % a_s)
        '''
        '''
        dsamp = dsamples_dev1.get()
        #dsamp += dsamples_dev1.get()
        #dsamp += dsamples_dev1.get()
        for d_s in dsamp:
            df.write('%s\n' % d_s)
        '''
            
        print(">>>> Read in %f secs." % (time.time()-t))
    af.close()
    df.close()

    analog_dev1_proc.join()
    analog_dev2_proc.join()
    analog_dev4_proc.join()
    analog_dev5_proc.join()
    digital_dev1_proc.join()
    
    print "Done!"
