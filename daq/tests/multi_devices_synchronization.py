# need to start the dio task first!
from __future__ import print_function, absolute_import
from PyDAQmx import *
import time
import numpy as np
import platform
import multiprocessing as mp
import sys
import os

# internal libs
_dirname = os.path.dirname
parent_dir = _dirname(_dirname(_dirname(os.path.abspath(__file__))))
os.sys.path.insert(1, parent_dir)
os.sys.path.insert(1, 'c:/mswim/')

mod = __import__('arch')
sys.modules['arch'] = mod
__package__ = 'arch'

from arch.libs.buffer import DaqBuffer
from arch.libs.segmentation import SegmentTask
from arch.libs.save import Acquisition, save_acquisition_data

from labtrans.devices.cam.ocr.arh import FXCamd102

__PRINT = print
DEBUG = False

def new_print(*args, **kargs):
    if DEBUG:
        __PRINT(*args, **kargs)

print = new_print

# some useful parameters
CAM_HOST = 'localhost:65080'
samples_to_save = 15000
nsamples = 5000  # about 1 sec
samplerate = 5000.
# consider 'rse' (referenced single-ended),'nrse' (non-referenced single ended)
# 'diff', or 'pseudodiff' as other options, can look at panel for hints
TERMINALEND = 'nrse'

nchannels = 16
ndigital = 1  # number of digital channels

DEFAULT_PARAM_CREATE_AI = {
    'nameToAssignToChannel': '',
    'minVal': -10.0,
    'maxVal': 10.0,
    'terminalConfig': DAQmx_Val_NRSE,
    'units': DAQmx_Val_Volts,
    'customScaleName': None
}

DEFAULT_PARAM_SMPCLKTM_AI = {
    'source': '',
    'rate': samplerate,
    'activeEdge': DAQmx_Val_Rising,
    'sampleMode': DAQmx_Val_ContSamps,
    'sampsPerChan': nsamples*nchannels*10
}

DEFAULT_PARAM_SMPCLKTM_DI = {
    'rate': samplerate,
    'activeEdge': DAQmx_Val_Rising,
    'sampleMode': DAQmx_Val_ContSamps,
    'sampsPerChan': nsamples*ndigital*10
}

# connect analog input to this terminal, customize as you wish
analog_input_dev5 = r','.join(['Dev5/ai%s' % s for s in range(nchannels)])
analog_input_dev4 = r','.join(['Dev4/ai%s' % s for s in range(nchannels)])
analog_input_dev2 = r','.join(['Dev2/ai%s' % s for s in range(nchannels)])
analog_input_dev1 = r','.join(['Dev1/ai%s' % s for s in range(nchannels)])
temperature_input = r'Dev4/ai30,Dev4/ai31'

digital_input_dev5 = r'Dev5/port0/line0'
digital_input_dev4 = r'Dev4/port0/line0'
digital_input_dev1 = r'Dev1/port0/line0'

cam_input_trigger = r'Dev2/port0/line0'

DEV = {}
DEV['Dev1'] = analog_input_dev1.split(',') + digital_input_dev1.split(',')
DEV['Dev2'] = analog_input_dev2.split(',')
DEV['Dev4'] = (
    analog_input_dev4.split(',') +
    temperature_input.split(',') +
    digital_input_dev4.split(',')
)
DEV['Dev5'] = analog_input_dev5.split(',') + digital_input_dev5.split(',')
DEV['DevTemp'] = temperature_input.split(',')

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


def analog_dev1(asamples_dev1, go):
    # Analog dev 1
    print("\nCreating analog task.")
    # name='AIN'
    aitask = Task()
    aitask.CreateAIVoltageChan(analog_input_dev1, **DEFAULT_PARAM_CREATE_AI)
    aitask.CfgSampClkTiming(**DEFAULT_PARAM_SMPCLKTM_AI)

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
        print("Read %s ANALOG  samples ... queue size = %s, %f" % (
            total_samps.value, asamples_dev1.qsize(), time.time()-t
        ))
        sys.stdout.flush()
    aitask.stop()
    del aitask
    asamples_dev1.task_done()


