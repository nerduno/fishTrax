import ArenaBehaviorAnalysis as aba
import pylab
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import pylab
import scipy

#5mm bars 30 on 60 off
c_omr_5mm = ['/home/vburns/Dropbox/ConchisData/2013-09-30/f00641/f00641_2013-09-30-11-27-45.json',
             '/home/vburns/Dropbox/ConchisData/2013-09-30/f00642/f00642_2013-09-30-11-27-58.json',
             '/home/vburns/Dropbox/ConchisData/2013-09-30/f00643/f00643_2013-09-30-11-28-08.json',
             '/home/vburns/Dropbox/ConchisData/2013-09-30/f00644/f00644_2013-09-30-11-28-19.json',
             #'/home/vburns/Dropbox/ConchisData/2013-09-30/f00645/f00645_2013-09-30-11-28-27.json',
             '/home/vburns/Dropbox/ConchisData/2013-09-30/f00646/f00646_2013-09-30-11-28-34.json',
             '/home/vburns/Dropbox/ConchisData/2013-09-30/f00647/f00647_2013-09-30-11-28-41.json',
             '/home/vburns/Dropbox/ConchisData/2013-09-30/f00648/f00648_2013-09-30-11-28-52.json',
# '/home/vburns/Dropbox/ConchisData/2013-09-27/f00625/f00625_2013-09-27-14-19-33.json',
# '/home/vburns/Dropbox/ConchisData/2013-09-27/f00626/f00626_2013-09-27-14-19-26.json',
# '/home/vburns/Dropbox/ConchisData/2013-09-27/f00627/f00627_2013-09-27-14-19-21.json',
# '/home/vburns/Dropbox/ConchisData/2013-09-27/f00628/f00628_2013-09-27-14-19-17.json',
# '/home/vburns/Dropbox/ConchisData/2013-09-27/f00629/f00629_2013-09-27-14-19-13.json',
# '/home/vburns/Dropbox/ConchisData/2013-09-27/f00630/f00630_2013-09-27-14-19-08.json',
# '/home/vburns/Dropbox/ConchisData/2013-09-27/f00631/f00631_2013-09-27-14-19-04.json',
# '/home/vburns/Dropbox/ConchisData/2013-09-27/f00632/f00632_2013-09-27-14-18-59.json',
# '/home/vburns/Dropbox/ConchisData/2013-09-27/f00633/f00633_2013-09-27-14-22-01.json',
# '/home/vburns/Dropbox/ConchisData/2013-09-27/f00634/f00634_2013-09-27-14-22-09.json',
# '/home/vburns/Dropbox/ConchisData/2013-09-27/f00635/f00635_2013-09-27-14-22-17.json',
# '/home/vburns/Dropbox/ConchisData/2013-09-27/f00636/f00636_2013-09-27-14-22-30.json',
# '/home/vburns/Dropbox/ConchisData/2013-09-27/f00637/f00637_2013-09-27-14-22-43.json',
# '/home/vburns/Dropbox/ConchisData/2013-09-27/f00638/f00638_2013-09-27-14-22-53.json',
# '/home/vburns/Dropbox/ConchisData/2013-09-27/f00639/f00639_2013-09-27-14-23-03.json',
# '/home/vburns/Dropbox/ConchisData/2013-09-27/f00640/f00640_2013-09-27-14-23-12.json'
]
c_omr_5mm = aba.loadMultipleDataFiles(c_omr_5mm)

c_omr_2mm = ['/home/vburns/Dropbox/ConchisData/2013-09-30/f00649/f00649_2013-09-30-11-30-50.json',
             '/home/vburns/Dropbox/ConchisData/2013-09-30/f00650/f00650_2013-09-30-11-31-37.json',
             '/home/vburns/Dropbox/ConchisData/2013-09-30/f00651/f00651_2013-09-30-11-31-42.json',
             '/home/vburns/Dropbox/ConchisData/2013-09-30/f00652/f00652_2013-09-30-11-31-52.json',
             '/home/vburns/Dropbox/ConchisData/2013-09-30/f00653/f00653_2013-09-30-11-32-07.json',
             '/home/vburns/Dropbox/ConchisData/2013-09-30/f00654/f00654_2013-09-30-11-32-17.json',
             #'/home/vburns/Dropbox/ConchisData/2013-09-30/f00655/f00655_2013-09-30-11-32-24.json',
             '/home/vburns/Dropbox/ConchisData/2013-09-30/f00656/f00656_2013-09-30-11-32-31.json']
