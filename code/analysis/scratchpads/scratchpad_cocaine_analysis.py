import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np

e_pre_f_multi = '/home/vburns/Dropbox/ConchisData/2012-12-21/f00022/f00022_2012-12-21-10-07-32.json'
e_pre_f = ['/home/vburns/Dropbox/ConchisData/2012-12-21/f00024/f00024_2012-12-21-10-07-38.json',
 '/home/vburns/Dropbox/ConchisData/2012-12-21/f00027/f00027_2012-12-21-10-07-46.json',
 '/home/vburns/Dropbox/ConchisData/2012-12-21/f00029/f00029_2012-12-21-10-07-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-03/f00042/f00042_2013-01-03-11-26-35.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-03/f00043/f00043_2013-01-03-11-26-32.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-03/f00044/f00044_2013-01-03-11-26-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-03/f00045/f00045_2013-01-03-11-26-27.json']
e_pre = aba.loadMultipleDataFiles(e_pre_f)
e_temp = aba.loadDataFromFile_AvgMultiFish(e_pre_f_multi) 
e_pre = [e_temp] + e_pre

e_postM_f = '/home/vburns/Dropbox/ConchisData/2012-12-21/f00022/f00022_2012-12-21-13-23-49.json'
e_post_f = ['/home/vburns/Dropbox/ConchisData/2012-12-21/f00024/f00024_2012-12-21-13-24-03.json',
 '/home/vburns/Dropbox/ConchisData/2012-12-21/f00027/f00027_2012-12-21-13-25-17.json',
 '/home/vburns/Dropbox/ConchisData/2012-12-21/f00029/f00029_2012-12-21-13-25-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-03/f00042/f00042_2013-01-03-13-52-59.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-03/f00043/f00043_2013-01-03-13-53-02.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-03/f00044/f00044_2013-01-03-13-53-04.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-03/f00045/f00045_2013-01-03-13-53-06.json']
e_temp2 = aba.loadDataFromFile_AvgMultiFish(e_postM_f)
e_post = aba.loadMultipleDataFiles(e_post_f)
e_post = [e_temp2] + e_post

c_pre_f = ['/home/vburns/Dropbox/ConchisData/2013-01-14/f00080/f00080_2013-01-14-12-17-49.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-14/f00081/f00081_2013-01-14-12-17-52.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-14/f00082/f00082_2013-01-14-12-17-55.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-14/f00083/f00083_2013-01-14-12-17-58.json']
c_pre = aba.loadMultipleDataFiles(c_pre_f)

c_post_f = ['/home/vburns/Dropbox/ConchisData/2013-01-14/f00080/f00080_2013-01-14-14-27-16.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-14/f00081/f00081_2013-01-14-14-27-21.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-14/f00082/f00082_2013-01-14-14-27-30.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-14/f00083/f00083_2013-01-14-14-27-41.json']
c_post = aba.loadMultipleDataFiles(c_post_f)

e_low_pre = ['/home/vburns/Dropbox/ConchisData/2012-12-31/f00037/f00037_2012-12-31-12-03-03.json',
 '/home/vburns/Dropbox/ConchisData/2012-12-31/f00038/f00038_2012-12-31-12-03-01.json',
 '/home/vburns/Dropbox/ConchisData/2012-12-31/f00039/f00039_2012-12-31-12-02-58.json',
 '/home/vburns/Dropbox/ConchisData/2012-12-31/f00040/f00040_2012-12-31-12-02-54.json']
e_low_pre = aba.loadMultipleDataFiles(e_low_pre)

e_low_post = ['/home/vburns/Dropbox/ConchisData/2012-12-31/f00037/f00037_2012-12-31-14-24-44.json',
 '/home/vburns/Dropbox/ConchisData/2012-12-31/f00038/f00038_2012-12-31-14-24-32.json',
 '/home/vburns/Dropbox/ConchisData/2012-12-31/f00039/f00039_2012-12-31-14-24-16.json',
 '/home/vburns/Dropbox/ConchisData/2012-12-31/f00040/f00040_2012-12-31-14-24-01.json']
e_low_post = aba.loadMultipleDataFiles(e_low_post)

e_pre_one = ['/home/vburns/Dropbox/ConchisData/2013-01-23/f00092/f00092_2013-01-23-11-54-03.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-23/f00093/f00093_2013-01-23-11-54-00.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-23/f00094/f00094_2013-01-23-11-53-57.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-23/f00095/f00095_2013-01-23-11-53-52.json']
e_pre_one = aba.loadMultipleDataFiles(e_pre_one)

