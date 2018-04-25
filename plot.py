import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import signal
from wavelets import WaveletAnalysis
import matplotlib.ticker as ticker

tick_spacing = 4

data = np.genfromtxt("data/batch_1.txt", delimiter=",")
time = (data[:, 0])/1000


x = 9.8*(data[:, 1])/2048
y = 9.8*(data[:, 2])/2048
z = 9.8*((data[:, 3]) + 430)/2048 # -- factory offset of this particular accelerator!

#x[np.where(np.abs(x) > 5)] = 0
#y[np.where(np.abs(y) > 5)] = 0
#z[np.where(np.abs(z) > 5)] = 0
#print np.median(z)
#exit()
raw_acc = np.sqrt(x**2 + y**2 + z**2)

#print np.mean(x), np.mean(y), np.mean(z)
#exit()

dt = 0.005
print(np.mean(np.diff(time)))

vel = np.cumsum(raw_acc * dt) 

#print time[1]-time[0], time[501]-time[500], np.mean(np.diff(time))

fig = plt.figure()
f, ax = plt.subplots(2)

ax[0].axhline(0, c='k')

ax[0].plot(time, z, c="b", label="z")
ax[0].plot(time, y, c="g", label="y")
ax[0].plot(time, x, c="r", label="x")
ax[0].legend(loc=3)
fft = np.abs(np.fft.rfft(x, norm='ortho')/(2*len(x)))
freq = np.fft.rfftfreq(len(z), dt)
ax[1].plot(freq, fft, c="r", label="x")

#fft = np.abs(np.fft.fft(z))/(2*len(z))
#freq = np.fft.fftfreq(len(z), dt)
#ax[1].plot(freq, fft, c="b", label="z")



#f, t, Sxx = signal.spectrogram(x, 100)
#ax[3].pcolormesh(t, f, Sxx)
#ax[1].axis([0, 20, 0, 0.1])
ax[1].xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
ax[1].legend(loc=1)
plt.xlabel("Hz")
plt.tight_layout()
plt.savefig("img/spectrogram.png")

exit()
fig = plt.figure()
wa = WaveletAnalysis(raw_acc, dt=dt)

# wavelet power spectrum
power = wa.wavelet_power
# scales 
scales = wa.scales
# associated time vector
t = wa.time
T, S = np.meshgrid(time, scales)
d = plt.contourf(T, S, power, 400)
plt.colorbar(d)
plt.xlabel("Time, s")
plt.ylabel("Scale, s")

fig.savefig('img/test_wavelet_power_spectrum.png')