c_omr_2mm = aba.loadMultipleDataFiles(c_omr_2mm)

c_omr_8mm_slow = ['/home/vburns/Dropbox/ConchisData/2013-09-30/f00657/f00657_2013-09-30-14-30-02.json',
                  '/home/vburns/Dropbox/ConchisData/2013-09-30/f00658/f00658_2013-09-30-14-30-12.json',
                  '/home/vburns/Dropbox/ConchisData/2013-09-30/f00659/f00659_2013-09-30-14-30-20.json',
                  '/home/vburns/Dropbox/ConchisData/2013-09-30/f00660/f00660_2013-09-30-14-30-26.json',
                  '/home/vburns/Dropbox/ConchisData/2013-09-30/f00661/f00661_2013-09-30-14-30-40.json',
                  '/home/vburns/Dropbox/ConchisData/2013-09-30/f00662/f00662_2013-09-30-14-30-48.json',
                  '/home/vburns/Dropbox/ConchisData/2013-09-30/f00663/f00663_2013-09-30-14-30-56.json',
                  '/home/vburns/Dropbox/ConchisData/2013-09-30/f00664/f00664_2013-09-30-14-31-05.json']
c_omr_8mm_slow = aba.loadMultipleDataFiles(c_omr_8mm_slow)

c_omr_8mm_fast = [#'/home/vburns/Dropbox/ConchisData/2013-09-30/f00665/f00665_2013-09-30-14-32-02.json',
                  #'/home/vburns/Dropbox/ConchisData/2013-09-30/f00666/f00666_2013-09-30-14-32-10.json',
                  '/home/vburns/Dropbox/ConchisData/2013-09-30/f00667/f00667_2013-09-30-14-32-15.json',
                  '/home/vburns/Dropbox/ConchisData/2013-09-30/f00668/f00668_2013-09-30-14-32-21.json',
                  '/home/vburns/Dropbox/ConchisData/2013-09-30/f00669/f00669_2013-09-30-14-32-31.json',
                  '/home/vburns/Dropbox/ConchisData/2013-09-30/f00670/f00670_2013-09-30-14-32-38.json',
                  '/home/vburns/Dropbox/ConchisData/2013-09-30/f00671/f00671_2013-09-30-14-32-44.json',
                  '/home/vburns/Dropbox/ConchisData/2013-09-30/f00672/f00672_2013-09-30-14-33-01.json']
c_omr_8mm_fast= aba.loadMultipleDataFiles(c_omr_8mm_fast)

c_omr_10mm_fast = ['/home/vburns/Dropbox/ConchisData/2013-09-30/f00673/f00673_2013-09-30-19-25-37.json',
                   '/home/vburns/Dropbox/ConchisData/2013-09-30/f00674/f00674_2013-09-30-19-25-40.json',
                   '/home/vburns/Dropbox/ConchisData/2013-09-30/f00675/f00675_2013-09-30-19-25-44.json',
                   '/home/vburns/Dropbox/ConchisData/2013-09-30/f00676/f00676_2013-09-30-19-25-47.json',
                   '/home/vburns/Dropbox/ConchisData/2013-09-30/f00677/f00677_2013-09-30-19-25-50.json',
                   '/home/vburns/Dropbox/ConchisData/2013-09-30/f00678/f00678_2013-09-30-19-25-52.json',
                   '/home/vburns/Dropbox/ConchisData/2013-09-30/f00679/f00679_2013-09-30-19-25-55.json',
                   '/home/vburns/Dropbox/ConchisData/2013-09-30/f00680/f00680_2013-09-30-19-25-58.json'
]
c_omr_10mm_fast = aba.loadMultipleDataFiles(c_omr_10mm_fast)

