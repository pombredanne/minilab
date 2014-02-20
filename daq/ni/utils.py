from datetime import datetime


def calculate_time_sequence(delta_t, quantity):
    timestamp = [datetime.now()]

    def next_time(_timestamp):
        _ts = _timestamp[0]
        _timestamp[0] += delta_t
        return _ts

    return [next_time(timestamp) for _ in range(quantity)]