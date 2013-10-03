import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy

#15 acclimation, 30 shock bouts, 5 min post.
e_omr= [
#        '/home/vburns/Dropbox/ConchisData/2013-09-27/f00609/f00609_2013-09-27-10-23-16.json', #side 52 dead
	'/home/vburns/Dropbox/ConchisData/2013-09-27/f00610/f00610_2013-09-27-10-23-11.json',
	'/home/vburns/Dropbox/ConchisData/2013-09-27/f00611/f00611_2013-09-27-10-23-07.json',
	'/home/vburns/Dropbox/ConchisData/2013-09-27/f00612/f00612_2013-09-27-10-23-02.json',
	'/home/vburns/Dropbox/ConchisData/2013-09-27/f00613/f00613_2013-09-27-10-22-56.json',
	'/home/vburns/Dropbox/ConchisData/2013-09-27/f00614/f00615_2013-09-27-10-22-51.json',
	'/home/vburns/Dropbox/ConchisData/2013-09-27/f00615/f00615_2013-09-27-10-22-46.json',
	'/home/vburns/Dropbox/ConchisData/2013-09-27/f00616/f00616_2013-09-27-10-22-42.json', #current imbalance
	'/home/vburns/Dropbox/ConchisData/2013-09-27/f00617/f00617_2013-09-27-10-32-05.json',
	'/home/vburns/Dropbox/ConchisData/2013-09-27/f00618/f00616_2013-09-27-10-31-57.json',
	'/home/vburns/Dropbox/ConchisData/2013-09-27/f00619/f00619_2013-09-27-10-31-48.json',#current imbalance
        '/home/vburns/Dropbox/ConchisData/2013-09-27/f00620/f00620_2013-09-27-10-31-38.json',
	'/home/vburns/Dropbox/ConchisData/2013-09-27/f00621/f00621_2013-09-27-10-31-30.json', #current imbalance
	'/home/vburns/Dropbox/ConchisData/2013-09-27/f00622/f00622_2013-09-27-10-31-22.json',
	'/home/vburns/Dropbox/ConchisData/2013-09-27/f00623/f00623_2013-09-27-10-31-15.json',
	'/home/vburns/Dropbox/ConchisData/2013-09-27/f00624/f00624_2013-09-27-10-31-05.json'
]
e_omr = aba.loadMultipleDataFiles(e_omr)

e_post_omr = [
#    '/home/vburns/Dropbox/ConchisData/2013-09-27/f00609/f00609_2013-09-27-11-25-24.json',
    '/home/vburns/Dropbox/ConchisData/2013-09-27/f00610/f00610_2013-09-27-11-25-49.json',
    '/home/vburns/Dropbox/ConchisData/2013-09-27/f00611/f00611_2013-09-27-11-26-04.json',
    '/home/vburns/Dropbox/ConchisData/2013-09-27/f00612/f00612_2013-09-27-11-26-20.json',
    '/home/vburns/Dropbox/ConchisData/2013-09-27/f00613/f00613_2013-09-27-11-26-35.json',
    '/home/vburns/Dropbox/ConchisData/2013-09-27/f00614/f00614_2013-09-27-11-27-06.json',
    '/home/vburns/Dropbox/ConchisData/2013-09-27/f00615/f00615_2013-09-27-11-27-22.json',
    '/home/vburns/Dropbox/ConchisData/2013-09-27/f00616/f00616_2013-09-27-11-27-37.json',
    '/home/vburns/Dropbox/ConchisData/2013-09-27/f00617/f00617_2013-09-27-11-28-37.json',
    '/home/vburns/Dropbox/ConchisData/2013-09-27/f00618/f00618_2013-09-27-11-28-52.json',
    '/home/vburns/Dropbox/ConchisData/2013-09-27/f00619/f00619_2013-09-27-11-29-07.json',
    '/home/vburns/Dropbox/ConchisData/2013-09-27/f00620/f00620_2013-09-27-11-29-17.json',
    '/home/vburns/Dropbox/ConchisData/2013-09-27/f00621/f00621_2013-09-27-11-29-31.json',
    '/home/vburns/Dropbox/ConchisData/2013-09-27/f00622/f00622_2013-09-27-11-29-45.json',
    '/home/vburns/Dropbox/ConchisData/2013-09-27/f00623/f00623_2013-09-27-11-29-56.json',
    '/home/vburns/Dropbox/ConchisData/2013-09-27/f00624/f00624_2013-09-27-11-30-07.json'
]
e_post_omr = aba.loadMultipleDataFiles(e_post_omr)

