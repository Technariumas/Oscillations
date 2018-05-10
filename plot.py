import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.fftpack import fft
from scipy.stats import norm
from astroML.fourier import PSD_continuous

tick_spacing = 4

data = np.genfromtxt("data/batch_3.txt", delimiter=",")
time = (data[:, 0])/1000
x = 9.8*(data[:, 1])/2048
y = 9.8*(data[:, 2])/2048
z = 9.8*(data[:, 3])/2048 # -- factory offset of this particular accelerator!

var = z


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
fk, PSD = PSD_continuous(time, var)

# plot the data and PSD
ax1.plot(time, var, '-', c=color, lw=1)
ax2.plot(fk, PSD, '-', c=color, lw=linewidth)

# vertical line marking the expected peak location
ax2.axhline(0, c='k', lw=0.3)
ax2.axvline(13.535, c='grey', lw=0.2, label="13.535 Hz")
plt.legend(loc=1, frameon=False)
#ax1.set_xlim(-25, 25)
#ax1.set_ylim(-0.1, 0.3001)

ax1.set_xlabel('$t$')
ax1.set_ylabel('$h(t)$')

ax1.yaxis.set_major_locator(plt.MultipleLocator(4))

ax2.set_xlim(0, 20)
ax2.set_ylim(0, 8000)

ax2.set_xlabel('$f$')
ax2.set_ylabel('$PSD(f)$')
plt.tight_layout()
plt.savefig('img/batch3_spectrogram_z.png')