e_post_one = ['/home/vburns/Dropbox/ConchisData/2013-01-23/f00092/f00092_2013-01-23-14-07-47.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-23/f00093/f00093_2013-01-23-14-07-41.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-23/f00094/f00094_2013-01-23-14-07-34.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-23/f00095/f00095_2013-01-23-14-07-18.json']
e_post_one = aba.loadMultipleDataFiles(e_post_one)

e_three_temp1 = '/home/vburns/Dropbox/ConchisData/2013-01-24/f00096/f00096_2013-01-24-13-56-46.json'
e_pre_three = ['/home/vburns/Dropbox/ConchisData/2013-01-24/f00098/f00098_2013-01-24-13-56-50.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-24/f00099/f00099_2013-01-24-13-56-53.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-24/f00100/f00100_2013-01-24-13-56-56.json']
e_pre_three = aba.loadMultipleDataFiles(e_pre_three)
e_three_temp1 = aba.loadDataFromFile_AvgMultiFish(e_three_temp1)
e_pre_three = [e_three_temp1] + e_pre_three

e_three_temp = '/home/vburns/Dropbox/ConchisData/2013-01-24/f00096/f00096_2013-01-24-16-10-11.json'
e_post_three = ['/home/vburns/Dropbox/ConchisData/2013-01-24/f00098/f00098_2013-01-24-16-10-14.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-24/f00099/f00099_2013-01-24-16-10-17.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-24/f00100/f00100_2013-01-24-16-10-22.json']
e_post_three = aba.loadMultipleDataFiles(e_post_three)
e_three_temp = aba.loadDataFromFile_AvgMultiFish(e_three_temp)
e_post_three = [e_three_temp] + e_post_three 

e_pre_pfour = ['/home/vburns/Dropbox/ConchisData/2013-01-28/f00105/f00105_2013-01-28-11-32-09.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-28/f00106/f00106_2013-01-28-11-32-07.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-28/f00107/f00107_2013-01-28-11-32-05.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-28/f00108/f00108_2013-01-28-11-32-02.json']
e_pre_pfour = aba.loadMultipleDataFiles(e_pre_pfour)

e_post_pfour = ['/home/vburns/Dropbox/ConchisData/2013-01-28/f00105/f00105_2013-01-28-13-44-18.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-28/f00106/f00106_2013-01-28-13-44-20.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-28/f00107/f00107_2013-01-28-13-44-23.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-28/f00108/f00108_2013-01-28-13-44-26.json']
e_post_pfour = aba.loadMultipleDataFiles(e_post_pfour)

e_pre_ten =['/home/vburns/Dropbox/ConchisData/2013-01-29/f00109/f00109_2013-01-29-10-59-53.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-29/f00110/f00110_2013-01-29-10-59-51.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-29/f00111/f00111_2013-01-29-10-59-48.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-29/f00112/f00112_2013-01-29-10-59-46.json'] 
e_pre_ten = aba.loadMultipleDataFiles(e_pre_ten)

e_post_ten = ['/home/vburns/Dropbox/ConchisData/2013-01-29/f00109/f00109_2013-01-29-13-35-23.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-29/f00110/f00110_2013-01-29-13-35-21.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-29/f00111/f00111_2013-01-29-13-35-19.json',
 '/home/vburns/Dropbox/ConchisData/2013-01-29/f00112/f00112_2013-01-29-13-35-17.json']
e_post_ten = aba.loadMultipleDataFiles(e_post_ten)

print asdf
#assumes cocaine is on red
(e_pre_frac,e_pre_dist) = aba.getSidePreference_Multi(e_pre, cond = [3,8], refState ='Red')
(c_pre_frac,c_pre_dist) = aba.getSidePreference_Multi(c_pre, cond = [3,8], refState = 'Red')

(e_post_frac,e_post_dist) = aba.getSidePreference_Multi(e_post, cond = [3,8], refState ='Red')
(c_post_frac,c_post_dist) = aba.getSidePreference_Multi(c_post, cond = [3,8], refState = 'Red')

(e_prel_frac,e_prel_dist) = aba.getSidePreference_Multi(e_low_pre, cond = [3,8], refState ='Red')
(e_postl_frac,e_postl_dist) = aba.getSidePreference_Multi(e_low_post, cond = [3,8], refState = 'Red')

