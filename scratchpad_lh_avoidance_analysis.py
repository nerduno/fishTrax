import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np

e_test_f = [u'/Users/andalman/Dropbox/ConchisData/2013-01-11/f00076/f00076_2013-01-11-13-41-31.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-11/f00077/f00077_2013-01-11-13-41-34.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-11/f00078/f00078_2013-01-11-13-41-37.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-11/f00079/f00079_2013-01-11-13-41-39.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-10/f00076/f00076_2013-01-10-18-40-41.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-10/f00077/f00077_2013-01-10-18-40-38.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-10/f00078/f00078_2013-01-10-18-40-36.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-10/f00079/f00079_2013-01-10-18-40-34.json']
e_test = aba.loadMultipleDataFiles(e_test_f)

e_lh_f = [u'/Users/andalman/Dropbox/ConchisData/2013-01-11/f00076/f00076_2013-01-11-12-29-51.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-11/f00077/f00077_2013-01-11-12-29-49.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-11/f00078/f00078_2013-01-11-12-29-46.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-11/f00079/f00079_2013-01-11-12-29-44.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-10/f00076/f00076_2013-01-10-18-03-08.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-10/f00077/f00077_2013-01-10-18-03-11.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-10/f00078/f00078_2013-01-10-18-03-13.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-10/f00079/f00079_2013-01-10-18-03-16.json']
e_lh = aba.loadMultipleDataFiles(e_lh_f)

c_test_f = [u'/Users/andalman/Dropbox/ConchisData/2013-01-10/f00072/f00072_2013-01-10-17-16-45.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-10/f00073/f00073_2013-01-10-17-16-42.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-10/f00074/f00074_2013-01-10-17-16-39.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-10/f00075/f00075_2013-01-10-17-16-36.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-09/f00046/f00046_2013-01-09-18-24-16.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-09/f00047/f00047_2013-01-09-18-24-20.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-09/f00048/f00048_2013-01-09-18-24-24.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-09/f00049/f00049_2013-01-09-18-24-26.json']
c_test = aba.loadMultipleDataFiles(c_test_f)

c_lh_f = [u'/Users/andalman/Dropbox/ConchisData/2013-01-10/f00072/f00072_2013-01-10-16-39-43.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-10/f00073/f00073_2013-01-10-16-39-40.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-10/f00074/f00074_2013-01-10-16-39-38.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-10/f00075/f00075_2013-01-10-16-39-36.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-09/f00046/f00046_2013-01-09-16-25-41.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-09/f00047/f00047_2013-01-09-16-25-43.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-09/f00048/f00048_2013-01-09-16-25-45.json',
 u'/Users/andalman/Dropbox/ConchisData/2013-01-09/f00049/f00049_2013-01-09-16-25-48.json']
c_lh = aba.loadMultipleDataFiles(c_lh_f)

#Real time avoidance statistics following extended shock (learned helplessness)
(e_fracTimeOnShock,e_distFromShock) = aba.getSidePreference_Multi(e_test)
(c_fracTimeOnShock,c_distFromShock) = aba.getSidePreference_Multi(c_test)

