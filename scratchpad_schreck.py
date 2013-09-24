import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy
import math
import itertools

f_pre = ['/Users/andalman/Dropbox/ConchisData/2013-07-10/f00601/f00601_2013-07-10-14-32-59.json',
         '/Users/andalman/Dropbox/ConchisData/2013-07-10/f00602/f00602_2013-07-10-14-32-59.json',
         '/Users/andalman/Dropbox/ConchisData/2013-07-10/f00603/f00603_2013-07-10-14-32-59.json',
         '/Users/andalman/Dropbox/ConchisData/2013-07-10/f00604/f00604_2013-07-10-14-32-59.json',
         '/Users/andalman/Dropbox/ConchisData/2013-07-10/f00605/f00605_2013-07-10-14-32-59.json',
         '/Users/andalman/Dropbox/ConchisData/2013-07-10/f00606/f00606_2013-07-10-14-32-59.json',
         '/Users/andalman/Dropbox/ConchisData/2013-07-10/f00607/f00607_2013-07-10-14-33-00.json',
         '/Users/andalman/Dropbox/ConchisData/2013-07-10/f00608/f00608_2013-07-10-14-33-00.json']

f_veh= ['/Users/andalman/Dropbox/ConchisData/2013-07-10/f00601/f00601_2013-07-10-15-05-42.json',
        '/Users/andalman/Dropbox/ConchisData/2013-07-10/f00602/f00602_2013-07-10-15-05-42.json',
        '/Users/andalman/Dropbox/ConchisData/2013-07-10/f00603/f00603_2013-07-10-15-05-42.json',
        '/Users/andalman/Dropbox/ConchisData/2013-07-10/f00604/f00604_2013-07-10-15-05-42.json',
        '/Users/andalman/Dropbox/ConchisData/2013-07-10/f00605/f00605_2013-07-10-15-05-42.json',
        '/Users/andalman/Dropbox/ConchisData/2013-07-10/f00606/f00606_2013-07-10-15-05-43.json',
        '/Users/andalman/Dropbox/ConchisData/2013-07-10/f00607/f00607_2013-07-10-15-05-43.json',
        '/Users/andalman/Dropbox/ConchisData/2013-07-10/f00608/f00608_2013-07-10-15-05-43.json']

f_sch = ['/Users/andalman/Dropbox/ConchisData/2013-07-10/f00601/f00601_2013-07-10-15-37-43.json',
         '/Users/andalman/Dropbox/ConchisData/2013-07-10/f00602/f00602_2013-07-10-15-37-43.json',
         '/Users/andalman/Dropbox/ConchisData/2013-07-10/f00603/f00603_2013-07-10-15-37-43.json',
         '/Users/andalman/Dropbox/ConchisData/2013-07-10/f00604/f00604_2013-07-10-15-37-43.json',
         '/Users/andalman/Dropbox/ConchisData/2013-07-10/f00605/f00605_2013-07-10-15-37-43.json',
         '/Users/andalman/Dropbox/ConchisData/2013-07-10/f00606/f00606_2013-07-10-15-37-44.json',
         '/Users/andalman/Dropbox/ConchisData/2013-07-10/f00607/f00607_2013-07-10-15-37-44.json',
         '/Users/andalman/Dropbox/ConchisData/2013-07-10/f00608/f00608_2013-07-10-15-37-44.json']

d_pre = np.array(aba.loadMultipleDataFiles(f_pre, arena_mm = None))
d_veh = np.array(aba.loadMultipleDataFiles(f_veh, arena_mm = None))
d_sch = np.array(aba.loadMultipleDataFiles(f_sch, arena_mm = None))

