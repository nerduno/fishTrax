import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import scipy
import os

#control fish moved to shock water
control_first = [
 '/home/vburns/Dropbox/ConchisData/2014-03-06/f01105/f01105_2014-03-06-10-20-43.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-06/f01106/f01106_2014-03-06-10-20-39.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-06/f01107/f01107_2014-03-06-10-20-34.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-06/f01108/f01108_2014-03-06-10-20-28.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-06/f01109/f01109_2014-03-06-10-20-23.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-06/f01110/f01110_2014-03-06-10-20-16.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-06/f01111/f01111_2014-03-06-10-20-11.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-06/f01112/f01112_2014-03-06-10-20-06.json',
]
control_first = aba.loadMultipleDataFiles(control_first)

control_sec =[
'/home/vburns/Dropbox/ConchisData/2014-03-06/f01105/f01105_2014-03-06-11-16-23.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-06/f01106/f01106_2014-03-06-11-16-29.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-06/f01107/f01107_2014-03-06-11-16-34.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-06/f01108/f01108_2014-03-06-11-16-40.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-06/f01109/f01109_2014-03-06-11-16-48.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-06/f01110/f01110_2014-03-06-11-16-53.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-06/f01111/f01111_2014-03-06-11-17-01.json',
 '/home/vburns/Dropbox/ConchisData/2014-03-06/f01112/f01112_2014-03-06-11-17-08.json',
]
control_sec = aba.loadMultipleDataFiles(control_sec)

print "Done loading fish."

datanames = ['Control fish moved to shock water']

data = [control_first, control_sec]