(e_pre1_frac,e_pre1_dist) = aba.getSidePreference_Multi(e_pre_one, cond = [3,8], refState ='Red')
(e_post1_frac,e_post1_dist) = aba.getSidePreference_Multi(e_post_one, cond = [3,8], refState = 'Red')

(e_pre3_frac,e_pre3_dist) = aba.getSidePreference_Multi(e_pre_three, cond = [3,8], refState ='Red')
(e_post3_frac,e_post3_dist) = aba.getSidePreference_Multi(e_post_three, cond = [3,8], refState = 'Red')

(e_prep4_frac,e_prep4_dist) = aba.getSidePreference_Multi(e_pre_pfour, cond = [3,8], refState ='Red')
(e_postp4_frac,e_postp4_dist) = aba.getSidePreference_Multi(e_post_pfour, cond = [3,8], refState = 'Red')

(e_preten_frac,e_preten_dist) = aba.getSidePreference_Multi(e_pre_ten, cond = [3,8], refState ='Red')
(e_postten_frac,e_postten_dist) = aba.getSidePreference_Multi(e_post_ten, cond = [3,8], refState = 'Red')


import scipy
[tv, p_e_pre] = scipy.stats.ttest_1samp(np.mean(e_pre_frac, axis = 1),.5)
[tv, p_e_post] = scipy.stats.ttest_1samp(np.mean(e_post_frac, axis = 1),.5)
[tv, e_pre_post] = scipy.stats.ttest_1samp(np.mean(e_post_frac, axis = 1)-np.mean(e_pre_frac, axis = 1),0)

[tv, p_c_pre] = scipy.stats.ttest_1samp(np.mean(c_pre_frac, axis = 1),.5)
[tv, p_c_post] = scipy.stats.ttest_1samp(np.mean(c_post_frac, axis = 1),.5)
[tv, c_pre_post] = scipy.stats.ttest_1samp(np.mean(c_post_frac, axis = 1)-np.mean(c_pre_frac, axis = 1),0)

[tv, p_e3_pre] = scipy.stats.ttest_1samp(np.mean(e_pre3_frac, axis = 1),.5)
[tv, p_e3_post] = scipy.stats.ttest_1samp(np.mean(e_post3_frac, axis = 1),.5)
[tv, e3_pre_post] = scipy.stats.ttest_1samp(np.mean(e_post3_frac, axis = 1)-np.mean(e_pre3_frac, axis = 1),0)

[tv, e_low_prefrac] = scipy.stats.ttest_1samp(np.mean(e_prel_frac, axis = 1),.5)
[tv, e_low_postfrac] = scipy.stats.ttest_1samp(np.mean(e_postl_frac, axis = 1),.5)
[tv, e_low_prepost] = scipy.stats.ttest_1samp(np.mean(e_postl_frac, axis = 1)-np.mean(e_prel_frac, axis = 1),0)

[tv, e_ten_prefrac] = scipy.stats.ttest_1samp(np.mean(e_preten_frac, axis = 1),.5)
[tv, e_ten_postfrac] = scipy.stats.ttest_1samp(np.mean(e_postten_frac, axis = 1),.5)
[tv, e_ten_prepost] = scipy.stats.ttest_1samp(np.mean(e_postten_frac, axis = 1)-np.mean(e_preten_frac, axis = 1),0)

print 'experimental pre,post,prevspost: ', p_e_pre, p_e_post, e_pre_post
print 'control pre,post,prevspost: ', p_c_pre, p_c_post, c_pre_post
print 'experimental (low dose) pre, post, pre vs post:', e_low_prefrac, e_low_postfrac, e_low_prepost
print 'experimental 3um:', p_e3_pre, p_e3_post, e3_pre_post
print 'experimental 10um pre, post, pre vs post:', e_ten_prefrac, e_ten_postfrac, e_ten_prepost

