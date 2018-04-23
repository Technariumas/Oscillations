import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import signal

data = np.genfromtxt("data/LOGGER01.CSV", delimiter=",")
time = (data[:, 0])/1000


x = (data[:, 1])/2048
y = (data[:, 2])/2048
z = ((data[:, 3]) - 488)/2048 #183 -- factory offset of this particular accelerator!

x[np.where(np.abs(x) > 5)] = 0
y[np.where(np.abs(y) > 5)] = 0
z[np.where(np.abs(z) > 5)] = 0
print np.median(z)
#exit()
raw_acc = np.sqrt(x**2 + y**2 + z**2)

#print np.mean(x), np.mean(y), np.mean(z)
#exit()

raw_acc = raw_acc
dt = 0.01

vel = np.cumsum(raw_acc * dt) 




#print time[1]-time[0], time[501]-time[500], np.mean(np.diff(time))

fig = plt.figure()
f, ax = plt.subplots(4)
ax[0].plot(time, raw_acc, c="k", label="a")
ax[0].legend()

ax[1].plot(time, z, c="b", label="z")
ax[1].plot(time, y, c="g", label="y")
ax[1].plot(time, x, c="r", label="x")
ax[1].legend()
ax[2].hist(np.diff(time), bins=20)#plot(time, dist, c="k")

fft = np.abs(np.fft.fft(z))/(2*len(raw_acc))
freq = np.fft.fftfreq(len(raw_acc), dt)

#ax[3].plot(freq, fft, c="k", label="FFT")

f, t, Sxx = signal.spectrogram(x, 100)
ax[3].pcolormesh(t, f, Sxx)
#ax[3].axis([0, 50, 0, 1])
#ax[3].legend(loc=2)
plt.xlabel("Hz")
plt.tight_layout()
plt.savefig("img/spectrogram.png")