def analog_dev2(asamples_dev2,go):
    # Analog dev 4
    print("\nCreating analog task.")
    # name='AIN'
    aitask = Task()
    aitask.CreateAIVoltageChan(analog_input_dev2, **DEFAULT_PARAM_CREATE_AI)
    aitask.CfgSampClkTiming(**DEFAULT_PARAM_SMPCLKTM_AI)

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
        print("Read %s ANALOG  samples ... queue size = %s, %f" % (
            nsamples, asamples_dev2.qsize(), time.time()-t
        ))
        sys.stdout.flush()
    aitask.stop()
    del aitask
    asamples_dev2.task_done()


def analog_dev4(asamples_dev4,go):
    # Analog dev 4
    print("\nCreating analog task.")
    # name='AIN'
    aitask = Task()
    aitask.CreateAIVoltageChan(
        analog_input_dev4 + ',' + temperature_input, **DEFAULT_PARAM_CREATE_AI
    )
    aitask.CfgSampClkTiming(
        r'',
        samplerate,
        DAQmx_Val_Rising,
        DAQmx_Val_ContSamps,
        nsamples*(nchannels+2)*10
    )
    #print "\naitask info:", aitask.get_info_str()
    sys.stdout.flush()
    aitask.StartTask()
    go.wait()
    while run:
        t = time.time()
        total_samps = int32()
        adata = np.zeros((nsamples*(nchannels+2),), dtype=np.float64)
        
        aitask.ReadAnalogF64(
            nsamples, 
            10.0,
            DAQmx_Val_GroupByChannel,
            adata,
            nsamples*(nchannels+2),
            byref(total_samps),        
            None
        )
        asamples_dev4.put(adata)
        #prof_a.write('%f\n' % (time.time()-t))
        print("Read %s ANALOG  samples ... queue size = %s, %f" % (
            nsamples,asamples_dev4.qsize(), time.time()-t
        ))
        sys.stdout.flush()
    aitask.stop()
    del aitask
    asamples_dev4.task_done()


def analog_dev5(asamples_dev5,go):
    # Analog
    print("\nCreating analog task.")
    # name='AIN'
    aitask = Task()
    aitask.CreateAIVoltageChan(analog_input_dev5, **DEFAULT_PARAM_CREATE_AI)
    aitask.CfgSampClkTiming(**DEFAULT_PARAM_SMPCLKTM_AI)
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
        print("Read %s ANALOG  samples ... queue size = %s, %f" % (
            nsamples,asamples_dev5.qsize(), time.time()-t
        ))
        sys.stdout.flush()
    aitask.stop()
    del aitask
    asamples_dev5.task_done()


def digital_dev1(dsamples_dev1,go):
    # Digital
    print("\nCreating digital task.")
    ditask = Task()
    ditask.CreateDIChan(digital_input_dev1, '', DAQmx_Val_ChanPerLine)
    ditask.CfgSampClkTiming(
        r'/Dev1/ai/SampleClock', **DEFAULT_PARAM_SMPCLKTM_DI
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
            10.0,
            DAQmx_Val_GroupByChannel,
            ddata,
            nsamples,
            byref(total_samps),
            byref(total_bytes),
            None
        )
        dsamples_dev1.put(ddata)
        #prof_d.write('%f\n' % (time.time()-t))
        print("Read %s DIGITAL samples ... queue size = %s, %f" % (
            nsamples, dsamples_dev1.qsize(), time.time()-t
        ))
        sys.stdout.flush()
    ditask.stop()
    del ditask
    dsamples_dev1.task_done()


def digital_dev4(dsamples_dev4, go):
    # Digital
    print("\nCreating digital task.")
    ditask = Task()
    ditask.CreateDIChan(digital_input_dev4, '', DAQmx_Val_ChanPerLine)
    ditask.CfgSampClkTiming(
        r'/Dev4/ai/SampleClock', **DEFAULT_PARAM_SMPCLKTM_DI
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
            10.0,
            DAQmx_Val_GroupByChannel,
            ddata,
            nsamples,
            byref(total_samps),
            byref(total_bytes),
            None
        )
        dsamples_dev4.put(ddata)
        #prof_d.write('%f\n' % (time.time()-t))
        print("Read %s DIGITAL samples ... queue size = %s, %f" % (
            nsamples, dsamples_dev4.qsize(), time.time()-t
        ))
        sys.stdout.flush()
    ditask.stop()
    del ditask
    dsamples_dev4.task_done()