import pylab
pylab.figure(1)
pylab.clf()
pylab.suptitle('Effect of Cocaine CCP (5uM) Experimental Fish', ha = 'center')
ax = pylab.subplot(1,2,1)
pylab.plot([0,1],[np.mean(e_pre_frac, 1),np.mean(e_post_frac,1)],'.-r')
ax.set_xticks((0,1))
ax.set_xticklabels(('pre','post'))
pylab.xlim((-.25,1.25))
pylab.ylim((0,1))
pylab.ylabel('Percent Time on Cocaine Color (Experimental)')
pylab.hold(True)
pylab.errorbar([0,1],[np.mean(e_pre_frac),np.mean(e_post_frac)], yerr=2*scipy.stats.sem([np.mean(e_pre_frac,1),np.mean(e_post_frac,1)], axis = 1), capsize = 5, fmt = '.-k', linewidth = 3, markersize = 10)
pylab.axhline(.5,color='k',linestyle=':')
ax = pylab.subplot(1,2,2,sharey=ax)
pylab.plot([0,1],[np.mean(c_pre_frac, 1),np.mean(c_post_frac,1)],'.-b')
ax.set_xticks((0,1))
ax.set_xticklabels(('pre','post'))
pylab.xlim((-.25,1.25))
pylab.ylim((0,1))
pylab.ylabel('Percent Time on Cocaine Color (Control)')
pylab.hold(True)
pylab.errorbar([0,1],[np.mean(c_pre_frac),np.mean(c_post_frac)], yerr=2*scipy.stats.sem([np.mean(c_pre_frac,1),np.mean(c_post_frac,1)], axis = 1), capsize = 5, fmt = '.-k', linewidth = 3, markersize = 10)
pylab.axhline(.5,color='k',linestyle=':')
pylab.show()

pylab.figure(2)
pylab.clf()
pylab.suptitle('Effect of Cocaine CCP (0.25uM) Experimental Fish')
ax = pylab.subplot(1,2,1)
pylab.plot([0,1],[np.mean(e_prel_frac, 1),np.mean(e_postl_frac,1)],'.-r')
ax.set_xticks((0,1))
ax.set_xticklabels(('pre','post'))
pylab.xlim((-.25,1.25))
pylab.ylim((0,1))
pylab.ylabel('Percent Time on Cocaine Color (Experimental)')
pylab.hold(True)
pylab.errorbar([0,1],[np.mean(e_prel_frac),np.mean(e_postl_frac)], yerr=2*scipy.stats.sem([np.mean(e_pre_frac,1),np.mean(e_post_frac,1)], axis = 1), capsize = 5, fmt = '.-k', linewidth = 3, markersize = 10)
pylab.axhline(.5,color='k',linestyle=':')
ax = pylab.subplot(1,2,2,sharey=ax)
pylab.plot([0,1],[np.mean(c_pre_frac, 1),np.mean(c_post_frac,1)],'.-b')
ax.set_xticks((0,1))
ax.set_xticklabels(('pre','post'))
pylab.xlim((-.25,1.25))
pylab.ylim((0,1))
pylab.ylabel('Percent Time on Cocaine Color (Control)')
pylab.hold(True)
pylab.errorbar([0,1],[np.mean(c_pre_frac),np.mean(c_post_frac)], yerr=2*scipy.stats.sem([np.mean(c_pre_frac,1),np.mean(c_post_frac,1)], axis = 1), capsize = 5, fmt = '.-k', linewidth = 3, markersize = 10)
pylab.axhline(.5,color='k',linestyle=':')
pylab.show()

pylab.figure(7)
pylab.clf()
pylab.suptitle('Effect of Cocaine CCP (1.6uM) Experimental Fish')
ax = pylab.subplot(1,2,1)
pylab.plot([0,1],[np.mean(e_pre1_frac, 1),np.mean(e_post1_frac,1)],'.-r')
ax.set_xticks((0,1))
ax.set_xticklabels(('pre','post'))
pylab.xlim((-.25,1.25))
pylab.ylim((0,1))
pylab.ylabel('Percent Time on Cocaine Color (Experimental)')
pylab.hold(True)
pylab.errorbar([0,1],[np.mean(e_pre1_frac),np.mean(e_post1_frac)], yerr=2*scipy.stats.sem([np.mean(e_pre1_frac,1),np.mean(e_post1_frac,1)], axis = 1), capsize = 5, fmt = '.-k', linewidth = 3, markersize = 10)
pylab.axhline(.5,color='k',linestyle=':')
ax = pylab.subplot(1,2,2,sharey=ax)
pylab.plot([0,1],[np.mean(c_pre_frac, 1),np.mean(c_post_frac,1)],'.-b')
ax.set_xticks((0,1))
ax.set_xticklabels(('pre','post'))
pylab.xlim((-.25,1.25))
pylab.ylim((0,1))
pylab.ylabel('Percent Time on Cocaine Color (Control)')
pylab.hold(True)
pylab.errorbar([0,1],[np.mean(c_pre_frac),np.mean(c_post_frac)], yerr=2*scipy.stats.sem([np.mean(c_pre_frac,1),np.mean(c_post_frac,1)], axis = 1), capsize = 5, fmt = '.-k', linewidth = 3, markersize = 10)
pylab.axhline(.5,color='k',linestyle=':')
pylab.show()

