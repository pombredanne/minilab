# -*- coding:utf-8 -*-
import re
import cProfile

def acq_file_datetime(file_path):
    patt_date = re.compile('^Date\s+([0-9]{4}/[0-9]{2}/[0-9]{2})')
    patt_time = re.compile('^Time\s+([0-9]{2}:[0-9]{2}:[0-9]{2})')

    with open(file_path) as f:
        data = f.read().splitlines()[:23]

    _date = None
    _time = None
    data_header = 0

    for line in data:
        if line.strip() == '***End_of_Header***':
            data_header += 1

        if data_header == 0:
            continue
        elif data_header == 2:
            return '%s %s' % (_date, _time)

        if line.startswith('Date'):
            _date = patt_date.match(line.replace('\t', ' ')).group(1)

        if line.startswith('Time'):
            _time = patt_time.match(line.replace('\t', ' ')).group(1)


def acq_file_datetime2(file_path):
    patt_date = re.compile('Date\s+([0-9]{4}/[0-9]{2}/[0-9]{2})')
    patt_time = re.compile('Time\s+([0-9]{2}:[0-9]{2}:[0-9]{2})')

    with open(file_path) as f:
        data = '-'.join(f.read().splitlines()[15:20]).replace('\t', ' ')

    _date = patt_date.search(data).group(1)
    _time = patt_time.search(data).group(1)

    return '%s %s' % (_date, _time)


def test():
    path = '/home/ivan/Público/data_test/'
    fs = [(path + '2012_03_20_10_10_14_polimero.txt', '2012/03/20 10:10:22'),
          (path + '2012_03_20_10_10_14_quartzo.txt', '2012/03/20 10:10:17'),
          (path + '2012_03_20_10_12_58_polimero.txt', '2012/03/20 10:13:06'),
          (path + '2012_03_20_10_12_58_quartzo.txt', '2012/03/20 10:13:01'),
          (path + '20120704_132513_piezoQuartzo_DadosBrutos.txt',
           '2012/07/04 13:25:17'),
          (path + '20120707_150028_piezoQuartzo_DadosBrutos.txt',
           '2012/07/07 15:00:32')]

    for f in fs:
        result = acq_file_datetime2(f[0])
        assert result == f[1]

    return True


def test2():
    path = '/home/ivan/Público/data_test/'
    fs = path + '2012_03_20_10_10_14_polimero.txt'

    acq_file_datetime2(fs)



if __name__ == '__main__':
    cProfile.run('test()')