####### QUANTIFY CENTER TYPE
whichndx = [1,2,3,4,5,6,7]
compare = [[d_pre[whichndx],d_veh[whichndx]],[d_veh[whichndx], d_sch[whichndx]]]
trange = [[[1000,1700],[0,360]],  [[1000,1700],[0,360]]]
titles = ['Vehicle','Schreckstoff']
labels = [['Baseline','Vehicle_Start'],['Vehicle_End','Schreckstoff_Start']]
bins = np.linspace(0,300,50)
f = pyplot.figure(7)
f.set_facecolor('w')
mmperpixel=35.0/300
center=(150,150)
center_rad = 100
for compnum,comp in enumerate(compare):
    timeInCenter = np.zeros([len(comp),len(comp[0])])
    for condnum, cond in enumerate(comp):
        for fishnum, fish in enumerate(cond):
            tracking = aba.getTracking(fish)
            tracking[:,1]-=tracking[:,1].min()
            tracking[:,2]-=tracking[:,2].min()
            trel = trange[compnum][condnum] + tracking[0,0]
            tndx = np.logical_and(tracking[:,0]>=trel[0], tracking[:,0]<trel[1])
            heatmap, xedges, yedges = np.histogram2d(tracking[tndx,1],tracking[tndx,2],bins=bins,normed=True)
            xx,yy = np.meshgrid([x1+x2/2.0 for x1, x2 in itertools.izip(xedges[1:], xedges)],
                                [y1+y2/2.0 for y1, y2 in itertools.izip(yedges[1:], yedges)])
            xxndx,yyndx = np.meshgrid(range(len(xedges)-1),range(len(yedges)-1))
            centerndx = np.nonzero(np.sqrt(pow(xx-center[0],2)+pow(yy-center[1],2))<center_rad)
            timeInCenter[condnum][fishnum] = heatmap[xxndx[centerndx],yyndx[centerndx]].sum() / heatmap.sum()
    print timeInCenter
    (t,p) = scipy.stats.ttest_rel(timeInCenter[0,:],timeInCenter[1,:])
    pyplot.subplot(1,len(compare),1+compnum)
    pyplot.plot(range(len(comp)),timeInCenter,'o-b')
    pyplot.xlim([-0.5,len(comp)-0.5])
    pyplot.title('%s (paired t-test p=%f)'%(titles[compnum],p))
    pyplot.gca().xaxis.set_ticks(range(len(comp)))
    pyplot.gca().xaxis.set_ticklabels(labels[compnum])
    pyplot.ylabel('Prob in Center')

pyplot.show()

####### getMedianVelocity
whichndx = [0,1,2,3,4,5,6,7]
compare = [[d_pre[whichndx],d_veh[whichndx]],[d_veh[whichndx], d_sch[whichndx]]]
trange = [[[1000,1700],[0,360]],  [[1000,1700],[0,360]]]
titles = ['Vehicle','Schreckstoff']
labels = [['Baseline','Vehicle_Start'],['Vehicle_End','Schreckstoff_Start']]
bins = np.linspace(0,300,50)
f = pyplot.figure(6)
f.set_facecolor('w')
mmperpixel=35.0/300
for i,d in enumerate(compare):
    med_a = aba.getMedianVelMulti(d[0], trange[i][0], smoothWinLen=15)
    med_b = aba.getMedianVelMulti(d[1], trange[i][1], smoothWinLen=15)
    (t,p) = scipy.stats.ttest_rel(med_a,med_b)
    pyplot.subplot(1,len(compare),1+i)
    pyplot.plot([0,1],[med_a * mmperpixel,med_b * mmperpixel],'o-b')
    pyplot.xlim([-0.5,1.5])
    pyplot.ylim([0,5])
    pyplot.title('%s (paired t-test p=%f)'%(titles[i],p))
    pyplot.gca().xaxis.set_ticks([0,1])
    pyplot.gca().xaxis.set_ticklabels(labels[i])
    pyplot.ylabel('Median Velocity (mm/s)')

######## PLOT PATHS
whichndx = [1,2,3,5,6,7]
trange = [[0,1700],[0,1700],[0,1700]]
f = pyplot.figure(1)
f.set_facecolor('w')
titles = ['Baseline','Vehicle','Schreckstoff']
for i,d in enumerate([d_pre, d_veh, d_sch]):
    pyplot.subplot(1,3,i+1)
    map(aba.plotFishPath, d[whichndx], [trange[i]]*len(whichndx))
    pyplot.title(titles[i])

######## PLOT HEATMAPS
whichndx = [0,1,2,3,4,5,6,7]
trange = [[1000,1700],[0,360],[1000,1700],[0,360]]
titles = ['Baseline','Vehicle_Start','Vehicle_End','Schreckstoff_Start']
bins = np.linspace(0,300,50)
for i,d in enumerate([d_pre[whichndx],d_veh[whichndx],d_veh[whichndx], d_sch[whichndx]]):
    f = pyplot.figure(2+i, figsize=(10,4))
    f.set_facecolor('w')
    f.suptitle(titles[i])
    for j,f in enumerate(d):
        pyplot.subplot(2,math.ceil(len(whichndx)/2.0),j+1)
        tracking = aba.getTracking(f)
        tracking[:,1]-=tracking[:,1].min()
        tracking[:,2]-=tracking[:,2].min()
        aba.plotFishPathHeatmap(f,trange[i],bins=bins,tracking=tracking)
        pyplot.savefig('/Users/andalman/Dropbox/ConchisData/Schreckstoff/20130710_%s_heatmap_%dto%d.png'%
                       (titles[i],trange[i][0],trange[i][1]), dpi=300)

pyplot.show()