pylab.figure(8)
pylab.clf()
pylab.suptitle('Effect of Cocaine CCP (4.125uM) Experimental Fish')
ax = pylab.subplot(1,2,1)
pylab.plot([0,1],[np.mean(e_pre3_frac, 1),np.mean(e_post3_frac,1)],'.-r')
ax.set_xticks((0,1))
ax.set_xticklabels(('pre','post'))
pylab.xlim((-.25,1.25))
pylab.ylim((0,1))
pylab.ylabel('Percent Time on Cocaine Color (Experimental)')
pylab.hold(True)
pylab.errorbar([0,1],[np.mean(e_pre3_frac),np.mean(e_post3_frac)], yerr=2*scipy.stats.sem([np.mean(e_pre3_frac,1),np.mean(e_post3_frac,1)], axis = 1), capsize = 5, fmt = '.-k', linewidth = 3, markersize = 10)
pylab.axhline(.5,color='k',linestyle=':')
ax = pylab.subplot(1,2,2,sharey=ax)
pylab.plot([0,1],[np.mean(c_pre_frac, 1),np.mean(c_post_frac,1)],'.-b')
ax.set_xticks((0,1))
ax.set_xticklabels(('pre','post'))
pylab.xlim((-.25,1.25))
pylab.ylim((0,1))
pylab.ylabel('Percent Time on Cocaine Color (Control)')
pylab.hold(True)
pylab.errorbar([0,1],[np.mean(c_pre_frac),np.mean(c_post_frac)], yerr=2*scipy.stats.sem([np.mean(c_pre_frac,1),np.mean(c_post_frac,1)], axis = 1), capsize = 5, fmt = '.-k', linewidth = 3, markersize = 10)
pylab.axhline(.5,color='k',linestyle=':')
pylab.show()

pylab.figure(9)
pylab.clf()
pylab.suptitle('Effect of Cocaine CCP (0.041uM) Experimental Fish')
ax = pylab.subplot(1,2,1)
pylab.plot([0,1],[np.mean(e_prep4_frac, 1),np.mean(e_postp4_frac,1)],'.-r')
ax.set_xticks((0,1))
ax.set_xticklabels(('pre','post'))
pylab.xlim((-.25,1.25))
pylab.ylim((0,1))
pylab.ylabel('Percent Time on Cocaine Color (Experimental)')
pylab.hold(True)
pylab.errorbar([0,1],[np.mean(e_prep4_frac),np.mean(e_postp4_frac)], yerr=2*scipy.stats.sem([np.mean(e_prep4_frac,1),np.mean(e_postp4_frac,1)], axis = 1), capsize = 5, fmt = '.-k', linewidth = 3, markersize = 10)
pylab.axhline(.5,color='k',linestyle=':')
ax = pylab.subplot(1,2,2,sharey=ax)
pylab.plot([0,1],[np.mean(c_pre_frac, 1),np.mean(c_post_frac,1)],'.-b')
ax.set_xticks((0,1))
ax.set_xticklabels(('pre','post'))
pylab.xlim((-.25,1.25))
pylab.ylim((0,1))
pylab.ylabel('Percent Time on Cocaine Color (Control)')
pylab.hold(True)
pylab.errorbar([0,1],[np.mean(c_pre_frac),np.mean(c_post_frac)], yerr=2*scipy.stats.sem([np.mean(c_pre_frac,1),np.mean(c_post_frac,1)], axis = 1), capsize = 5, fmt = '.-k', linewidth = 3, markersize = 10)
pylab.axhline(.5,color='k',linestyle=':')
pylab.show()