def digital_dev5(dsamples_dev5, go):
    # Digital
    print("\nCreating digital task.")
    ditask = Task()
    ditask.CreateDIChan(digital_input_dev5, '', DAQmx_Val_ChanPerLine)
    ditask.CfgSampClkTiming(
        r'/Dev5/ai/SampleClock', **DEFAULT_PARAM_SMPCLKTM_DI
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
            10.0,
            DAQmx_Val_GroupByChannel,
            ddata,
            nsamples,
            byref(total_samps),
            byref(total_bytes),
            None
        )
        dsamples_dev5.put(ddata)
        #prof_d.write('%f\n' % (time.time()-t))
        print("Read %s DIGITAL samples ... queue size = %s, %f" % (
            nsamples, dsamples_dev5.qsize(), time.time()-t
        ))
        sys.stdout.flush()
    ditask.stop()
    del ditask
    dsamples_dev5.task_done()


def prepare_data(device_name, data):
    channels = DEV[device_name]

    return {
        name: data[i * nsamples:(i + 1) * nsamples]
        for i, name in enumerate(channels)
    }


def ring_buffer(bf_queue, save_queue):
    channels_settings = {
        'quartz': DEV['Dev1']+DEV['Dev2'],
        'ceramic': DEV['Dev5']+DEV['DevTemp'],
        'polymer': DEV['Dev4']
    }

    sensors_settings = {
        'quartz': {'trigger': digital_input_dev1},
        'ceramic': {'trigger': digital_input_dev5},
        'polymer': {'trigger': digital_input_dev4}
    }

    bf = DaqBuffer(channels_settings, nsamples*100)
    sg = SegmentTask(samples_to_save, sensors_settings)

    while True:
        bf.append(prepare_data(*bf_queue.get()))
        sg_data = sg(bf)

        if sg_data:
            save_queue.put(sg_data)

        print('RB size %s' % bf_queue.qsize())

    bf_queue.task_done()


def save_data_type(save_type_queue, cam_type_queue):
    """

    @param save_type_queue: queue
    @param cam_queue: queue

    """
    # CONFIGURATION
    dsn = ''
    with open('dsn.txt', 'r') as f:
        dsn = f.read()

    temperature_channels = [{'Dev4/ai30': 5, 'Dev4/ai31': 17}]
    sensors_settings = {
        'quartz': {'temperature_channels': []},
        'ceramic': {'temperature_channels': temperature_channels},
        'polymer': {'temperature_channels': temperature_channels},
    }

    channels = {
        'quartz': analog_input_dev1.split(',')+analog_input_dev2.split(','),
        'ceramic': analog_input_dev5.split(','),
        'polymer': analog_input_dev4.split(',')
    }

    acq = Acquisition(
        dsn, 'mswim', samples_to_save, samplerate, 1,
        sensors_settings, channels
    )

    while True:
        data = save_type_queue.get()
        t = time.time()
        try:
            vehicle_image = {data.keys()[0]: cam_type_queue.get(timeout=1)}
        except:
            vehicle_image = {}

        acq.save(data, vehicle_image)

        # print('<<< Saved Data from %s' % str(data.keys()))
        __PRINT(
            'Save type qsize: %s; CAM type qsize %s; - in %s secs.' % (
                save_type_queue.qsize(), cam_type_queue.qsize(), time.time()-t
            )
        )


def save_hub(
    save_queue, save_quartz_queue, save_ceramic_queue, save_polymer_queue
):
    """

    @param save_queue:
    @type save_queue:
    @param save_quartz_queue:
    @type save_quartz_queue:
    @param save_ceramic_queue:
    @type save_ceramic_queue:
    @param save_polymer_queue:
    @type save_polymer_queue:

    """
    _save_queues = {
        'quartz': save_quartz_queue,
        'ceramic': save_ceramic_queue,
        'polymer': save_polymer_queue
    }

    # LOOP PROCESS
    while True:
        data = save_queue.get()
        for k, d in data.items():
            _save_queues[k].put({k: d})

        __PRINT('Save qsize: %s' % save_queue.qsize())


