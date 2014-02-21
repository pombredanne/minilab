from __future__ import print_function
from collections import defaultdict
from time import sleep

from simulated import DigitalSimulatedTask, AnalogSimulatedTask
from callback import CallbackTask

try:
    from continuous import DigitalContinuousTask, AnalogContinuousTask
except Exception as e:
    from simulated import DigitalSimulatedTask as DigitalContinuousTask
    from simulated import AnalogSimulatedTask as AnalogContinuousTask


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

    def __init__(
            self, device={}, acquisition_mode='',
            samples_per_channel=1, callback=()
    ):
        """

        @return:

        """
        self.device = device

        if acquisition_mode == 'callback':
            self.analog_task = CallbackTask(
                physical_channels=device['analog'],
                digital_physical_channels=device['digital'],
                rate=device['rate'],
                minv=device['minv'],
                maxv=device['maxv'],
                samples_per_channel=samples_per_channel
            )
            self.analog_task.bind(callback)
        else:
            if acquisition_mode == 'continuous':
                DIGITAL_TASK = DigitalContinuousTask
                ANALOG_TASK = AnalogContinuousTask
            elif acquisition_mode == 'simulated':
                DIGITAL_TASK = DigitalSimulatedTask
                ANALOG_TASK = AnalogSimulatedTask
            else:
                raise Exception('Invalid Acquisition Mode.')

            self.digital_task = DIGITAL_TASK(
                physical_channels=device['digital'],
                rate=device['rate'],
                samples_per_channel=samples_per_channel
            )

            self.analog_task = ANALOG_TASK(
                physical_channels=device['analog'],
                rate=device['rate'],
                minv=device['minv'],
                maxv=device['maxv'],
                seconds_to_acquire=device['seconds_to_acquire'],
                samples_per_channel=samples_per_channel
            )

    def read(self):
        signals = self.read_analog()
        signals.update(self.read_digital())
        return signals

    def read_analog(self):
        data = self.analog_task.read()

        sensors = defaultdict(dict)
        for chan_i, chan_data in data.items():
            for i, sensor_voltage in enumerate(chan_data):
                # changed to return use the same baseline
                if not sensors[chan_i]:
                    sensors[chan_i] = []
                sensors[chan_i] += [sensor_voltage]
        return sensors

    def read_digital(self):
        if not self.digital_task.physical_channels:
            return {}

        data = self.digital_task.read()

        sensors = defaultdict(dict)
        for chan_i, chan_data in data.items():
            for i, sensor_voltage in enumerate(chan_data):
                # changed to return use the same baseline
                if not sensors[chan_i]:
                    sensors[chan_i] = []
                sensors[chan_i] += [sensor_voltage]
        return sensors

    def run(self):
        self.analog_task.run()

    def close(self):
        """

        @return:

        """
        try:
            self.analog_task.close()
            self.digital_task.close()
        except:
            pass


if __name__ == '__main__':
    import platform
    import sys

    # internal
    sys.path.append('../../')

    from arch.libs.util import extract_devices
    from acquisition import AcquisitionTask

    if platform.system() == 'Linux':
        sys.path.append('/var/www/mswim/')
    else:
        sys.path.append('c:/mswim/')

    def test_callback():
        from gui.plotter.async_chart import DaqMultiPlotter
        from mswim.settings import DEVICES

        def callback1(dev_name):
            def _cb(interval, data):
                DaqMultiPlotter.send_data({dev_name: data})

            return _cb

        def callback2(dev_name):
            def _cb(interval, data):
                DaqMultiPlotter.send_data({dev_name: data})
                DaqMultiPlotter.show()
            return _cb


        chunk = 1000

        groups_available = ['Dev1', 'Dev2', 'Dev5', 'Dev4']
        callback_list = {
            'Dev1': callback1,
            'Dev2': callback1,
            'Dev5': callback1,
            'Dev4': callback2
        }

        DaqMultiPlotter.configure(chunk, groups_available)

        tasks = []

        # device={}, acquisition_mode='',
        # samples_per_channel=1, callback=()

        for dev_name in groups_available:
            tasks.append(AcquisitionTask(
                device=extract_devices(DEVICES)[dev_name],
                acquisition_mode='callback',
                samples_per_channel=chunk,
                callback=callback_list[dev_name](dev_name)
            ))

        DaqMultiPlotter.start()

        for task in tasks:
            task.run()

        while True:
            try:
                raw_input(
                    'Acquiring samples continuously. ' +
                    'Press CTRL + C to interrupt\n'
                )
            except KeyboardInterrupt:
                break

        for task in tasks:
            task.close()

        DaqMultiPlotter.stop()

    def test():
        test_callback()

    test()