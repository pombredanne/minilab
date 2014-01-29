from __future__ import print_function
from continuous import DigitalContinuousTask, AnalogContinuousTask
from datetime import datetime
from collections import defaultdict
from time import sleep


def calculate_time_sequence(delta_t, quantity):
    timestamp = [datetime.now()]

    def next_time(_timestamp):
        _ts = _timestamp[0]
        _timestamp[0] += delta_t
        return _ts

    return [next_time(timestamp) for _ in range(quantity)]


class AcquisitionTask():
    """

    """
    ACQ_TYPE = {
        'test': 2,
        'calibration': 3,
        'statistic': 1
    }

    analog_task = None
    digital_task = None

    device = None

    def __init__(self, device={}, acquisition_mode=''):
        """

        @return:

        """
        self.device = device

        if acquisition_mode == 'continuous':
            DIGITAL_TASK = DigitalContinuousTask
            ANALOG_TASK = AnalogContinuousTask
        else:
            raise Exception('Invalid Acquisition Mode.')

        self.digital_task = DIGITAL_TASK(
            channels=device['digital'],
            samples_per_channel=device['rate']
        )

        self.analog_task = ANALOG_TASK(
            physical_channel=device['analog'],
            rate=device['rate'],
            minv=device['minv'],
            maxv=device['maxv'],
            seconds_to_acquire=device['seconds_to_acquire']
        )

    def read(self):
        signals = self.read_analog()
        signals.update(self.read_digital())
        return signals

    def read_analog(self):
        data = self.analog_task.read()

        sensors = defaultdict(dict)
        for chan_i, chan_data in data.items():
            i_sensor = self.analog_task.physical_channel.index(chan_i)
            for i, sensor_voltage in enumerate(chan_data):
                # changed to return use the same baseline
                if not sensors[i_sensor]:
                    sensors[i_sensor] = list()
                sensors[i_sensor] += [sensor_voltage]
        return sensors

    def read_digital(self):
        return {}
        data = self.digital_task.read()

        sensors = defaultdict(dict)
        for chan_i, chan_data in data.items():
            i_sensor = self.channel.index(chan_i)
            for i, sensor_voltage in enumerate(chan_data):
                # changed to return use the same baseline
                if not sensors[i_sensor]:
                    sensors[i_sensor] = defaultdict(list)
                sensors[i_sensor].append( sensor_voltage)
        return sensors

    def close(self):
        """

        @return:

        """
        self.analog_task.close()
        self.digital_task.close()


if __name__ == '__main__':
    import sys
    import platform

    # internal
    sys.path.append('../../')
    from arch.socket_arch.util import extract_devices

    if platform.system() == 'Linux':
        sys.path.append('/var/www/mswim/')
    else:
        sys.path.append('c:/mswim/')

    from mswim.settings import DEVICES

    task = AcquisitionTask(extract_devices(DEVICES)['Dev5'], 'continuous')
    while True:
        print(task.read())
        sleep(10)
        task.close()
        break