def cam_send_trigger(cam_queue):
    """

    """
    numRead = int32()
    bytesPerSamp = int32()

    tg_num_channels = 1
    tg_samples_per_channel = 4

    _param_smpclktm_di = {
        'rate': 5000,
        'activeEdge': DAQmx_Val_Rising,
        'sampleMode': DAQmx_Val_ContSamps,
        'sampsPerChan': nsamples*ndigital*10
    }

    ditask = Task()
    ditask.CreateDIChan(
        cam_input_trigger, '', DAQmx_Val_ChanPerLine
    )
    """
    ditask.CfgSampClkTiming(
        r'/Dev2/ai/SampleClock', **_param_smpclktm_di
    )
    """
    ditask.CfgChangeDetectionTiming(
        cam_input_trigger, '', DAQmx_Val_ContSamps,
        tg_samples_per_channel * tg_num_channels
    )
    ditask.StartTask()

    data = np.zeros((tg_num_channels*tg_samples_per_channel,), dtype=np.uint8)

    cam = FXCamd102(CAM_HOST)

    while True:
        try:
            ditask.ReadDigitalLines(
                tg_samples_per_channel, 3.0,
                DAQmx_Val_GroupByScanNumber,
                data, tg_samples_per_channel*tg_num_channels,
                byref(numRead), byref(bytesPerSamp), None
            )
            cam_queue.put(cam.send_trigger(wait=True))
        except:
            #time out
            pass


def cam_get_image(
    cam_queue, cam_quartz_queue,
    cam_ceramic_queue, cam_polymer_queue
):
    """

    """
    cam = FXCamd102(CAM_HOST)
    while True:
        image_id = cam_queue.get()

        t = time.time()

        im = cam.image(image_id)

        cam_quartz_queue.put(im)
        cam_ceramic_queue.put(im)
        cam_polymer_queue.put(im)
        print(
            'CAM size %s %s %s : - Exec time: %f secs' %
            (
                cam_quartz_queue.qsize(),
                cam_ceramic_queue.qsize(),
                cam_polymer_queue.qsize(),
                time.time() - t)
        )