pylab.figure(10)
pylab.clf()
pylab.suptitle('Effect of Cocaine CCP (10uM) Experimental Fish', ha = 'center')
ax = pylab.subplot(1,2,1)
pylab.plot([0,1],[np.mean(e_preten_frac, 1),np.mean(e_postten_frac,1)],'.-r')
ax.set_xticks((0,1))
ax.set_xticklabels(('pre','post'))
pylab.xlim((-.25,1.25))
pylab.ylim((0,1))
pylab.ylabel('Percent Time on Cocaine Color (Experimental)')
pylab.hold(True)
pylab.errorbar([0,1],[np.mean(e_preten_frac),np.mean(e_postten_frac)], yerr=2*scipy.stats.sem([np.mean(e_preten_frac,1),np.mean(e_postten_frac,1)], axis = 1), capsize = 5, fmt = '.-k', linewidth = 3, markersize = 10)
pylab.axhline(.5,color='k',linestyle=':')
ax = pylab.subplot(1,2,2,sharey=ax)
pylab.plot([0,1],[np.mean(c_pre_frac, 1),np.mean(c_post_frac,1)],'.-b')
ax.set_xticks((0,1))
ax.set_xticklabels(('pre','post'))
pylab.xlim((-.25,1.25))
pylab.ylim((0,1))
pylab.ylabel('Percent Time on Cocaine Color (Control)')
pylab.hold(True)
pylab.errorbar([0,1],[np.mean(c_pre_frac),np.mean(c_post_frac)], yerr=2*scipy.stats.sem([np.mean(c_pre_frac,1),np.mean(c_post_frac,1)], axis = 1), capsize = 5, fmt = '.-k', linewidth = 3, markersize = 10)
pylab.axhline(.5,color='k',linestyle=':')
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
ePreVel = getVelMulti(e_pre, (900, 1800))
ePostVel1 = getVelMulti(e_post, (0,900))
ePostVel2 = getVelMulti(e_post, (45*60-600,45*60))
ePreLV = getVelMulti(e_low_pre, (900, 1800))
ePostLV1 = getVelMulti(e_low_post, (0,900))
ePostLV2 = getVelMulti(e_low_post, (30*60-600,30*60))
cPreVel = getVelMulti(c_pre, (900, 1800))
cPostVel1 = getVelMulti(c_post, (0,900))
cPostVel2 = getVelMulti(c_post, (90*60-600,90*60))
"""
[tv, e_Shock_LH] = scipy.stats.ttest_ind(eShockVel, eLHVel)
[tv, e_Shock_Nov] = scipy.stats.ttest_ind(eShockVel, eNovVel)
[tv, e_LH_Nov] = scipy.stats.ttest_ind(eLHVel, eNovVel)

print 'Velocity at Shock, Real Time Test, Novel (exp): ', eShockVel, eLHVel, eNovVel
print 'Statistcs comparing Shock/LH, Shock/Nov, LH/Nov: ', e_Shock_LH, e_Shock_Nov, e_LH_Nov
"""
pylab.figure(3)
ax = pylab.subplot(1,3,1)
pylab.plot([0,1,2],[ePreVel,ePostVel1, ePostVel2],'.-r')
ax.set_xticks((0,1,2))
ax.set_xticklabels(('pre','post first 15 min', 'post last 15 min'))
pylab.xlim((-.25,2.25))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Fish in 5uM, post=45min after (~60 min after cocaine)')
pylab.suptitle('Effect of cocaine on velocity')
ax = pylab.subplot(1,3,2)
pylab.plot([0,1,2],[ePreLV,ePostLV1, ePostLV2],'.-r')
ax.set_xticks((0,1,2))
ax.set_xticklabels(('pre (low)','post (low) first 15 min', 'post (low) last 15 min'))
pylab.xlim((-.25,2.25))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Fish in 0.25uM, post=30min after')
ax = pylab.subplot(1,3,3)
pylab.plot([0,1,2],[cPreVel,cPostVel1, cPostVel2],'.-r')
ax.set_xticks((0,1,2))
ax.set_xticklabels(('pre','post first 15 min', 'post last 15 min'))
pylab.xlim((-.25,2.25))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Fish in 0uM (control), post=90min after')

pylab.figure(4)
ax = pylab.subplot(1,3,1)
pylab.plot([0,1],[ePreVel, ePostVel2],'.-r')
ax.set_xticks((0,1))
ax.set_xticklabels(('pre','post last 15 min'))
pylab.xlim((-.25,1.25))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Fish in 5uM, post=45min after (~60 min after cocaine)')
pylab.suptitle('Effect of cocaine on velocity')
ax = pylab.subplot(1,3,2)
pylab.plot([0,1],[ePreLV,ePostLV2],'.-r')
ax.set_xticks((0,1))
ax.set_xticklabels(('pre (low)', 'post (low) last 15 min'))
pylab.xlim((-.25,1.25))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Fish in 0.25uM, post=30min after')
ax = pylab.subplot(1,3,3)
pylab.plot([0,1],[cPreVel, cPostVel2],'.-r')
ax.set_xticks((0,1))
ax.set_xticklabels(('pre', 'post last 15 min'))
pylab.xlim((-.25,1.25))
pylab.ylabel('Median Velocity (mm/s)')
pylab.title('Fish in 0uM (control), post=90min after')



pylab.show()