c_omr = [
'/home/vburns/Dropbox/ConchisData/2013-09-27/f00625/f00625_2013-09-27-14-19-33.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00626/f00626_2013-09-27-14-19-26.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00627/f00627_2013-09-27-14-19-21.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00628/f00628_2013-09-27-14-19-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00629/f00629_2013-09-27-14-19-13.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00630/f00630_2013-09-27-14-19-08.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00631/f00631_2013-09-27-14-19-04.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00632/f00632_2013-09-27-14-18-59.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00633/f00633_2013-09-27-14-22-01.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00634/f00634_2013-09-27-14-22-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00635/f00635_2013-09-27-14-22-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00636/f00636_2013-09-27-14-22-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00637/f00637_2013-09-27-14-22-43.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00638/f00638_2013-09-27-14-22-53.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00639/f00639_2013-09-27-14-23-03.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00640/f00640_2013-09-27-14-23-12.json'
]
c_omr = aba.loadMultipleDataFiles(c_omr)

c_post_omr = [
'/home/vburns/Dropbox/ConchisData/2013-09-27/f00625/f00625_2013-09-27-15-17-56.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00626/f00626_2013-09-27-15-17-43.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00627/f00627_2013-09-27-15-17-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00628/f00628_2013-09-27-15-17-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00629/f00629_2013-09-27-15-17-06.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00630/f00630_2013-09-27-15-16-55.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00631/f00631_2013-09-27-15-16-41.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00632/f00632_2013-09-27-15-16-31.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00633/f00633_2013-09-27-15-19-37.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00634/f00634_2013-09-27-15-19-13.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00635/f00635_2013-09-27-15-19-03.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00636/f00636_2013-09-27-15-18-53.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00637/f00637_2013-09-27-15-18-43.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00638/f00638_2013-09-27-15-18-32.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00639/f00639_2013-09-27-15-18-20.json',
 '/home/vburns/Dropbox/ConchisData/2013-09-27/f00640/f00640_2013-09-27-15-18-08.json'
]
c_post_omr = aba.loadMultipleDataFiles(c_post_omr)

#omr analysis
[eBaseMaxDist, eBaseTotalDist, eBaseFrac] = aba.getAvgOMRScoreMulti(e_omr, stateRange=[3,3])
[eEndMaxDist, eEndTotalDist, eEndFrac] = aba.getAvgOMRScoreMulti(e_omr, stateRange=[8,8])
[cBaseMaxDist, cBaseTotalDist, cBaseFrac] = aba.getAvgOMRScoreMulti(c_omr, stateRange=[3,3])
[cEndMaxDist, cEndTotalDist, cEndFrac] = aba.getAvgOMRScoreMulti(c_omr, stateRange=[8,8])

#get info for nonOMR times
[cBaseMaxDistNon, cBaseTotalDistNon, cBaseFracNon] = aba.getAvgOMRScoreMulti(c_omr, stateRange=[3,3],useOMR=False)
[cEndMaxDistNon, cEndTotalDistNon, cEndFracNon] = aba.getAvgOMRScoreMulti(c_omr, stateRange=[8,8], useOMR=False)
[eBaseMaxDistNon, eBaseTotalDistNon, eBaseFracNon] = aba.getAvgOMRScoreMulti(e_omr, stateRange=[3,3],useOMR=False)
[eEndMaxDistNon, eEndTotalDistNon, eEndFracNon] = aba.getAvgOMRScoreMulti(e_omr, stateRange=[8,8], useOMR=False)

#velocity analysis 
sm = 15; #smooth over 15 frames.
endWinLen = 5 * 60; #last five minutes
eBaseVel = aba.getMedianVelMulti(e_omr, (0, 15*60), smoothWinLen = sm)
eEndVel = aba.getMedianVelMulti(e_omr, tRange=[-endWinLen,-0], smoothWinLen=sm)
eEndVel_2a = aba.getMedianVelMulti(e_post_omr, (0,900), smoothWinLen=sm)
eEndVel_2b = aba.getMedianVelMulti(e_post_omr, (900,1800), smoothWinLen=sm)
cBaseVel = aba.getMedianVelMulti(c_omr, (0, 15*60), smoothWinLen = sm)
cEndVel = aba.getMedianVelMulti(c_omr, tRange=[-endWinLen,-0], smoothWinLen=sm)
cEndVel_2a = aba.getMedianVelMulti(c_post_omr, (0,900), smoothWinLen=sm)
cEndVel_2b = aba.getMedianVelMulti(c_post_omr, (900,1800), smoothWinLen=sm)

