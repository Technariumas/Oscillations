import matplotlib.pyplot as plt
import numpy as np
import math
import waipy
from waipy import wavelet_plot

tick_spacing = 4

data = np.genfromtxt("data/batch_4.txt", delimiter=",")[5000:10000]
time = (data[:, 0])#/1000

x = 9.8*(data[:, 1])/2048
y = 9.8*(data[:, 2])/2048
z = 9.8*((data[:, 3]))/2048 # -- factory offset of this particular accelerometer!

var = x

data_norm = waipy.normalize(var)
alpha = np.corrcoef(data_norm[0:-1], data_norm[1:])[0,1]; 
result = waipy.cwt(data_norm, 5, 0, 0.0625, 1, 36, alpha, 6, mother='Morlet', name="name")
waipy.wavelet_plot("img/batch_4.png", time, data_norm, 0.03125, result); 


"""
    CONTINUOUS WAVELET TRANSFORM
    pad = 1         # pad the time series with zeroes (recommended)
    dj = 0.25       # this will do 4 sub-octaves per octave
    s0 = 2*dt       # this says start at a scale of 6 months
    j1 = 7/dj       # this says do 7 powers-of-two with dj sub-octaves each
    lag1 = 0.72     # lag-1 autocorrelation for red noise background
    param = 6
    mother = 'Morlet'
"""
