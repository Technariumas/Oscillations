#usage: python3 plot.py <input_file> <axis>

import matplotlib.pyplot as plt
import numpy as np
import math
import sys
from scipy.fftpack import fft
from scipy import integrate
from scipy.stats import norm
from astroML.fourier import PSD_continuous
import scipy.signal as signal
from datetime import datetime, timezone

def utc_to_local(utc_t):
    return utc_t.replace(tzinfo=timezone.utc).astimezone(tz=None)

# First, design the Buterworth filter
#N  = 2    # Filter order
#Wn = 0.05 # Cutoff frequency
#B, A = signal.butter(N, Wn, btype='high', output='ba')

input_file = sys.argv[1]
output_filename = input_file[5:-4]
acc_axis = sys.argv[2]
tick_spacing = 4

data = np.genfromtxt(input_file, skip_header = 1, delimiter=",", dtype = int)#[132*200:133*200]
time = (data[:, 0])#/1000

with open(input_file) as f:
    start_time = utc_to_local(datetime.strptime(f.readline().strip(), '%Y-%m-%d %H:%M:%S.%f'))

start_offset = time - time[0]
print(start_offset[1])

timestamps = np.empty((time.shape), dtype = 'datetime64')
timestamps = np.datetime64(start_time) + start_offset



if acc_axis == 'x':
	acc = 9.8*(data[:, 1])/2048
elif acc_axis == 'y':
	acc = 9.8*(data[:, 2])/2048
elif acc_axis == 'z':
	acc = 9.8*(data[:, 3] - 150)/2048 # -- factory offset of this particular accelerometer!
else:
	print("Wrong axis argument!")
	exit()


#acc-=np.mean(acc)

#acc = signal.filtfilt(B,A, acc)
#vel = integrate.cumtrapz(acc, time, initial=0)
#vel-=np.mean(acc)
#var = integrate.cumtrapz(vel, time, initial=0)
dt = 0.005


#----------------------------------------------------------------------
# This function adjusts matplotlib settings for a uniform feel in the textbook.
# Note that with usetex=True, fonts are rendered with LaTeX.  This may
# result in an error if LaTeX is not installed on your system.  In that case,
# you can set usetex to False.
from astroML.plotting import setup_text_plots
setup_text_plots(fontsize=8, usetex=True)

#------------------------------------------------------------
# Draw the data

#------------------------------------------------------------
# plot the results
fig = plt.figure(figsize=(10, 7.5))
fig.subplots_adjust(hspace=0.25)
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)


color = 'black'
linewidth = 1

# compute the PSD
fk, PSD = PSD_continuous(time, acc)

# plot the data and PSD
ax1.plot(time, acc, '-', c=color, lw=1)
ax1.axhline(0, c='k', lw=0.3)

ax2.plot(fk, PSD, '-', c=color, lw=linewidth)

# vertical line marking the expected peak location
ax2.axvline(13.535, c='grey', lw=0.2, label="13.535 Hz")
plt.legend(loc=1, frameon=False)
#ax1.set_xlim(-25, 25)
#ax1.set_ylim(-0.1, 0.3001)
ax1.set_xlabel('$t$')
ax1.set_ylabel('$h(t)$')

#ax1.yaxis.set_major_locator(plt.MultipleLocator(1))

ax2.set_xlim(0, 50)
ax2.set_ylim(0, 5000)

ax2.set_xlabel('$f$')
ax2.set_ylabel('$PSD(f)$')
plt.tight_layout()
plt.savefig('img/'+output_filename+'_'+acc_axis+'.png')

