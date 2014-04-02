import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy
import os

control = ['/home/vburns/Dropbox/ConchisData/2014-02-20/f01039/f01039_2014-02-20-16-23-30.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-20/f01040/f01040_2014-02-20-16-23-19.json']
control = aba.loadMultipleDataFiles(control)

experimental =  [ '/home/vburns/Dropbox/ConchisData/2014-02-20/f01037/f01037_2014-02-20-15-45-35.json',
 '/home/vburns/Dropbox/ConchisData/2014-02-20/f01038/f01038_2014-02-20-15-45-43.json']
experimental = aba.loadMultipleDataFiles(experimental)

print "Done loading fish."

datanames = ['985', '986']

#data = [experimental]

data = [control]

