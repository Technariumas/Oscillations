#usage: python3 get_timestamps.py <input_file>

import numpy as np
import math
import sys
from datetime import datetime, timezone

def utc_to_local(utc_t):
    return utc_t.replace(tzinfo=timezone.utc).astimezone(tz=None)

input_file = sys.argv[1]

data = np.genfromtxt(input_file, skip_header = 1, delimiter=",", dtype = int)#[132*200:133*200]
seconds = data[:, 0]

x = 9.8*(data[:, 1])/2048
y = 9.8*(data[:, 2])/2048
z = 9.8*(data[:, 3] - 150)/2048

with open(input_file) as f:
    start_time = datetime.strptime(f.readline().strip(), '%Y-%m-%d %H:%M:%S.%f')
    real_time = utc_to_local(start_time)
    output_filename = real_time.strftime("%Y%m%d-%H_%M_%S")

start_offset = seconds - seconds[0]
timestamps = np.datetime64(start_time) + start_offset #microseconds
data = np.zeros(timestamps.size, dtype=[('time', 'U028'), ('seconds', float), ('x', float),  ('y', float),  ('z', float)])
data['time'] = timestamps
data['seconds'] = seconds
data['x'] = x
data['y'] = y
data['z'] = z
np.savetxt('data/'+output_filename+'_timestamps.csv', data, delimiter = ',', fmt="%s28, %i, %.12f, %.12f, %.12f")
