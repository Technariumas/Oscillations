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
from pandas.tseries import converter as pdtc


input_file = sys.argv[1]
output_filename = input_file[5:-4]
acc_axis = sys.argv[2]
tick_spacing = 4

data = np.genfromtxt(input_file, dtype=[('time', 'U028'), ('seconds', float), ('x', float),  ('y', float),  ('z', float)], delimiter=",")[6:]#offset at the beginning of 05.11 files
time = np.array(data['time'], dtype='datetime64')
seconds = data['seconds']/1000
seconds = seconds - seconds[0]
print(np.mean(np.diff(seconds)))

print(seconds.dtype)


acc = data[acc_axis]
#acc-=np.mean(acc)

print(acc.dtype)

#acc = signal.filtfilt(B,A, acc)
#vel = integrate.cumtrapz(acc, time, initial=0)
#vel-=np.mean(acc)
#var = integrate.cumtrapz(vel, time, initial=0)


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
# plot the data and PSD
ax1.plot(time, acc, '-', c=color, lw=1)
ax1.axhline(0, c='k', lw=0.3)

# compute the PSD
try:
	fk, PSD = PSD_continuous(seconds, acc)
except ValueError:
	seconds, acc = seconds[1:], acc[1:] #number of samples must be even
	fk, PSD = PSD_continuous(seconds, acc)

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
ax2.set_ylim(0, 8000)

ax2.set_xlabel('$f$')
ax2.set_ylabel('$PSD(f)$')
plt.tight_layout()
plt.savefig('img/'+output_filename+'_'+acc_axis+'.png')