#velocity comparisons 
[tv, exper_start_end] = scipy.stats.ttest_ind(eBaseVel, eEndVel)
[tv, control_start_end] = scipy.stats.ttest_ind(cBaseVel, cEndVel)
print 'Statistics comparing velocity between start and end velocity (experimental, control fish):', exper_start_end, control_start_end

#fix
#eEndVel25[2]= np.nan

#convert to array
eBV = np.array([np.array([eBaseVel[n]]) for n in range(len(eBaseVel))])
eEV = np.array([np.array([eEndVel[n]]) for n in range(len(eEndVel))])
eEV2a = np.array([np.array([eEndVel_2a[n]]) for n in range(len(eEndVel_2a))])
eEV2b = np.array([np.array([eEndVel_2b[n]]) for n in range(len(eEndVel_2b))])
experimental = np.transpose(np.hstack((eBV, eEV, eEV2a, eEV2b)))

cBV = np.array([np.array([cBaseVel[n]]) for n in range(len(cBaseVel))])
cEV = np.array([np.array([cEndVel[n]]) for n in range(len(cEndVel))])
cEV2a = np.array([np.array([cEndVel_2a[n]]) for n in range(len(cEndVel_2a))])
cEV2b = np.array([np.array([cEndVel_2b[n]]) for n in range(len(cEndVel_2b))])
control = np.transpose(np.hstack((cBV, cEV, cEV2a, cEV2b)))

eBMD = np.array([np.array([eBaseMaxDist[n]]) for n in range(len(eBaseMaxDist))])
eEMD = np.array([np.array([eEndMaxDist[n]]) for n in range(len(eEndMaxDist))])
eBTD = np.array([np.array([eBaseTotalDist[n]]) for n in range(len(eBaseTotalDist))])
eETD = np.array([np.array([eEndTotalDist[n]]) for n in range(len(eEndTotalDist))])
eBF = np.array([np.array([eBaseFrac[n]]) for n in range(len(eBaseFrac))])
eEF = np.array([np.array([eEndFrac[n]]) for n in range(len(eEndFrac))])
experimentalDist = np.transpose(np.hstack((eBMD, eEMD)))
experimentalTotalDist = np.transpose(np.hstack((eBTD, eETD)))
experimentalFrac = np.transpose(np.hstack((eBF, eEF)))

cBMD = np.array([np.array([cBaseMaxDist[n]]) for n in range(len(cBaseMaxDist))])
cEMD = np.array([np.array([cEndMaxDist[n]]) for n in range(len(cEndMaxDist))])
cBTD = np.array([np.array([cBaseTotalDist[n]]) for n in range(len(cBaseTotalDist))])
cETD = np.array([np.array([cEndTotalDist[n]]) for n in range(len(cEndTotalDist))])
cBF = np.array([np.array([cBaseFrac[n]]) for n in range(len(cBaseFrac))])
cEF = np.array([np.array([cEndFrac[n]]) for n in range(len(cEndFrac))])
controlDist = np.transpose(np.hstack((cBMD, cEMD)))
controlTotalDist = np.transpose(np.hstack((cBTD, cETD)))
controlFrac = np.transpose(np.hstack((cBF, cEF)))

cBMDN = np.array([np.array([cBaseMaxDistNon[n]]) for n in range(len(cBaseMaxDistNon))])
cEMDN = np.array([np.array([cEndMaxDistNon[n]]) for n in range(len(cEndMaxDistNon))])
cBTDN = np.array([np.array([cBaseTotalDistNon[n]]) for n in range(len(cBaseTotalDistNon))])
cETDN = np.array([np.array([cEndTotalDistNon[n]]) for n in range(len(cEndTotalDistNon))])
cBFN = np.array([np.array([cBaseFracNon[n]]) for n in range(len(cBaseFracNon))])
cEFN = np.array([np.array([cEndFracNon[n]]) for n in range(len(cEndFracNon))])
controlDistNon = np.transpose(np.hstack((cBMDN, cEMDN)))
controlTotalDistNon = np.transpose(np.hstack((cBTDN, cETDN)))
controlFracNon = np.transpose(np.hstack((cBFN, cEFN)))

