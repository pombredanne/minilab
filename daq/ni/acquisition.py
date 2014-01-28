from continuous import DigitalContinuousTask, AnalogContinuousTask
from datetime import datetime
from collections import defaultdict


def calc_time(delta_t, N):
    timestamp = [datetime.now()]

    def next_time(tstamp):
        _ts = tstamp[0]
        tstamp[0] += delta_t
        return _ts

    return [next_time(timestamp) for _ in range(N)]


class AcquisitionTask():
    """

    """
    ACQ_TYPE = {
        'test': 2,
        'calibration': 3,
        'statistic': 1
    }

    trigger_task = None
    channel = None
    is_simulated = None
    task_device = None
    acquisition_type = None

    def __init__(
        self, trigger_channel='', channels=[],
        minv=0, maxv=0, rate=2000, seconds_to_acquire=1,
        plotting=False, sensor_type=0, temperature_sensor=False,
        temperature_path=None, is_simulated=False,
        acquisition_type=None, acquisition_mode=''
    ):
        """

        @return:

        """
        self.channels = channels

        self.sensor_type = sensor_type
        self.plotting = plotting
        self.temperature_sensor = temperature_sensor
        self.temperature_path = temperature_path
        self.is_simulated = is_simulated
        self.acquisition_type = acquisition_type


        if acquisition_mode == 'continuous':
            DIGITAL_TASK = DigitalContinuousTask
            ANALOG_TASK = AnalogContinuousTask
        else:
            raise Exception('Invalid Acquisition Mode.')

        DIGITAL_TASK(
            channels=[trigger_channel],
            samples_per_channel=1
        )

        self.task_device = {}
        for _id, chans in enumerate(self.channels):
            sorted_channels = [
                c for c in sorted(chans, key=lambda x: chans[x])
            ]
            self.task_device[_id] = AcquisitionFiniteTask(
                physical_channel=sorted_channels,
                rate=rate,
                minv=minv,
                maxv=maxv,
                seconds_to_acquire=seconds_to_acquire
            )

    def ready(self):
        acq_datetime = datetime.now()

        for _id, chans in enumerate(self.channels):
            header = {
                'acq_datetime': acq_datetime,
                'temperature': {'5cm': None, '17cm': None},
                'channels': len(chans),
                'acquisition_type': self.ACQ_TYPE[self.acquisition_type]
            }

            task_dev = self.task_device[_id]

            if self.temperature_sensor:
                # update header temperature
                for t in [5, 17]:
                    with open('%stemp%s' % (self.temperature_path, t)) as f:
                        header['temperature']['%scm' % t] = float(f.read()) * 10

            data, acq_time = task_dev.read()

            sensors = defaultdict(dict)
            for chan_i, chan_data in data.items():
                i_sensor = chans[chan_i]
                for t, sensor_voltage in enumerate(chan_data):
                    # changed to return use the same baseline
                    sensor_time = acq_time[t]

                    if not sensors[i_sensor]:
                        sensors[i_sensor] = defaultdict(dict)
                    sensors[i_sensor][sensor_time] = sensor_voltage

            if self.plotting:
                self.plot(data)

            # save the data
            AcquisitionModel(
                header, sensors, sensor_type=self.sensor_type
            ).save()

    def clear(self):
        """

        @return:

        """
        self.trigger_task.clear()

    def plot(self, data):
        plt.axis([0, self.samples_per_channel - 1, -2, 5.5])

        for data_sensor in data:
            plt.plot(data_sensor)

        plt.grid()
        plt.show()


if __name__ == '__main__':
    import sys
    import platform

    # internal
    if platform.system() == 'Linux':
        sys.path.append('/var/www/mswim/')
    else:
        sys.path.append('c:/mswim/')

    from mswim import settings