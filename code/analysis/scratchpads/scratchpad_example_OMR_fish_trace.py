import ArenaBehaviorAnalysis as aba

#make sure fish are loaded

#6,7,9,13
fish = e_omr_same[7]

def plotFishPositionVsTime(jsonData, startState=1, endState=0, smooth=5, axis=0, fmt='b-',wid=1):
    state = jsonData['stateinfo']
    midLine = (jsonData['tankSize_mm'][axis])/2.0

    st,_,nS,_ = aba.state_to_time(jsonData,startState)
    _,et,_,nE = aba.state_to_time(jsonData,endState)

    tracking = aba.getTracking(jsonData)
    tracking = tracking[np.logical_and(tracking[:,0] > st, tracking[:,0] < et),:].copy()
    frametime = tracking[:,0] - st
    position = tracking[:,axis+1]
    
    if 'OMRinfo' in jsonData.keys():
        results = aba.getOMRinfo(jsonData, tankLength =midLine*2)
        color = {-1:'red', 1:'blue'}
        hatch = {-1:'\\', 1:'/'}
        os = results['omrResults']['st']
        oe = results['omrResults']['et']
        od = results['omrResults']['dir']
        for n in range(len(os)):
            p1 = mpl.patches.Rectangle((os[n]-st,0),
                                       width=oe[n]-os[n],
                                       height=midLine*2,alpha=0.5,
                                       color=[.5,1,.5],hatch=hatch[od[n]])
            pyplot.gca().add_patch(p1)
            #pyplot.text(os[n]-st+(oe[n]-os[n])/3, 45, '%0.2f'%results['omrResults']['maxdist'][n])

    pyplot.plot(frametime, position, fmt, lw=1)
    if smooth>0:
        import scipy
        pyplot.plot(frametime, scipy.convolve(position,np.ones(smooth)/smooth, mode='same'))
    pyplot.ylim([0,midLine*2])
    pyplot.xlim([0,et-st])
    if axis==0:
        pyplot.ylabel('')
    else:
        pyplot.ylabel('')
    pyplot.xlabel('Time (s)')

fig=pyplot.figure(1,figsize=(11,4))
pyplot.clf()
ax=pyplot.subplot(121)

plotFishPositionVsTime(fish)
pyplot.xlim((250,900))
ax.set_yticks([0,20,40])
#ax.set_xticks([0,150,300,450])
#ax.set_xticklabels([])
ax=pyplot.subplot(122)
plotFishPositionVsTime(fish)
pyplot.xlim((3050, 3700))
ax.set_yticks([0,20,40])
#ax.set_xticks([3300,3450,3600])
#ax.set_xticklabels([])

pyplot.show()