pylab.figure()
pylab.suptitle('OMR-based Learned Helplessness Assay at 5V (experimental fish)')
ax = pylab.subplot2grid((2,3), (0,0), colspan=3)
pylab.plot(experimental)
pylab.plot(0, [eBaseVel], 'r.')
pylab.plot(1, [eEndVel], 'r.')
pylab.plot(2, [eEndVel_2a], 'r.')
pylab.plot(3, [eEndVel_2b], 'r.')
pylab.plot([0,1,2,3],[np.mean(eBaseVel), np.mean(eEndVel), np.mean(eEndVel_2a), np.mean(eEndVel_2b)],'o-k',lw=3)
yerr = (2*scipy.stats.sem(eBaseVel), 2*scipy.stats.sem(eEndVel), 2*scipy.stats.sem(eEndVel_2a), 2*scipy.stats.sem(eEndVel_2b))
pyplot.errorbar([0,1,2,3],[np.mean(eBaseVel), np.mean(eEndVel),np.mean(eEndVel_2a), np.mean(eEndVel_2b)],fmt='ok',yerr=yerr, lw=3)
ax.set_xticks((0,1,2,3))
ax.set_xticklabels(('baseline\n (15 min)','last 5 min', 'post 0-15', 'post 15-30'))
pylab.xlim((-.25,3.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Experimental Fish - OMR and Learned Helplessness')
patch1 = mpl.patches.Rectangle((-.25,0), 1.5,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax2=pylab.subplot2grid((2,3), (1,0))
pylab.plot(experimentalDist)
pylab.plot(0, [eBaseMaxDist],'r.')
pylab.plot(1, [eEndMaxDist],'r.')
pylab.plot([0,1],[np.mean(eBaseMaxDist), np.mean(eEndMaxDist)],'o-k',lw=3)
yerrMD = (2*scipy.stats.sem(eBaseMaxDist), 2*scipy.stats.sem(eEndMaxDist))
pyplot.errorbar([0,1],[np.mean(eBaseMaxDist), np.mean(eEndMaxDist)],fmt='ok',yerr=yerrMD, lw=3)
ax2.set_xticks((0,1))
ax2.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Maximum Distance')
ax3=pylab.subplot2grid((2,3),(1,1))
pylab.plot(experimentalTotalDist)
pylab.plot(0, [eBaseTotalDist],'r.')
pylab.plot(1, [eEndTotalDist],'r.')
pylab.plot([0,1],[np.mean(eBaseTotalDist), np.mean(eEndTotalDist)],'o-k',lw=3)
yerrTD = (2*scipy.stats.sem(eBaseTotalDist), 2*scipy.stats.sem(eEndTotalDist))
pyplot.errorbar([0,1],[np.mean(eBaseTotalDist), np.mean(eEndTotalDist)],fmt='ok',yerr=yerrTD, lw=3)
ax3.set_xticks((0,1))
ax3.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Total Distance')
ax4=pylab.subplot2grid((2,3),(1,2))
pylab.plot(experimentalFrac)
pylab.plot(0, [eBaseFrac],'r.')
pylab.plot(1, [eEndFrac],'r.')
pylab.plot([0,1],[np.mean(eBaseFrac), np.mean(eEndFrac)],'o-k',lw=3)
yerrF = (2*scipy.stats.sem(eBaseFrac), 2*scipy.stats.sem(eEndFrac))
pyplot.errorbar([0,1],[np.mean(eBaseFrac), np.mean(eEndFrac)],fmt='ok',yerr=yerrF, lw=3)
ax4.set_xticks((0,1))
ax4.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Fraction of time')

pylab.figure()
pylab.suptitle('OMR-based Learned Helplessness Assay at 5V (control fish)')
ax = pylab.subplot2grid((2,3), (0,0), colspan=3)
pylab.plot(control)
pylab.plot(0, [cBaseVel], 'r.')
pylab.plot(1, [cEndVel], 'r.')
pylab.plot(2, [cEndVel_2a], 'r.')
pylab.plot(3, [cEndVel_2b], 'r.')
pylab.plot([0,1,2,3],[np.mean(cBaseVel), np.mean(cEndVel), np.mean(cEndVel_2a), np.mean(cEndVel_2b)],'o-k',lw=3)
yerrC = (2*scipy.stats.sem(cBaseVel), 2*scipy.stats.sem(cEndVel), 2*scipy.stats.sem(cEndVel_2a), 2*scipy.stats.sem(cEndVel_2b))
pyplot.errorbar([0,1,2,3],[np.mean(cBaseVel), np.mean(cEndVel),np.mean(cEndVel_2a), np.mean(cEndVel_2b)],fmt='ok',yerr=yerr, lw=3)
ax.set_xticks((0,1,2,3))
ax.set_xticklabels(('baseline\n (15 min)','last 5 min', 'post 0-15', 'post 15-30'))
pylab.xlim((-.25,3.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Control Fish - OMR and Learned Helplessness')
patch1 = mpl.patches.Rectangle((-.25,0), 1.5,10, color = 'g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch1)
ax2=pylab.subplot2grid((2,3), (1,0))
pylab.plot(controlDist)
pylab.plot(0, [cBaseMaxDist],'r.')
pylab.plot(1, [cEndMaxDist],'r.')
pylab.plot([0,1],[np.mean(cBaseMaxDist), np.mean(cEndMaxDist)],'o-k',lw=3)
yerrMDC = (2*scipy.stats.sem(cBaseMaxDist), 2*scipy.stats.sem(cEndMaxDist))
pyplot.errorbar([0,1],[np.mean(cBaseMaxDist), np.mean(cEndMaxDist)],fmt='ok',yerr=yerrMD, lw=3)
ax2.set_xticks((0,1))
ax2.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Maximum Distance')
ax3=pylab.subplot2grid((2,3),(1,1))
pylab.plot(controlTotalDist)
pylab.plot(0, [cBaseTotalDist],'r.')
pylab.plot(1, [cEndTotalDist],'r.')
pylab.plot([0,1],[np.mean(cBaseTotalDist), np.mean(cEndTotalDist)],'o-k',lw=3)
yerrTDC = (2*scipy.stats.sem(cBaseTotalDist), 2*scipy.stats.sem(cEndTotalDist))
pyplot.errorbar([0,1],[np.mean(cBaseTotalDist), np.mean(cEndTotalDist)],fmt='ok',yerr=yerrTD, lw=3)
ax3.set_xticks((0,1))
ax3.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Total Distance')
ax4=pylab.subplot2grid((2,3),(1,2))
pylab.plot(controlFrac)
pylab.plot(0, [cBaseFrac],'r.')
pylab.plot(1, [cEndFrac],'r.')
pylab.plot([0,1],[np.mean(cBaseFrac), np.mean(cEndFrac)],'o-k',lw=3)
yerrFC = (2*scipy.stats.sem(cBaseFrac), 2*scipy.stats.sem(cEndFrac))
pyplot.errorbar([0,1],[np.mean(cBaseFrac), np.mean(cEndFrac)],fmt='ok',yerr=yerrF, lw=3)
ax4.set_xticks((0,1))
ax4.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Fraction of time')


pylab.figure()
pylab.suptitle('OMR-LH Summary')
ax = pylab.subplot2grid((2,3), (0,0), colspan=3)
experimentalfish = ax.plot([0,1,2,3],[np.mean(eBaseVel), np.mean(eEndVel),np.mean(eEndVel_2a), np.mean(eEndVel_2b)],'o-b', lw=3, label='Experimental Fish (5V)')
pyplot.errorbar([0,1,2,3],[np.mean(eBaseVel), np.mean(eEndVel),np.mean(eEndVel_2a), np.mean(eEndVel_2b)],fmt='ob', yerr=yerr, lw=3)
controlfish = ax.plot([0,1,2,3],[np.mean(cBaseVel), np.mean(cEndVel),np.mean(cEndVel_2a), np.mean(cEndVel_2b)],'o-k', lw=3, label='Control Fish (5V)')
pyplot.errorbar([0,1,2,3],[np.mean(cBaseVel), np.mean(cEndVel),np.mean(cEndVel_2a), np.mean(cEndVel_2b)],fmt='ok', yerr=yerrC, lw=3)
handles, labels=ax.get_legend_handles_labels()
ax.legend(handles, labels)
ax.set_xticks((0,1,2,3))
ax.set_xticklabels(('baseline\n (15min)', 'last 5 min\n of shock','post 0-15', 'post 15-30'))
pylab.xlim((-.25,3.5))
pylab.ylim((0,5.5))
pylab.ylabel('Median Velocity (mm/s)')
patch3 = mpl.patches.Rectangle((-.25,0),1.5 , 10, color='g', fill=True, alpha=0.5)
pyplot.gca().add_patch(patch3)
ax2=pylab.subplot2grid((2,3), (1,0))
maxdistance = ax2.plot([0,1],[np.mean(eBaseMaxDist), np.mean(eEndMaxDist)],'o-b',lw=3)
pyplot.errorbar([0,1],[np.mean(eBaseMaxDist), np.mean(eEndMaxDist)],fmt='ob',yerr=yerrMD, lw=3)
maxdistancecontrol = ax2.plot([0,1],[np.mean(cBaseMaxDist), np.mean(cEndMaxDist)],'o-k',lw=3)
pyplot.errorbar([0,1],[np.mean(cBaseMaxDist), np.mean(cEndMaxDist)],fmt='ok',yerr=yerrMDC, lw=3)
ax2.set_xticks((0,1))
ax2.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Maximum Distance')
ax3=pylab.subplot2grid((2,3), (1,1))
totaldistance = ax3.plot([0,1],[np.mean(eBaseTotalDist), np.mean(eEndTotalDist)],'o-b',lw=3)
pyplot.errorbar([0,1],[np.mean(eBaseTotalDist), np.mean(eEndTotalDist)],fmt='ob',yerr=yerrTD, lw=3)
totaldistancecontrol = ax3.plot([0,1],[np.mean(cBaseTotalDist), np.mean(cEndTotalDist)],'o-k',lw=3)
pyplot.errorbar([0,1],[np.mean(cBaseTotalDist), np.mean(cEndTotalDist)],fmt='ok',yerr=yerrTDC, lw=3)
ax3.set_xticks((0,1))
ax3.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Total Distance')
ax4=pylab.subplot2grid((2,3), (1,2))
fraction = ax4.plot([0,1],[np.mean(eBaseFrac), np.mean(eEndFrac)],'o-b',lw=3)
pyplot.errorbar([0,1],[np.mean(eBaseFrac), np.mean(eEndFrac)],fmt='ob',yerr=yerrF, lw=3)
fractioncontrol = ax4.plot([0,1],[np.mean(cBaseFrac), np.mean(cEndFrac)],'o-k',lw=3)
pyplot.errorbar([0,1],[np.mean(cBaseFrac), np.mean(cEndFrac)],fmt='ok',yerr=yerrFC, lw=3)
ax4.set_xticks((0,1))
ax4.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Fraction of time')

pylab.figure()
pylab.suptitle('Is OMR working?')
ax2=pylab.subplot(231)
maxdistancecontrol = ax2.plot([0,1],[np.mean(cBaseMaxDist), np.mean(cEndMaxDist)],'o-k',lw=3, label="OMR on")
pyplot.errorbar([0,1],[np.mean(cBaseMaxDist), np.mean(cEndMaxDist)],fmt='ok',yerr=yerrMDC, lw=3)
maxdistancecontrolnon = ax2.plot([0,1],[np.mean(cBaseMaxDistNon), np.mean(cEndMaxDistNon)],'o-m',lw=3, label="OMR off")
yerrMDCN = (2*scipy.stats.sem(cBaseMaxDistNon), 2*scipy.stats.sem(cEndMaxDistNon))
pyplot.errorbar([0,1],[np.mean(cBaseMaxDistNon), np.mean(cEndMaxDistNon)],fmt='om',yerr=yerrMDCN, lw=3)
handles, labels=ax2.get_legend_handles_labels()
ax2.legend(handles, labels)
ax2.set_xticks((0,1))
ax2.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Control Maximum Distance')
ax3=pylab.subplot(232)
totaldistancecontrol = ax3.plot([0,1],[np.mean(cBaseTotalDist), np.mean(cEndTotalDist)],'o-k',lw=3, label = "OMR on")
pyplot.errorbar([0,1],[np.mean(cBaseTotalDist), np.mean(cEndTotalDist)],fmt='ok',yerr=yerrTDC, lw=3)
totaldistancecontrolnon = ax3.plot([0,1],[np.mean(cBaseTotalDistNon), np.mean(cEndTotalDistNon)],'o-m',lw=3, label = "OMR off")
yerrTDCN = (2*scipy.stats.sem(cBaseTotalDistNon), 2*scipy.stats.sem(cEndTotalDistNon))
pyplot.errorbar([0,1],[np.mean(cBaseTotalDistNon), np.mean(cEndTotalDistNon)],fmt='om',yerr=yerrTDCN, lw=3)
handles, labels=ax3.get_legend_handles_labels()
ax3.legend(handles, labels)
ax3.set_xticks((0,1))
ax3.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Control Total Distance')
ax4=pylab.subplot(233)
fractioncontrol = ax4.plot([0,1],[np.mean(cBaseFrac), np.mean(cEndFrac)],'o-k',lw=3,label = "OMR on")
pyplot.errorbar([0,1],[np.mean(cBaseFrac), np.mean(cEndFrac)],fmt='ok',yerr=yerrFC, lw=3)
fractioncontrolnon = ax4.plot([0,1],[np.mean(cBaseFracNon), np.mean(cEndFracNon)],'o-m',lw=3,label = "OMR off")
yerrFCN = (2*scipy.stats.sem(cBaseFracNon), 2*scipy.stats.sem(cEndFracNon))
pyplot.errorbar([0,1],[np.mean(cBaseFracNon), np.mean(cEndFracNon)],fmt='om',yerr=yerrFCN, lw=3)
handles, labels=ax4.get_legend_handles_labels()
ax4.legend(handles, labels)
ax4.set_xticks((0,1))
ax4.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Control Fraction of time')
ax5=pylab.subplot(234)
maxdistance = ax5.plot([0,1],[np.mean(eBaseMaxDist), np.mean(eEndMaxDist)],'o-k',lw=3, label="OMR on")
pyplot.errorbar([0,1],[np.mean(eBaseMaxDist), np.mean(eEndMaxDist)],fmt='ok',yerr=yerrMD, lw=3)
maxdistancenon = ax5.plot([0,1],[np.mean(eBaseMaxDistNon), np.mean(eEndMaxDistNon)],'o-m',lw=3, label="OMR off")
yerrMDN = (2*scipy.stats.sem(eBaseMaxDistNon), 2*scipy.stats.sem(eEndMaxDistNon))
pyplot.errorbar([0,1],[np.mean(eBaseMaxDistNon), np.mean(eEndMaxDistNon)],fmt='om',yerr=yerrMDN, lw=3)
handles, labels=ax2.get_legend_handles_labels()
ax5.legend(handles, labels)
ax5.set_xticks((0,1))
ax5.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Experimental Maximum Distance')
ax6=pylab.subplot(235)
totaldistance = ax6.plot([0,1],[np.mean(eBaseTotalDist), np.mean(eEndTotalDist)],'o-k',lw=3, label = "OMR on")
pyplot.errorbar([0,1],[np.mean(eBaseTotalDist), np.mean(eEndTotalDist)],fmt='ok',yerr=yerrTD, lw=3)
totaldistancenon = ax6.plot([0,1],[np.mean(eBaseTotalDistNon), np.mean(eEndTotalDistNon)],'o-m',lw=3, label = "OMR off")
yerrTDN = (2*scipy.stats.sem(eBaseTotalDistNon), 2*scipy.stats.sem(eEndTotalDistNon))
pyplot.errorbar([0,1],[np.mean(eBaseTotalDistNon), np.mean(eEndTotalDistNon)],fmt='om',yerr=yerrTDN, lw=3)
handles, labels=ax6.get_legend_handles_labels()
ax6.legend(handles, labels)
ax6.set_xticks((0,1))
ax6.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Experimental Total Distance')
ax7=pylab.subplot(236)
fraction = ax7.plot([0,1],[np.mean(eBaseFrac), np.mean(eEndFrac)],'o-k',lw=3,label = "OMR on")
pyplot.errorbar([0,1],[np.mean(eBaseFrac), np.mean(eEndFrac)],fmt='ok',yerr=yerrF, lw=3)
fractionnon = ax7.plot([0,1],[np.mean(eBaseFracNon), np.mean(eEndFracNon)],'o-m',lw=3,label = "OMR off")
yerrFN = (2*scipy.stats.sem(eBaseFracNon), 2*scipy.stats.sem(eEndFracNon))
pyplot.errorbar([0,1],[np.mean(eBaseFracNon), np.mean(eEndFracNon)],fmt='om',yerr=yerrFN, lw=3)
handles, labels=ax7.get_legend_handles_labels()
ax7.legend(handles, labels)
ax7.set_xticks((0,1))
ax7.set_xticklabels(('baseline 15 min', 'last 5 min'))
pylab.xlim((-.25,1.5))
pylab.title('Experimental Fraction of time')

pylab.show()

