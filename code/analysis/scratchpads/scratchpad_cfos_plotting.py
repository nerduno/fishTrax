##
##vanessa: read fiji text file output from point picker (aka cell counts)
##

import pylab
import matplotlib as mpl
import numpy as np

prefix = '/home/vburns/Dropbox/D-Lab Stuff/Leica/cFos blind data/'
c_list = ('blinds_cfos_20140116_blind1pts.txt',
          'blinds_cfos_20140116_blind2pts.txt')
e_list = ('blinds_cfos_20140116_blind3pts.txt',
          'blinds_cfos_20140116_blind4pts.txt')
bpre = '/home/vburns/Dropbox/D-Lab Stuff/Leica/'
blind_list = ('baselinepos1_pts.txt', 'baselinepos3_pts.txt', 'baselinepos4_pts.txt', 'baselinepos5_pts.txt', 'baselinepos6_pts.txt')

c_data = []
e_data = []
blinds = []

for i in range(len(c_list)):
    c_data.append(np.genfromtxt(prefix + c_list[i]))
    c_data[i] = c_data[i][1:] #remove header line
for k in range(len(e_list)): 
    e_data.append(np.genfromtxt(prefix + e_list[k]))
    e_data[k] = e_data[k][1:]

for i in range(len(blind_list)):
    blinds.append(np.genfromtxt(bpre + blind_list[i]))
    blinds[i] = blinds[i][1:] #remove header line

#generate information
def generateinfo(dataset,bins):
    numName = []
    xName = []
    yName = []
    histData = []
    for i in range(len(dataset)): 
        numName.append(len(dataset[i]))
        xName.append(dataset[i][:,1])
        yName.append(dataset[i][:,2])
        hist, edges = np.histogram(dataset[i][:,1],bins)
        histData.append(hist)
    return numName, xName, yName,histData

bins =100
[cNum, cX, cY, cH] = generateinfo(c_data,bins)
[eNum, eX, eY, eH] = generateinfo(e_data,bins)
[bNum, bX, bY, bH] = generateinfo(blinds, bins)
'''
#plot number of cells
pylab.figure()
pylab.suptitle('cFos Cell Counts')
ax = pylab.subplot(111)
pylab.plot(0,[cNum],'ob',lw=2)
pylab.plot(1,[eNum],'or',lw=2)
pylab.axhline(np.mean(cNum), xmin=.2, xmax=.3,color='k', lw=3)
pylab.axhline(np.mean(eNum), xmin=.7, xmax=.8,color='k', lw=3)
pylab.ylim((0,150))
pylab.xlim((-.5,1.5))
pylab.ylabel('Number of Cells')
ax.set_xticks((0,1))
ax.set_xticklabels(('control', 'experimental'))
'''
pylab.figure()
pylab.suptitle('cFos Cell Counts')
ax = pylab.subplot(111)
pylab.plot(0, [bNum],'og', lw=2)
pylab.plot(1,[cNum],'ob',lw=2)
pylab.plot(2,[eNum],'or',lw=2)
pylab.axhline(np.mean(bNum), xmin=.11, xmax=.22, color='k', lw=3)
pylab.axhline(np.mean(cNum), xmin=.44, xmax=.56,color='k', lw=3)
pylab.axhline(np.mean(eNum), xmin=.77, xmax=.9,color='k', lw=3)
pylab.ylim((0,150))
pylab.xlim((-.5,2.5))
pylab.ylabel('Number of Cells')
ax.set_xticks((0,1,2))
ax.set_xticklabels(('baseline', 'control', 'experimental'))
'''
#generate distribution
pylab.figure()
pylab.figure('cFos Distribution')
ax2=pylab.subplot(111)
pylab.step(np.arange(bins),np.mean(cH, axis=0), 'b')
pylab.step(np.arange(bins),np.mean(eH,axis=0), 'r')
pylab.ylabel('Average number of cells in region')
'''
pylab.show()
