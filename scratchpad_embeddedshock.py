import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np

e_fish_youngNR = ['/home/vburns/Dropbox/ConchisData/2013-02-12/f00134/f00134_2013-02-12-17-57-45.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-12/f00135/f00135_2013-02-12-17-57-30.json']
e_fish_youngNR = aba.loadMultipleDataFiles(e_fish_youngNR)

e_fish_youngR = '/home/vburns/Dropbox/ConchisData/2013-02-12/f00136/f00136_2013-02-12-17-57-33.json'
e_fish_youngR = aba.loadDataFromFile(e_fish_youngR)
e_fish_youngR = [e_fish_youngR]

e_fish_oldNR = ['/home/vburns/Dropbox/ConchisData/2013-02-12/f00138/f00138_2013-02-12-17-57-37.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-12/f00139/f00139_2013-02-12-17-57-40.json']
e_fish_oldNR = aba.loadMultipleDataFiles(e_fish_oldNR)

e_fish_oldR = ['/home/vburns/Dropbox/ConchisData/2013-02-12/f00140/f00140_2013-02-12-17-57-48.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-12/f00141/f00141_2013-02-12-17-57-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-02-12/f00142/f00142_2013-02-12-17-57-53.json']
e_fish_oldR = aba.loadMultipleDataFiles(e_fish_oldR)

#assumes shock is on red
(e_frac_yNR, e_dist_yNR) = aba.getSidePreference_Multi(e_fish_youngNR, cond = [8,8], refState ='Red')
(e_frac_yR, e_dist_yR) = aba.getSidePreference_Multi(e_fish_youngR, cond = [8,8], refState ='Red')
(e_frac_oNR, e_dist_oNR) = aba.getSidePreference_Multi(e_fish_oldNR, cond = [8,8], refState ='Red')
(e_frac_oR, e_dist_oR) = aba.getSidePreference_Multi(e_fish_oldR, cond = [8,8], refState ='Red')

e_young_frac = np.append(e_frac_yNR, e_frac_yR, axis = 0)
e_old_frac = np.append(e_frac_oNR, e_frac_oR, axis = 0)
e_young_dist = np.append(e_dist_yNR, e_dist_yR, axis = 0)
e_old_dist = np.append(e_dist_oNR, e_dist_oR, axis = 0)

import scipy
[tv, e_yfrac] = scipy.stats.ttest_1samp(np.mean(e_young_frac, axis = 1), 0.5)
[tv, e_ofrac] = scipy.stats.ttest_1samp(np.mean(e_old_frac, axis = 1), 0.5)
[tv, e_ydist] = scipy.stats.ttest_1samp(np.mean(e_young_dist, axis = 1), 24)
[tv, e_odist] = scipy.stats.ttest_1samp(np.mean(e_old_dist, axis = 1), 24)

print 'experimental young frac, old frac, young dist, old dist: ', e_yfrac, e_ofrac, e_ydist, e_odist

import pylab
total = e_fish_youngNR + e_fish_youngR + e_fish_oldNR + e_fish_oldR
for n in range(len(total)):
     pylab.figure(1);
     ax = pylab.subplot(2,4,n)
     aba.plotFishXPosition(total[n])
pylab.show()

