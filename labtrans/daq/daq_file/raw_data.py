# -*- coding: utf-8 -*-
from __future__ import division, print_function
import copy
from datetime import timedelta


def save_file(acq, file_path='/tmp/raw_data.txt'):
    delta = 1/5000

    def next_time(initial_time, float_delta):
        delta = timedelta(seconds=float_delta)
        _time = copy.deepcopy(initial_time)
        while True:
            yield str(_time)[11:].replace('.', ',')
            _time += delta

    with open(file_path, 'w') as f:
        # clear the file
        f.write('')

    with open(file_path, 'a') as f:
        channels = 32 if acq.sensor_type == 1 else 16

        channel_time = next_time(acq.date_time.value, delta)

        f.write('Python Measurement\n')
        f.write('Writer_Version\t3\n')
        f.write('Reader_Version\t3\n')
        f.write('Separator_Version\tTab\n')
        f.write('Decimal_Separator\t,\n')
        f.write('Multi_Headings\tNo\n')
        f.write('X_Columns\tOne\n')
        f.write('Time_Pref\tAbsolute\n')
        f.write('Operator\tadmin\n')
        f.write('Date\t%s\n' % str(acq.date_time.value)[:10].replace('-', '/'))
        f.write('Time\t%s\n' % str(acq.date_time.value)[11:].replace('.', ','))
        f.write('***End_of_Header***\t\n\n')
        f.write('Channels\t%s\n' % channels)
        f.write('Samples\t%s\n' % ('15000\t' * channels))
        f.write(
            'Date\t%s\n' % (
                (str(acq.date_time.value)[:10].replace('-', '/') +
                 '\t') * channels
            )
        )
        f.write(
            'Time\t%s\n' %
            '\t'.join([channel_time.next() for _ in range(channels)])
        )
        f.write('Y_Unit_Label\t%s\n' % ('Volts\t' * channels))
        f.write('X_Dimension\t%s\n' % ('Time\t' * channels))
        f.write('X_0\t%s\n' % ('0,0000000000000000E+0\t' * channels))
        f.write(
            'Delta_X\t%s\n' % (
                (str(delta).replace('.', ',') + '\t') * channels
            )
        )
        f.write('***End_of_Header***\t%s\n' % ('\t' * channels))
        f.write(
            'X_Value\t%s\t1\tComment\n' %
            '\t'.join(['Voltage_%s' % x for x in range(channels)])
        )

        counter = 0.
        time, data = acq.data.array()

        total = len(data[0])

        for i in range(total):
            columns = '\t'.join(
                [str(data[s][i]).replace('.', ',') for s in range(channels)]
            )
            line = '%s\t%s\n' % (('%f' % counter).replace('.', ','), columns)
            counter += delta
            f.write(line)