c_omr_10mm_slow = [#'/home/vburns/Dropbox/ConchisData/2013-09-30/f00681/f00681_2013-09-30-19-25-07.json',
                   '/home/vburns/Dropbox/ConchisData/2013-09-30/f00682/f00682_2013-09-30-19-25-10.json',
                   '/home/vburns/Dropbox/ConchisData/2013-09-30/f00683/f00683_2013-09-30-19-25-13.json',
                   '/home/vburns/Dropbox/ConchisData/2013-09-30/f00684/f00684_2013-09-30-19-25-17.json',
                   '/home/vburns/Dropbox/ConchisData/2013-09-30/f00685/f00685_2013-09-30-19-25-21.json',
                   '/home/vburns/Dropbox/ConchisData/2013-09-30/f00686/f00686_2013-09-30-19-25-24.json',
                   '/home/vburns/Dropbox/ConchisData/2013-09-30/f00687/f00687_2013-09-30-19-25-26.json',
                   '/home/vburns/Dropbox/ConchisData/2013-09-30/f00688/f00688_2013-09-30-19-25-29.json'
                   ]
c_omr_10mm_slow = aba.loadMultipleDataFiles(c_omr_10mm_slow)



c_1 = c_omr_10mm_fast
cTitle = '10mm fast'
e_1 = c_omr_5mm
eTitle = '5mm'

#omr analysis
omr_tp = 12
eBaseResults = aba.getOMRScoreStatsMulti(e_1, stateRange=[3,3],timePoint=omr_tp)
eEndResults = aba.getOMRScoreStatsMulti(e_1, stateRange=[8,8],timePoint=omr_tp)
cBaseResults = aba.getOMRScoreStatsMulti(c_1, stateRange=[3,3],timePoint=omr_tp)
cEndResults = aba.getOMRScoreStatsMulti(c_1, stateRange=[8,8],timePoint=omr_tp)

def plotOMRMetric(cond1base, cond1end, cond2base, cond2end, title, baseTitle, endTitle, cond1label, cond2label):
    ax = pyplot.gca()
    ax.plot([0,1],[np.mean(cond1base), np.mean(cond1end)],'o-k',lw=3, label=cond1label)
    sem2 = (2*scipy.stats.sem(cond1base), 2*scipy.stats.sem(cond1end))
    pyplot.errorbar([0,1],[np.mean(cond1base), np.mean(cond1end)],fmt='ok',yerr=sem2, lw=3)

    ax.plot([0,1],[np.mean(cond2base), np.mean(cond2end)],'o-m',lw=3, label=cond2label)
    sem2 = (2*scipy.stats.sem(cond2base), 2*scipy.stats.sem(cond2end))
    pyplot.errorbar([0,1],[np.mean(cond2base), np.mean(cond2end)],fmt='om',yerr=sem2, lw=3)
   
    handles, labels= ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    ax.set_xticks((0,1))
    ax.set_xticklabels((baseTitle, endTitle))
    pyplot.xlim((-.25,1.5))
    pyplot.ylim((0,1))
 
    _, pre_p = scipy.stats.ttest_rel(cond1base, cond2base)
    _, post_p = scipy.stats.ttest_rel(cond1end, cond2end)
    pyplot.title('%s %0.3f %0.3f'%(title,pre_p,post_p))


pyplot.figure()
pylab.suptitle('Is OMR working?')
pylab.subplot(231)
plotOMRMetric(cBaseResults['omrResults']['avgmaxdist'], cEndResults['omrResults']['avgmaxdist'],
              cBaseResults['omrControl']['avgmaxdist'], cEndResults['omrControl']['avgmaxdist'],
              '%s maxdist'%cTitle, 'pre', 'post', 'omr', 'nonomr')