if __name__ == '__main__':
    # EVENTS
    go = mp.Event()

    # QUEUES
    bf_queue = mp.Queue()
    save_queue = mp.Queue()
    save_quartz_queue = mp.Queue()
    save_ceramic_queue = mp.Queue()
    save_polymer_queue = mp.Queue()

    cam_queue = mp.Queue()
    cam_quartz_queue = mp.Queue()
    cam_ceramic_queue = mp.Queue()
    cam_polymer_queue = mp.Queue()

    asamples_dev4 = mp.Queue()
    asamples_dev5 = mp.Queue()
    asamples_dev2 = mp.Queue()
    asamples_dev1 = mp.Queue()

    dsamples_dev1 = mp.Queue()
    dsamples_dev4 = mp.Queue()
    dsamples_dev5 = mp.Queue()

    # PROCESSES
    bf_proc = mp.Process(target=ring_buffer, args=(bf_queue, save_queue))

    save_hub_proc = mp.Process(
        target=save_hub,
        args=(
            save_queue, save_quartz_queue,
            save_ceramic_queue, save_polymer_queue
        )
    )

    save_quartz_proc = []
    save_ceramic_proc = []
    save_polymer_proc = []

    for _ in range(2):
        p = mp.Process(
            target=save_data_type, args=(save_quartz_queue, cam_quartz_queue)
        )
        p.daemon = True
        p.start()
        save_quartz_proc.append(p)

        p = mp.Process(
            target=save_data_type, args=(save_ceramic_queue, cam_ceramic_queue)
        )
        p.daemon = True
        p.start()
        save_ceramic_proc.append(p)

        p = mp.Process(
            target=save_data_type, args=(save_polymer_queue, cam_polymer_queue)
        )
        p.daemon = True
        p.start()
        save_polymer_proc.append(p)

    cam_send_trigger_proc = mp.Process(
        target=cam_send_trigger,
        args=(cam_queue,)
    )
    cam_get_image_proc = mp.Process(
        target=cam_get_image,
        args=(
            cam_queue, cam_quartz_queue,
            cam_ceramic_queue, cam_polymer_queue
        )
    )

    analog_dev1_proc = mp.Process(target=analog_dev1, args=(asamples_dev1, go))
    analog_dev2_proc = mp.Process(target=analog_dev2, args=(asamples_dev2, go))
    analog_dev4_proc = mp.Process(target=analog_dev4, args=(asamples_dev4, go))
    analog_dev5_proc = mp.Process(target=analog_dev5, args=(asamples_dev5, go))

    digital_dev1_proc = mp.Process(
        target=digital_dev1, args=(dsamples_dev1, go)
    )
    digital_dev4_proc = mp.Process(
        target=digital_dev4, args=(dsamples_dev4, go)
    )
    digital_dev5_proc = mp.Process(
        target=digital_dev5, args=(dsamples_dev5, go)
    )

    bf_proc.daemon = True
    save_hub_proc.daemon = True
    #save_quartz_proc.daemon = True
    #save_ceramic_proc.daemon = True
    #save_polymer_proc.daemon = True


    cam_send_trigger.daemon = True
    cam_get_image.daemon = True

    analog_dev1_proc.daemon = True
    analog_dev2_proc.daemon = True
    analog_dev4_proc.daemon = True
    analog_dev5_proc.daemon = True

    digital_dev1_proc.daemon = True
    digital_dev4_proc.daemon = True
    digital_dev5_proc.daemon = True

    digital_dev1_proc.start()
    digital_dev4_proc.start()
    digital_dev5_proc.start()
    analog_dev1_proc.start()
    analog_dev2_proc.start()
    analog_dev4_proc.start()
    analog_dev5_proc.start()

    # buffer process start
    bf_proc.start()
    save_hub_proc.start()
    #save_quartz_proc.start()
    #save_ceramic_proc.start()
    #save_polymer_proc.start()
    cam_send_trigger_proc.start()
    cam_get_image_proc.start()

    if DEBUG:
        print("Starting Processes")
        print("Digital Dev1 process PID = %s" % digital_dev1_proc.pid)
        print("Digital Dev4 process PID = %s" % digital_dev4_proc.pid)
        print("Digital Dev5 process PID = %s" % digital_dev5_proc.pid)
        print("Analog  Dev1 process PID = %s" % analog_dev1_proc.pid)
        print("Analog  Dev2 process PID = %s" % analog_dev2_proc.pid)
        print("Analog  Dev4 process PID = %s" % analog_dev4_proc.pid)
        print("Analog  Dev5 process PID = %s" % analog_dev5_proc.pid)
        #Syncronize reads in both threads
        print("Sending sync signal")

    sys.stdout.flush()
    go.set()

    while run:
        t = time.time()

        bf_queue.put(
            ('Dev1',
             np.concatenate((asamples_dev1.get(), dsamples_dev1.get())))
        )
        bf_queue.put(('Dev2', asamples_dev2.get()))
        bf_queue.put(
            ('Dev4',
             np.concatenate((asamples_dev4.get(), dsamples_dev4.get())))
        )
        bf_queue.put(
            ('Dev5',
             np.concatenate((asamples_dev5.get(), dsamples_dev5.get())))
        )

        if DEBUG:
            print(">>>> Read in %f secs." % (time.time()-t))

    analog_dev1_proc.join()
    analog_dev2_proc.join()
    analog_dev4_proc.join()
    analog_dev5_proc.join()
    digital_dev1_proc.join()
    digital_dev4_proc.join()
    digital_dev5_proc.join()

    bf_proc.join()
    save_hub_proc.join()
    cam_send_trigger.join()
    cam_get_image.join()

    for i in range(2):
        save_quartz_proc[i].join()
        save_polymer_proc[i].join()
        save_ceramic_proc[i].join()

    print("Done!")
