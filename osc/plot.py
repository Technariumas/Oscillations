import matplotlib.pyplot as plt
import numpy as np
import math

data = np.genfromtxt("data/LOGGER16.CSV", delimiter=",")
time = (data[:, 0]-data[:, 0][0])/1000
x = (data[:, 1]/1024)
y = (data[:, 2]/1024)
z = ((data[:, 3])/1024)

raw_acc = np.sqrt(x**2 + y**2 + z**2)

raw_acc = raw_acc
dt = 0.01

vel = np.cumsum(raw_acc * dt) 

#dist = np.cumsum(vel)

#print time[1]-time[0], time[501]-time[500], np.mean(np.diff(time))

fig = plt.figure()
f, ax = plt.subplots(4)
ax[0].plot(time, raw_acc, c="k")

ax[1].plot(time, x, c="r")
ax[1].plot(time, y, c="g")

ax[1].plot(time, z, c="b")
ax[2].hist(np.diff(time))#plot(time, dist, c="k")

fft = np.abs(np.fft.fft(z))/(2*len(raw_acc))
freq = np.fft.fftfreq(len(raw_acc), dt)

ax[3].plot(freq, fft, c="k")
ax[3].axis([0, 50, 0, 1])
plt.savefig("img/res.png")