pylab.subplot(232)
plotOMRMetric(cBaseResults['omrResults']['avgnorm'], cEndResults['omrResults']['avgnorm'],
              cBaseResults['omrControl']['avgnorm'], cEndResults['omrControl']['avgnorm'],
              '%s maxdist'%cTitle, 'pre', 'post', 'omr', 'nonomr')
pylab.subplot(234)
plotOMRMetric(eBaseResults['omrResults']['avgmaxdist'], eEndResults['omrResults']['avgmaxdist'],
              eBaseResults['omrControl']['avgmaxdist'], eEndResults['omrControl']['avgmaxdist'],
              '%s maxdist'%eTitle, 'pre', 'post', 'omr', 'nonomr')
pylab.subplot(235)
plotOMRMetric(eBaseResults['omrResults']['avgnorm'], eEndResults['omrResults']['avgnorm'],
              eBaseResults['omrControl']['avgnorm'], eEndResults['omrControl']['avgnorm'],
              '%s maxdist'%eTitle, 'pre', 'post', 'omr', 'nonomr')

pyplot.figure()
color = ['k','r','g','m','c','b']
style = ['-',':']
#conditions = [c_omr_5mm, c_omr_8mm_slow, c_omr_8mm_fast, c_omr_10mm_slow]
conditions = [c_omr_2mm, c_omr_5mm, c_omr_8mm_slow, c_omr_8mm_fast, c_omr_10mm_slow, c_omr_10mm_fast]
for i,d in enumerate(conditions):
    m = []
    m_sem = []
    p = []
    stats = ['avgmaxdist','avgtotdist','avgfractime','avgnorm']
    for s,stat in enumerate(stats):
        tp = np.arange(2,21,2)
        m.append({'omr':np.zeros(len(tp)),'non':np.zeros(len(tp))})
        m_sem.append({'omr':np.zeros(len(tp)),'non':np.zeros(len(tp))})
        p.append([])
        for n,timePoint in enumerate(tp):
            #this call needs to be moved outside the stat loop, but timepoing and stat need to be flipped first.
            r = aba.getOMRScoreStatsMulti(d, stateRange=[8,8], timePoint=timePoint)
            m[s]['omr'][n] = r['omrResults'][stat].mean()
            m_sem[s]['omr'][n] = scipy.stats.sem(r['omrResults'][stat])
            if stat in r['omrControl'].dtype.fields.keys():
                m[s]['non'][n] = r['omrControl'][stat].mean()
                m_sem[s]['non'][n] = scipy.stats.sem(r['omrControl'][stat])
                _,pval = scipy.stats.ttest_rel(r['omrResults'][stat],r['omrControl'][stat])            
                p[s].append(pval)
                
        pyplot.subplot(len(stats),2,s*2+1)
        pyplot.errorbar(tp+i/20.0, m[s]['omr'], color=color[i], linestyle='-', yerr=m_sem[s]['omr'], lw=2 , 
                        label='bar%f speed%f'%(d[0]['parameters']['OMR_period'], d[0]['parameters']['OMR_velocity']))
        pyplot.xlabel('Time after OMR start (s)')
        pyplot.ylabel(stat)
        if stat in r['omrControl'].dtype.fields.keys():
            pyplot.errorbar(tp+i/20.0, m[s]['non'], color=color[i], linestyle=':', yerr=m_sem[s]['non'], lw=2 , 
                            label='control bar%f speed%f'%(d[0]['parameters']['OMR_period'], d[0]['parameters']['OMR_velocity']))
            pyplot.subplot(len(stats),2,s*2+2)
            pyplot.semilogy(tp,p[s], color=color[i], lw=2)
            pyplot.xlabel('Time after OMR start (s)')
            pyplot.ylabel('p value')

pyplot.subplot(len(stats),2,1)
fontP = mpl.font_manager.FontProperties()
fontP.set_size('xx-small')
handles, labels= pyplot.gca().get_legend_handles_labels()
pyplot.gca().legend(handles, labels, loc=2, prop=fontP)        
pylab.show()