#n is an animal
import scipy
[t,p_e_time] = scipy.stats.ttest_1samp(np.mean(e_fracTimeOnShock,1),.5)
[t,p_c_time] = scipy.stats.ttest_1samp(np.mean(c_fracTimeOnShock,1),.5)
[t,p_e_dist] = scipy.stats.ttest_1samp(np.mean(e_distFromShock,1),24)
[t,p_c_dist] = scipy.stats.ttest_1samp(np.mean(c_distFromShock,1),24)
[t,p_time_diff] = scipy.stats.ttest_ind(np.mean(e_fracTimeOnShock,1), np.mean(c_fracTimeOnShock,1))
[t,p_dist_diff] = scipy.stats.ttest_ind(np.mean(e_distFromShock,1), np.mean(c_distFromShock,1))
print 'BY ANIMAL Avoidance Post LH_5V      p_frac,p_dist: ', p_e_time, p_e_dist
print 'BY ANIMAL Avoidance Post LH_CONTROL p_frac,p_dist: ', p_c_time, p_c_dist
print 'BY ANIMAL Controls diff from Exper (time,dist): ', p_time_diff, p_dist_diff 
ae_f = np.mean(e_fracTimeOnShock,1)
ac_f = np.mean(c_fracTimeOnShock,1)
ae_d = np.mean(e_distFromShock,1)
ac_d = np.mean(c_distFromShock,1)
pylab.figure(1)
ax = pylab.subplot(1,2,1)
pylab.errorbar([0,1],[np.mean(ae_f),np.mean(ac_f)],fmt='o',yerr=(2*scipy.stats.sem(ae_f),2*scipy.stats.sem(ac_f)))
pylab.axhline(.5)
pylab.xlim((-1,2))
pylab.ylim((0,1))
pylab.ylabel('% Time on shock side')
ax.set_xticks((0,1))
ax.set_xticklabels(('exper','control'))
pylab.title('Real-time shock avoidance following \nlearned helplessness induction\np=%2.2f, %2.2f.'%(p_e_time,p_c_time))
ax = pylab.subplot(1,2,2)
pylab.errorbar([0,1],[48-np.mean(ae_d),48-np.mean(ac_d)],fmt='o',yerr=(2*scipy.stats.sem(ae_d),2*scipy.stats.sem(ac_d)))
pylab.axhline(24)
pylab.xlim((-1,2))
pylab.ylim((0,48))
pylab.ylabel('% Avg dist from safe side')
ax.set_xticks((0,1))
ax.set_xticklabels(('exper','control'))
ax.set_yticks((0,24,48))
pylab.title('Real-time shock avoidance following \nlearned helplessness induction\np=%2.2f, %2.2f.'%(p_e_dist,p_c_dist))

#n is an shockblock (120s)
import scipy
[t,p_e_time] = scipy.stats.ttest_1samp(e_fracTimeOnShock.flatten(),.5)
[t,p_c_time] = scipy.stats.ttest_1samp(c_fracTimeOnShock.flatten(),.5)
[t,p_e_dist] = scipy.stats.ttest_1samp(e_distFromShock.flatten(),24)
[t,p_c_dist] = scipy.stats.ttest_1samp(c_distFromShock.flatten(),24)
[t,p_time_diff] = scipy.stats.ttest_ind(e_fracTimeOnShock.flatten(), c_fracTimeOnShock.flatten())
[t,p_dist_diff] = scipy.stats.ttest_ind(e_distFromShock.flatten(), c_distFromShock.flatten())
print 'BY SHOCKBLOCK Avoidance Post LH_5V      p_frac,p_dist: ', p_e_time, p_e_dist
print 'BY SHOCKBLOCK Avoidance Post LH_CONTROL p_frac,p_dist: ', p_c_time, p_c_dist
print 'BY SHOCKBLOCK Controls diff from Exper (time,dist): ', p_time_diff, p_dist_diff 
pylab.figure(2)
pylab.subplot(1,2,1)
pylab.boxplot([e_fracTimeOnShock,c_fracTimeOnShock])
pylab.subplot(1,2,2)
pylab.boxplot([e_distFromShock,c_distFromShock])
pylab.show()

def getVelMulti(datasets, tRange=None):
    medVel = []
    for d in datasets:
        w = d['warpedTracking']
        if tRange:
            bNdxWin = np.logical_and(w[:,0]>tRange[0]+w[0,0], w[:,0]<tRange[1]+w[0,0])
            vel = np.sqrt(pow(np.diff(w[bNdxWin,1]),2) + pow(np.diff(w[bNdxWin,2]),2)) / np.diff(w[bNdxWin,0])
        else:
            vel = np.sqrt(pow(np.diff(w[:,1]),2) + pow(np.diff(w[:,2]),2)) / np.diff(w[:,0])
        medVel.append(np.median(vel))     
    return medVel

#velocity locomation analysis
eTestVel = getVelMulti(e_test)
eLHVel = getVelMulti(e_lh, (300,900))
cTestVel = getVelMulti(c_test)
cLHVel = getVelMulti(c_lh, (300,900))
pylab.figure(3)
ax = pylab.subplot(1,2,1)
pylab.plot([0,1],[eLHVel,eTestVel],'.-r')
ax.set_xticks((0,1))
ax.set_xticklabels(('pre','post'))
pylab.xlim((-.25,1.25))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Effect of LH protocol on velocity\nExperimental Fish')
ax = pylab.subplot(1,2,2,sharey=ax)
pylab.plot([0,1],[cLHVel,cTestVel],'.-k')
ax.set_xticks((0,1))
ax.set_xticklabels(('pre','post'))
pylab.xlim((-.25,1.25))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Effect of LH protocol on velocity\nControl Fish')
pylab.show()



