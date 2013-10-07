import sys, os
import math, random, time, logging, datetime, json, cv
import numpy as np
import scipy.stats as stats
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import matplotlib.patches
import tkFileDialog
import PerspectiveTransform
import pdb
import glob
import pprint
import traceback

defArena= [(0,0),(0,22),(48,22),(48,0)]

def loadDataFromFile(filename, arena_mm = defArena):
    with open(os.path.expanduser(filename)) as f:
        jsonData = json.load(f)

    if 'tankSize_mm' in jsonData.keys():
        arena_mm = [(0                           ,0),
                    (0                           ,jsonData['tankSize_mm'][1]),
                    (jsonData['tankSize_mm'][0]  ,jsonData['tankSize_mm'][1]),
                    (jsonData['tankSize_mm'][0]  ,0)]
        print 'Ignoring arena_mm.  Using tankSize_mm field.'
    else:
        jsonData['tankSize_mm'] = [arena_mm[2][0], arena_mm[2][1]]
    jsonData['warpedTracking'] = getWarpedAndCleanedTracking(jsonData, warpTarget=arena_mm)
    jsonData['filename'] = filename
    return jsonData

def loadDataFromFile_AvgMultiFish(filename, arena_mm = defArena):
    with open(os.path.expanduser(filename)) as f:
        jsonData = json.load(f)

    if 'tankSize_mm' in jsonData.keys():
        arena_mm = [(0,0),(0,jsonData['tankSize_mm'][1]),(jsonData['tankSize_mm'][0],jsonData['tankSize_mm'][1]),(jsonData['tankSize_mm'][0],jsonData['tankSize_mm'][1])]
        print 'Ignoring arena_mm.  Using tankSize_mm field.'
    else:
        jsonData['tankSize_mm'] = [arena_mm[2][0], arena_mm[2][1]]

    for nFrame in range(len(jsonData['tracking'])):
        jsonData['tracking'][nFrame] = (jsonData['tracking'][nFrame][0],
                                        np.mean(jsonData['tracking'][nFrame][1:-1:2]),
                                        np.mean(jsonData['tracking'][nFrame][2:-1:2]))
    jsonData['warpedTracking'] = getWarpedAndCleanedTracking(jsonData, warpTarget=arena_mm)
    return jsonData

def loadDataFromFolder(foldername, whichJson=0,arena_mm = defArena):
    filelist = glob.glob(fishDir+os.sep+'*.json')
    #filelist = os.listdir(fishDir)
    #filelist = filter(lambda x: x.endswith('json'), filelist)
    filelist.sort()
    if len(filelist) == 0:
        print 'No json files found'
        return None
    if len(filelist) > 1:
        print 'Warning multiple JSONs found, using first by default.'
    return loadDataFromFile(fishDir + os.sep + filelist[whichJson], arena_mm)

def loadDataFromFile_UI(filename, arena_mm=defArena):
    f = tkFileDialog.askopenfile()
    jsonData = loadDataFromFile(f, arena_mm)
    return jsonData

def loadDataSmart(datestr,fishNum, arena_mm=defArena):
    smartdir = os.path.expanduser('~'+os.sep+'Dropbox'+os.sep+'ConchisData'+os.sep+datestr+os.sep)
    datedirlist = glob.glob(smartdir+'f%05d'%fishNum+'*.json')
    fishdirlist = glob.glob(smartdir+'f%05d'%fishNum+os.sep+'f%05d'%fishNum+'*.json')
    print '\nSearch string: '+smartdir+'f%05d'%fishNum+os.sep+'f%05d'%fishNum+'*.json'
    datedirlist.sort() 
    fishdirlist.sort()
    filelist = datedirlist + fishdirlist
    if len(filelist) == 0:
        print 'No files found'
        return (None,None)
    n = 0 
    print 'List of found files:' 
    for filename in filelist:
        print '   ',n,filename
        n+=1
    userInput = raw_input('Enter selection number: ')
    try:
        val = int(userInput)
        if val < len(filelist):
            return [loadDataFromFile(filelist[val], arena_mm), filelist[val]]
        else:
            print('Invalid selection')
            return (None,None)
    except ValueError:
        print("Invalid selection")
        return (None,None)

def loadMultipleDataFiles_Smart(arena_mm=defArena):
    datasets = []
    filenames = []
    
    import readline
    readline.parse_and_bind("tab: complete")
    
    while True:
        datestr = raw_input('Enter a date folder name (-1 to quit):')
        if datestr=='-1':
            break
        datedir = os.path.expanduser('~'+os.sep+'Dropbox'+os.sep+'ConchisData'+os.sep+datestr+os.sep)
        try:
            dlist = os.listdir(datedir)
        except:
            continue

        while True:
            pprint.pprint(dlist,indent=4)
            fishstr = raw_input('Enter a fish number (-1 to change date folder):')
            if fishstr=='-1':
                break
            try:
                [d,filename] = loadDataSmart(datestr,int(fishstr),arena_mm)
                if d:
                    datasets.append(d)
                    filenames.append(filename)
                    print ''
                    print '********************************'
                    print 'CURRENT LIST:'
                    for s in filenames:
                        print '\t%s'%s
                    print '********************************'
                    print ''
            except:
                traceback.print_exc()

    return (datasets, filenames)

def loadMultipleDataFiles(filenames,arena_mm=defArena):
    datasets = []
    for fn in filenames:
        datasets.append(loadDataFromFile(fn,arena_mm=arena_mm))
    return datasets

def getWarpedAndCleanedTracking(jsonData, warpTarget, tracking=[]):
    #Get and clean up data
    if not tracking:
        tracking = np.array(jsonData['tracking'])
    tracking = tracking[tracking[:,1]!=0,:] #remove frames where tracking failed
    if warpTarget is not None:
        #warp based on arena
        ac = jsonData['trackingParameters']['arenaPoly']
        arena_raw = [tuple(x) for x in jsonData['trackingParameters']['arenaPoly']]
        Mw = PerspectiveTransform.getWarpMatrix(arena_raw,warpTarget)
        warpP = PerspectiveTransform.warpPoints(tracking[:,1:3],Mw)
        tracking = np.vstack([tracking[:,0],warpP[:,0],warpP[:,1]])
        tracking = tracking.T
    return tracking

def getTracking(jsonData):
    if 'warpedTracking' in jsonData:
        return jsonData['warpedTracking']
    else:
        return np.array(jsonData['tracking'])

def getEscapePosition(jsonData):
    fEscapePosition = .5*80
    if 'fEscapePosition' in jsonData['parameters'].keys():
        fEscapePosition = jsonData['parameters']['fEscapePosition']*80
    return fEscapePosition

def getFrameRate(jsonData):
    fr = np.array(jsonData['tracking'])
    ufr = np.mean(np.diff(fr[:,0]))
    print "frame rate: ", 1/ufr
    #Output number of failed track times
    totalFrames = fr.shape[0]
    missedFrames = np.sum(np.logical_or(fr[:,1]==0, fr[:,1]==-1))
    print "fraction of frames where tracking failed: " , missedFrames, 'of', totalFrames, ':', float(missedFrames)/totalFrames

def plotFishPath(jsonData, trange = None, tracking = []):
    """
    Plot the path of the fish -- used warped tracking data if available.
    trange - tuple of len 2 indicating the time range to be plotted in seconds relative to T0.
    tracking - optional override for default tracking info.
    """
    if tracking == []:
        tracking = getTracking(jsonData)
    
    if not trange:
        tndx = range(tracking.shape[0])
    else:
        trange = trange + tracking[0,0]
        tndx = np.logical_and(tracking[:,0]>=trange[0], tracking[:,0]<trange[1])
    pyplot.plot(tracking[tndx,1],tracking[tndx,2],'k-')

def plotFishPathHeatmap(jsonData, trange = None, bins=50, tracking=[]):
    """
    make heatmap of fish position -- used warped tracking data if available.
    trange - tuple of len 2 indicating the time range to be plotted in seconds relative to T0.
    bins - the bins argurment to np.histogram2d
    tracking - optional override for default tracking info.
    return heatmap, xedges, yedges (See np.histogram2d)
    """
    if tracking == []:
        tracking = getTracking(jsonData)
    
    if not trange:
        tndx = range(tracking.shape[0])
    else:
        trange = trange + tracking[0,0]
        tndx = np.logical_and(tracking[:,0]>=trange[0], tracking[:,0]<trange[1])
    heatmap, xedges, yedges = np.histogram2d(tracking[tndx,1],tracking[tndx,2],bins=bins,normed=True)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    pyplot.imshow(heatmap,extent = extent, interpolation='nearest',vmin=0, cmap=pyplot.hot())
    return (heatmap, xedges, yedges)

def generateFishPathMovie(jsonData, filename, trange = None, fps=10, trail_len=5, 
                          trail_color=[0,0,1], track_color=[.8,.8,1], 
                          xl=None, yl=None, tracking = None):
    """
    Make an mp4 movie of fish path
    filename - the output filename
    trange - tuple of len 2 indicating the time range to be rendered in seconds relative to T0.
    fps - number of frames per second
    trail_len - length of the fish trail in seconds
    trail_color - the color of the resent path trail - None to hide
    track_color - the color of the entire prior track -- None to hide
    tracking - optional override of jsondata.getTracking.
    """
    import tempfile
    tmpdir = tempfile.mkdtemp(prefix='tmpfishpath')
    
    if tracking is None:
        tracking = getTracking(jsonData)
    
    if not trange:
        tndx = range(tracking.shape[0])
    else:
        trange = trange + tracking[0,0]
        tndx = np.logical_and(tracking[:,0]>=trange[0], tracking[:,0]<trange[1])

    tracking=tracking[tndx,:]

    #save individual frames to temporary directory
    frametimes = np.arange(tracking[0,0],tracking[-1,0],1.0/fps)
    ###HIGHLY INEFFICIENT
    pyplot.ioff()
    f = pyplot.figure(1)
    output_template = os.path.join(tmpdir, 'tmpfishpath_%07d.png')
    for i,t in enumerate(frametimes):
        pyplot.clf()
        if track_color is not None:
            trackndx = tracking[:,0]<t
            pyplot.plot(tracking[trackndx,1],tracking[trackndx,2],color=track_color)
        if trail_color is not None:
            trailndx = np.logical_and(tracking[:,0]>=t-trail_len, tracking[:,0]<t)
            pyplot.plot(tracking[trailndx,1],tracking[trailndx,2],color=trail_color)
        if xl is not None:
            pyplot.xlim(xl)
        if yl is not None:
            pyplot.ylim(yl)
        pyplot.savefig(output_template%i)
        print i, t-tracking[0,0]

    #create the movie
    cmd  = ['ffmpeg']
    cmd += ['-i', output_template]
    cmd += ['-vcodec', 'libx264']
    #cmd += ['-vpre', 'hq'] #this doesn't always work (depends on ffmpeg version) 
    cmd += ['-preset', 'slow'] #but neither does this
    cmd += ['-crf', '22']
    cmd += ['-y']
    #cmd += ['-s', '%dx%d'%(np.ceil(im_col.shape[1]*0.5)*2, np.ceil(im_col.shape[0]*0.5)*2)] #make size even
    cmd += ['-threads', '0']
    cmd += [filename]
    cmd_string = ''.join(["%s " % el for el in cmd])
    print 'Running: ', cmd_string
    try:
        import subprocess
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)  # Grab stderr as well...
        print result
        print 'Cleaning up tmp directory.'
        import glob
        filelist = glob.glob(os.path.join(tmpdir,'*.png'))
        for f in filelist:
            os.remove(f)
        time.sleep(1)
        os.rmdir(tmpdir)
        print 'Clean up complete.'
    except subprocess.CalledProcessError,e:                              # Handle error conditions
        print str(e) + '\nProgram output was:\n' + e.output
    finally:
        pyplot.ion()

def plotFishXPosition(jsonData, startState=1, endState=0, smooth=0, fmt='k.'):
    plotFishPositionVsTime(jsonData, startState=1, endState=0, smooth=0, axis=0, fmt=fmt)

def plotFishYPosition(jsonData, startState=1, endState=0, smooth=0, fmt='k.'):
    plotFishPositionVsTime(jsonData, startState=1, endState=0, smooth=0, axis=1, fmt=fmt)

def plotFishPositionVsTime(jsonData, startState=1, endState=0, smooth=0, axis=0, fmt='k.'):
    """
    For RealTime and ClassicalConditioning Data
    Plot x position over time.
    """
    state = jsonData['stateinfo']
    midLine = (jsonData['tankSize_mm'][axis])/2.0
   
    st,_,nS,_ = state_to_time(jsonData,startState)
    _,et,_,nE = state_to_time(jsonData,endState)

    tracking = getTracking(jsonData)
    tracking = tracking[np.logical_and(tracking[:,0] > st, tracking[:,0] < et),:].copy()
    frametime = tracking[:,0] - st
    position = tracking[:,axis+1]
    
    if 'OMRinfo' in jsonData.keys():
        results = getOMRinfo(jsonData, tankLength =midLine*2)
        color = {-1:'red', 1:'blue'}
        hatch = {-1:'\\', 1:'/'}
        os = results['omrResults']['st']
        oe = results['omrResults']['et']
        od = results['omrResults']['dir']
        for n in range(len(os)):
            p1 = mpl.patches.Rectangle((os[n]-st,0),
                                       width=oe[n]-os[n],
                                       height=midLine*2,alpha=0.5,
                                       color=color[od[n]],hatch=hatch[od[n]])
            pyplot.gca().add_patch(p1)
            pyplot.text(os[n]-st, midLine, '%0.2f'%results['omrResults']['maxdist'][n])

        color = {-1:'green', 1:'yellow'}
        hatch = {-1:'\\', 1:'/'}
        os = results['omrControl']['st']
        oe = results['omrControl']['et']
        od = results['omrControl']['dir']
        for n in range(len(os)):
            p1 = mpl.patches.Rectangle((os[n]-st,0),
                                       width=oe[n]-os[n],
                                       height=midLine*2,alpha=0.5,
                                       color=color[od[n]],hatch=hatch[od[n]])
            pyplot.gca().add_patch(p1)
            pyplot.text(os[n]-st, midLine, '%0.2f'%results['omrControl']['maxdist'][n])

    for i in range(nS,nE):
        c1 = state[i][2]
        c2 = state[i][3]
        c1 = 'Yellow' if c1=='On' else c1
        c1 = 'White' if c1=='Off' else c1
        c2 = 'Yellow' if c2=='On' else c2
        c2 = 'White' if c2=='Off' else c2

        p1 = mpl.patches.Rectangle((state[i][0]-st,0),
                                   width=state[i+1][0]-state[i][0],
                                   height=midLine,alpha=0.5,
                                   color=c1)
        p2 = mpl.patches.Rectangle((state[i][0]-st,midLine),
                                   width=state[i+1][0]-state[i][0],
                                   height=midLine,alpha=0.5,
                                   color=c2)
        pyplot.gca().add_patch(p1)
        pyplot.gca().add_patch(p2)
    pyplot.plot(frametime, position, fmt)
    if smooth>0:
        import scipy
        pyplot.plot(frametime, scipy.convolve(position,np.ones(smooth)/smooth, mode='same'), 'g-')
    pyplot.ylim([0,midLine*2])
    pyplot.xlim([0,et-st])
    if axis==0:
        pyplot.ylabel('x (mm)')
    else:
        pyplot.ylabel('y (mm)')
    pyplot.xlabel('Time (s)')

def plotOMRmetrics(runData, startState=1, endState=0, omrTimepoint=None):
    st,_,_,_ = state_to_time(runData,startState)
    _,et,_,_ = state_to_time(runData,endState)
    results = getOMRinfo(runData, timePoint = omrTimepoint)
    os = results['omrResults']['st']
    oe = results['omrResults']['et']
    ndx = np.nonzero(np.logical_and(os>st,oe<et))
    for k,c in zip(['norm','maxdist','ratio','sub'],['r','b','k','c']):
        omrScore = results['omrResults'][k]
        pyplot.plot(os[ndx] - st, omrScore[ndx],c)
        pyplot.axhline(omrScore[ndx].mean(), color=c)
    for k,c in zip(['norm','maxdist'],['r','b']):
        nonScore = results['omrControl'][k]
        pyplot.plot(os[ndx] - st, nonScore[ndx],c,linestyle=':')
        pyplot.axhline(nonScore[ndx].mean(), color=c,linestyle=':')
    import scipy.stats
    _,p = scipy.stats.ttest_rel(results['omrResults']['norm'],results['omrControl']['norm'])
    pyplot.title('p=%0.3f'%p)

def state_to_time(jsonData, state):
    """
    Returns the start time of the first occurence of the given state and the end time of the last occurance.
    Also returns the index of the first occurance and the index of the last occurance.
    """
    stateinfo = jsonData['stateinfo']
    ndx = np.nonzero(np.array(stateinfo)[:,1].astype('int')==state)[0]
    st = stateinfo[ndx[0]][0]
    if ndx[-1]+1 < len(stateinfo):
        et = stateinfo[ndx[-1]+1][0]
    else:
        et = stateinfo[ndx[-1]][0]
    return (st,et,ndx[0],ndx[-1])


def plotFishSummary(jsonData, startState=1, endState=0, smooth=0, xl=None, omrTimePoint=None):
    """
    For RealTime and ClassicalConditioning Data
    Plot x position over time.
    """
    state = jsonData['stateinfo']
    shockinfo = jsonData['shockinfo']
    midLine = (jsonData['tankSize_mm'][0])/2.0
    
    st,_,_,_ = state_to_time(jsonData,startState)
    _,et,_,_ = state_to_time(jsonData,endState)
    
    tracking = getTracking(jsonData)
    t0 = tracking[0,0]
    tracking = tracking[np.logical_and(tracking[:,0] > st, tracking[:,0] < et),:].copy()
    
    sizen = 4
    pyplot.figure()

    #plot x position
    ax = pyplot.subplot(sizen,1,1)
    plotFishXPosition(jsonData, startState, endState, smooth)
    pyplot.title(jsonData['filename'])

    #plot y position
    pyplot.subplot(sizen,1,2,sharex=ax)
    plotFishYPosition(jsonData, startState, endState, smooth)

    if 'OMRinfo' in jsonData.keys(): 
        #plot omr metric
        pyplot.subplot(sizen,1,3, sharex=ax)
        plotOMRmetrics(jsonData, startState, endState, omrTimePoint)
    
    pyplot.subplot(sizen, 1, 4)
    plotCurrent(jsonData)
    
def plotCurrent(jsonData, cond=[5], ylm=1):
    #input is voltage?
    resistor =1000.0
    shockinfo = jsonData['shockinfo']
    
    shockon = []
    current1 = []
    current2 = []
    for s in range(len(shockinfo)):
        shockon.append(shockinfo[s][1])
        current1.append(shockinfo[s][3])
        current2.append(shockinfo[s][4])
    current1=np.array(current1)
    current2=np.array(current2)
    current1= current1[np.array(shockon)]
    current2 = current2[np.array(shockon)] 
    for i in range(len(current1)):
        if current1[i]==None:
            current1[i] = 0
        if current2[i] == None: 
            current2[i] = 0
    pyplot.bar(np.array(range(len(current1)))+1, current1, width=0.25, color='r')
    pyplot.bar(np.array(range(len(current2)))+1.25, current2, width=0.25, color='b')
    pyplot.xlim((0,31))
    pyplot.ylim((0,ylm))
    pyplot.ylabel('Current (mA)')
    #mA because output is voltage /1000 resistor *1000 convert to mA
    pyplot.xlabel('Bout Number (Red = Side1, Blue = Side2)')

def plotColoredPath(runData, cond=[2,3], color='On'):
    state = runData['stateinfo']
    ndx = np.nonzero([x in cond for x in [y[1] for y in state]])[0]
    w = runData['warpedTracking']
    for switchNdx in ndx:
        bNdxWin = np.logical_and(w[:,0]>state[switchNdx][0], w[:,0]<state[switchNdx+1][0])
        if state[switchNdx][2]==color:
            pyplot.plot(w[bNdxWin,1],w[bNdxWin,2],'r')
        else:
            pyplot.plot(w[bNdxWin,1],w[bNdxWin,2],'b')

def plotFlippedPath(runData, tankLength=48, cond=[2,3], color='On'):
    state = runData['stateinfo']
    tankLength = jsonData['tankSize_mm'][0]
    ndx = np.nonzero([x in cond for x in [y[1] for y in state]])[0]
    w = runData['warpedTracking']
    for switchNdx in ndx:
        bNdxWin = np.logical_and(w[:,0]>state[switchNdx][0], w[:,0]<state[switchNdx+1][0])
        if state[switchNdx][2]==color:
            pyplot.plot(w[bNdxWin,1],w[bNdxWin,2],'k')
        else:
            pyplot.plot(tankLength-w[bNdxWin,1],w[bNdxWin,2],'k')


def computeOMRmetrics(OMRfp, direction, tankLength=48, timePoint=None):
    """
    Compute several measure of OMR performance.
    OMRfp - position of the fish during the time window to be scored each row consists of (time, xpos, ypos)
    direction - either 1 or -1, 1 indicates the fish should be moving toward side 2.
    """      
    if timePoint is not None:
        OMRfp = OMRfp[OMRfp[:,0] < OMRfp[0,0]+timePoint,:].copy()

    #compute max distance as score
    if direction == 1: 
        maxdist = (np.max(OMRfp[:,1])-OMRfp[0,1])/(tankLength-OMRfp[0,1])
    elif direction==-1:
        maxdist = (OMRfp[0,1]-np.min(OMRfp[:,1]))/OMRfp[0,1]
    else: 
        print "unknown direction"
        1/0

    #compute total distance
    if direction == 1:
        totalDist = (OMRfp[-1,1]-OMRfp[0,1])*direction/(tankLength-OMRfp[0,1])
    else:
        totalDist = (OMRfp[-1,1]-OMRfp[0,1])*direction/OMRfp[0,1]

    #compute time moving in correct direction
    dt = np.diff(OMRfp[:,0])
    dx = np.diff(OMRfp[:,1])
    movingtime = np.sum(dt[np.nonzero(dx*direction>0)])/(OMRfp[-1,0]-OMRfp[0,0])
    return (maxdist, totalDist, movingtime)

def getNumOMRBouts(runData):
    OMRdata = runData['OMRinfo']
    num = 0
    for omr in OMRdata:
        num += omr[1]
    return num

def getOMRinfo(runData, tankLength=48, timePoint=None):
    """
    Extract regions of OMR and compute preformance metric for each OMR region. 
    Use with contextual learned helplessness arena.
    Timepoint is number of seconds following OMR onset at which beavioe is assessed (by default full session is used)
    """
    tankLength = runData['tankSize_mm'][0]
    OMRdata = runData['OMRinfo'] #time, T/F, [directionX,direcctionY]
    fp = getTracking(runData)
    results = {}
    numOMR = getNumOMRBouts(runData)
    results['omrResults'] = np.zeros(numOMR, dtype=[('st','f8'),('et','f8'),('dir','f8'),('maxdist','f8'),('totdist','f8'),('fractime','f8'),('ratio','f8'),('sub','f8'),('norm','f8')])
    results['omrControl'] = np.zeros(numOMR, dtype=[('st','f8'),('et','f8'),('dir','f8'),('maxdist','f8'),('totdist','f8'),('fractime','f8'),('norm','f8')])
    results['omrRandom']  = np.zeros(numOMR, dtype=[('st','f8'),('et','f8'),('dir','f8'),('maxdist','f8'),('totdist','f8'),('fractime','f8')])
    ndx = 0
    for i in range(len(OMRdata)-1):
        if OMRdata[i][1]:
            prevOMREndTime = OMRdata[i-1][0]
            startTime = OMRdata[i][0]
            endTime = OMRdata[i+1][0]
            direction = OMRdata[i][2][0]

            #get data regarding nonOMR period as control
            cntlStartTime = startTime - (endTime-startTime) 
            cntlEndTime = startTime
            cntlOMRfp = fp[np.logical_and(fp[:,0] > cntlStartTime, fp[:,0] < cntlEndTime),:].copy()
            cntlDirection = np.sign(tankLength/2.0 - cntlOMRfp[0,1])
            (cMaxdist, cTotalDist, cMovingtime) = computeOMRmetrics(cntlOMRfp, cntlDirection, tankLength, timePoint)
            results['omrControl'][ndx] = (cntlStartTime,cntlEndTime,cntlDirection,cMaxdist,cTotalDist,cMovingtime,cMaxdist/(cMaxdist+1))

            randDir = random.choice([-1,1])
            (rMaxdist, rTotalDist, rMovingtime) = computeOMRmetrics(cntlOMRfp, randDir, tankLength, timePoint)
            results['omrRandom'][ndx]  = (cntlStartTime,cntlEndTime,randDir,rMaxdist,rTotalDist,rMovingtime)

            #get data regarding OMR period
            OMRfp = fp[np.logical_and(fp[:,0] > startTime, fp[:,0] < endTime),:].copy()
            (maxdist, totalDist, movingtime) = computeOMRmetrics(OMRfp, direction, tankLength, timePoint)
            results['omrResults'][ndx] = (startTime,endTime,direction,maxdist,totalDist,movingtime,maxdist/(cMaxdist+0.001),maxdist-cMaxdist,maxdist/(cMaxdist+1))
            ndx+=1
    return results

def getSidePreference(runData, tankLength=48, cond=[3,8], refState='Red',sideFrac=.5):
    """
    cond specifies for which state the preference will be extracted
    specifies the side description on which the returned data is based.  e.g. if refState is red then
    then timeOnRefState will be the amount of time spent on red.
    data should be warped so that side1 is always 0 to midline.
    returns (timeOnRefState1, timeOnSide1, switchDuration, distFromRefState1, distFromSide1, startTime)
    """
    tankLength = jsonData['tankSize_mm'][0]

    timeOnSide1 = []
    switchDuration = []
    timeOnColor1 = []
    distFromSide1 = []
    distFromColor1 = []
    startTime = []

    state = runData['stateinfo']

    #HACK
    ndx = np.nonzero([x in cond for x in [y[1] for y in state]])[0]
    print ndx

    w = runData['warpedTracking']
    dt = np.diff(w[:,0])
    bMidNdx = w[0:-1,1]<tankLength*.5
    bSide1Ndx = w[0:-1,1]<tankLength*sideFrac
    bSide2Ndx = w[0:-1,1]>tankLength*(1-sideFrac)
    print 'Max dt=%f'%np.max(np.diff(w[:,0]))
    for switchNdx in ndx:
        startTime.append(state[switchNdx][0] - w[0,0])
        switchDuration.append(state[switchNdx+1][0]-state[switchNdx][0])
        bNdxWin = np.logical_and(w[:,0]>state[switchNdx][0], w[:,0]<state[switchNdx+1][0])
        bNdxWinDiff = np.logical_and(w[0:-1,0]>state[switchNdx][0], w[0:-1,0]<state[switchNdx+1][0])
        bNdx = np.logical_and(bNdxWinDiff, bMidNdx)
        timeOnSide1.append(sum(dt[bNdx]))
        distFromSide1.append(np.median(w[bNdxWin,1]))
        if refState.lower() == state[switchNdx][2].lower():
            bNdx = np.logical_and(bNdxWinDiff, bSide1Ndx)
            timeOnColor1.append(sum(dt[bNdx]))
            #timeOnColor1.append(timeOnSide1[-1])
            distFromColor1.append(np.median(w[bNdxWin,1]))
        elif refState.lower() == state[switchNdx][3].lower():
            bNdx = np.logical_and(bNdxWinDiff, bSide2Ndx)
            timeOnColor1.append(sum(dt[bNdx]))
            #timeOnColor1.append(switchDuration[-1] - timeOnSide1[-1])
            distFromColor1.append(tankLength - np.median(w[bNdxWin,1]))
        else:
            timeOnColor1.append(0)
            distFromColor1.append(0)
            print 'Warning requested color not present'
    return (timeOnColor1, timeOnSide1, switchDuration, distFromColor1, distFromSide1, startTime)

def getSidePreference_Multi(datasets, tankLength=48, cond=[3,4], refState='On',sideFrac=.5):
    tankLength = jsonData['tankSize_mm'][0]
    fracOnRef = []; distFromRef = []
    for n in range(len(datasets)):
        [rt,s1t,t,rd,s1d,t0] = getSidePreference(datasets[n], tankLength=tankLength, cond=cond, refState=refState, sideFrac=sideFrac)
        fracOnRef.append(np.array(rt)/np.array(t))
        distFromRef.append(rd)
    return (np.array(fracOnRef),np.array(distFromRef))

#todo plot velocity, and plot distance from shock edge...

def plotSidePreference(jsonData):
    [c, s, d] = getRunSidePreference(jsonData)
    c = np.array(c)
    d = np.array(d)
    ind = np.arange(len(c))
    width = 0.35

    ax = pyplot.gca()
    rects1 = ax.bar(ind, c/d, width, color='r')
    rects2 = ax.bar(ind+width, 1 -c/d, width, color='b')
    pyplot.ylim([0,1])
    pyplot.ylabel('Time on color (%)')

def getMedianVelMulti(datasets, tRange=None, stateRange=None, smoothWinLen=1, smoothWinType='flat'):
    """
    Return the median velocity in the time range.
    tRange: species time range relative to t_0. Negative values are relative to t_end.
    smoothWinLen: length of smoothing window.  smothing applied to position priod to computing vel.
    smoothWinType: flat, hanning, hamming, etc.
    """
    medVel = []
    for d in datasets:
        [vel,vt] = getVelRaw(d, tRange=tRange, stateRange=stateRange, 
                             smoothWinLen=smoothWinLen, smoothWinType=smoothWinType)
        medVel.append(np.median(vel))
    return np.array(medVel)

def getVelRaw(dataset, tRange=None, stateRange=None, smoothWinLen=1, smoothWinType='flat'):
    """
    Return array containing velocity at each frame.
    tRange: species time range relative to t_0. Negative values are relative to t_end.
    smoothWinLen: length of smoothing window.  smothing applied to position priod to computing vel.
    smoothWinType: flat, hanning, hamming, etc.
    """
    d = dataset
    w = d['warpedTracking']
    if smoothWinLen>1:
        if smoothWinType=='flat':
            smoothWin = np.ones(smoothWinLen,'d')
        else:
            smoothWin = eval('np.'+smoothWinType+'(smoothWinLen)')
        w_new = np.zeros([w.shape[0]-smoothWinLen+1, w.shape[1]])
        w_new[:,0] = np.convolve(smoothWin/smoothWin.sum(),w[:,0],mode='valid')
        w_new[:,1] = np.convolve(smoothWin/smoothWin.sum(),w[:,1],mode='valid')
        w_new[:,2] = np.convolve(smoothWin/smoothWin.sum(),w[:,2],mode='valid')
        w = w_new
    bNdxWin = np.ones(w.shape[0],dtype=bool)
    if tRange:
        if tRange[0]<0:
            tRange[0] = max(w[:,0]) - w[0,0] + tRange[0]
        if tRange[1]<0 or (tRange[1]==0 and tRange[1]<tRange[0]):    
            tRange[1] = max(w[:,0]) - w[0,0] + tRange[1]
        bNdxWin = np.logical_and(w[:,0]>tRange[0]+w[0,0], w[:,0]<tRange[1]+w[0,0])
    elif stateRange is not None:
        st,_,_,_ = state_to_time(dataset, stateRange[0])
        _,et,_,_ = state_to_time(dataset, stateRange[1])
        bNdxWin = np.logical_and(w[:,0]>st, w[:,0]<et)        
    vel = np.sqrt(pow(np.diff(w[bNdxWin,1]),2) + pow(np.diff(w[bNdxWin,2]),2)) / np.diff(w[bNdxWin,0])
    vt = w[bNdxWin[:-1],0]
    return vel, vt

def getOMRScoreStatsMulti(datasets, tRange=None,stateRange=None, timePoint = None): 
    stats = {}
    stats['omrResults'] = np.zeros(len(datasets),
                                   dtype = [('avgmaxdist',float),('avgtotdist',float),
                                            ('avgfractime',float),('avgratio',float),
                                            ('avgsub',float),('avgnorm',float)])
    stats['omrControl'] = np.zeros(len(datasets),
                                   dtype = [('avgmaxdist',float),('avgtotdist',float),
                                            ('avgfractime',float),('avgnorm',float)])
    stats['omrRandom'] = np.zeros(len(datasets),
                                  dtype = [('avgmaxdist',float),('avgtotdist',float),
                                           ('avgfractime',float)])                                                
    for i,d in enumerate(datasets):
        s = getOMRScoreStats(d, tRange,stateRange,timePoint)
        stats['omrResults'][i] = s['omrResults']
        stats['omrControl'][i] = s['omrControl']
        stats['omrRandom'][i] = s['omrRandom']
    return stats

def getOMRScoreStats(runData,tRange=None,stateRange=None, timePoint=None):
    t = runData['warpedTracking']
    results = getOMRinfo(runData,timePoint=timePoint)
    
    os=results['omrResults']['st']-t[0,0]
    ndx = range(len(os))

    if tRange is not None:
        ndx=np.nonzero(np.logical_and(os>tRange[0],os<tRange[1]))

    if stateRange is not None:
        st,_,_,_ = state_to_time(runData, stateRange[0])
        _,et,_,_ = state_to_time(runData, stateRange[1])
        st = st - t[0,0]
        et = et - t[0,0]
        ndx=np.nonzero(np.logical_and(os>st,os<et))        

    stats = {}
    stats['omrResults'] = np.array((results['omrResults']['maxdist'][ndx].mean(), 
                                    results['omrResults']['totdist'][ndx].mean(), 
                                    results['omrResults']['fractime'][ndx].mean(), 
                                    results['omrResults']['ratio'][ndx].mean(), 
                                    results['omrResults']['sub'][ndx].mean(), 
                                    results['omrResults']['norm'][ndx].mean()),
                                   dtype = [('avgmaxdist',float),('avgtotdist',float),
                                            ('avgfractime',float),('avgratio',float),
                                            ('avgsub',float),('avgnorm',float)])
    stats['omrControl'] = np.array((results['omrControl']['maxdist'][ndx].mean(), 
                                    results['omrControl']['totdist'][ndx].mean(), 
                                    results['omrControl']['fractime'][ndx].mean(),
                                    results['omrControl']['norm'][ndx].mean()),
                                   dtype = [('avgmaxdist',float),('avgtotdist',float),
                                            ('avgfractime',float),('avgnorm',float)])
    stats['omrRandom'] = np.array((results['omrRandom']['maxdist'][ndx].mean(), 
                                   results['omrRandom']['totdist'][ndx].mean(), 
                                   results['omrRandom']['fractime'][ndx].mean()),
                                  dtype = [('avgmaxdist',float),('avgtotdist',float),
                                           ('avgfractime',float)])                                                
    return stats  

#####################
# AVOIDANCE METHODS
####################

def getTrialDurations(jsonData):
    """
    For Avoidance Learning data:
    Get the Durations of every trial (for each trial time 
    until fish escaped or escape time expired)
    """
    trialTimes = []
    for trial in jsonData['trials']:
        trialTimes.append(trial['endT'] - trial['startT'])
    print trialTimes
    aTrialTimes = np.array(trialTimes)
    return aTrialTimes


def plotTrialDurations(jsonData):
    """
    For Avoidance learning data:
    """
    aTrialTimes = getTrialDurations(jsonData)
    pyplot.plot(aTrialTimes)

#Let S bet the trial startTime and E be the endTime.
#By default the function return the path from S-preTime to E+postTime.
#If bPostRelEnd is False, then path instead ends at S+postTime
#If bPreRelStart is False, then path instead starts at E-preTime
#If bFold, then flip trials that occurred on side 2.
def getTrialPath(jsonData, trialNum, preTime = 0, postTime = 0, bPreRelStart=True, bPostRelEnd=True, bFolded=False):
    #Get and clean up data
    if trialNum > len(jsonData['trials']):
        return np.array([])
    trial = jsonData['trials'][trialNum]
    tracking = getTracking(jsonData)

    #Extract the trial from the tracking info.
    s = trial['startT']-preTime if bPreRelStart else trial['endT']-preTime
    e = trial['endT']+postTime if bPostRelEnd else trial['startT']+postTime
    trialPath = tracking[np.logical_and(tracking[:,0] > s, tracking[:,0] < e),:].copy()

    #Fold if requested and return
    if bFolded:
        if trial['side'] == 1:
            trialPath[:,1] = 80 - trialPath[:,1]
    trialPath[:,0] = trialPath[:,0] - trial['startT']
    return trialPath

def getFoldedTrialPath(jsonData, trialNum, preTime = 0, postTime = 0, bPreRelStart=True, bPostRelEnd=True):
    trialPath = getTrialPath(jsonData, trialNum, preTime, postTime, bPreRelStart, bPostRelStart, bFolded=True)
    return trialPath

def plotTrialPath(jsonData, trialNum, preTime=0, postTime=0, bPreRelStart=True, bPostRelEnd=True, bFolded=False, bLabels=True):
    if type(trialNum) == type(int()):
        trialNum = [trialNum]
    for tn in trialNum:
        trial = jsonData['trials'][tn]
        trialPath = getTrialPath(jsonData, tn, preTime, postTime, bPreRelStart, bPostRelEnd, bFolded)
        if trial['bAvoidedShock']:
            pyplot.plot(trialPath[:,1],trialPath[:,2], 'g')
        else:
            pyplot.plot(trialPath[:,1],trialPath[:,2], 'r')
        #plot the LED
        if bFolded or trial['side']==0:
            pyplot.plot(0,35/2.0,marker='o',mec='r',mfc='r',ms=10)
            pyplot.plot(80,35/2.0,marker='o',mec='r',mfc='None',ms=10)
        else:
            pyplot.plot(0,35/2.0,marker='o',mec='r',mfc='None',ms=10)
            pyplot.plot(80,35/2.0,marker='o',mec='r',mfc='r',ms=10)
        #plot dot where LED turned on.
        ndxLED = np.flatnonzero(trialPath[:,0]>0)
        if len(ndxLED)>0:
            pyplot.plot(trialPath[ndxLED[0],1],trialPath[ndxLED[0],2],marker='o',mec='r',mfc='r',ms=5)
        #plot dot where Shock starts.
        ndxShock = np.flatnonzero(trialPath[:,0]>jsonData['parameters']['LEDTimeMS']/1000.0 - .1)
        if not trial['bAvoidedShock'] and len(ndxShock)>0:
            pyplot.plot(trialPath[ndxShock[0],1],trialPath[ndxShock[0],2],marker='o',mec='y',mfc='y',ms=5)
        pyplot.text(trialPath[-1,1],trialPath[-1,2], str(tn))
    pyplot.xlim([0,80])
    pyplot.ylim([0,35])
    pyplot.axvline(x=getEscapePosition(jsonData),color='k',ls='--')
    if bLabels:
        pyplot.xlabel('mm')
        pyplot.ylabel('mm')

def plotAllTrialPaths(jsonData, preTime=0, postTime=0, bPreRelStart=True, bPostRelEnd=True, bFolded=False):
    pyplot.figure(1,figsize=(12,9))
    pyplot.clf()
    pyplot.subplot(5,5,1)
    for nTrial in range(min(len(jsonData['trials']),25)):
        pyplot.subplot(5,5,nTrial+1)
        plotTrialPath(jsonData, nTrial, preTime, postTime, bPreRelStart, bPostRelEnd, bFolded, bLabels=False)

def plotTrialTimeByDistFromLED(jsonData, trialNum, preTime=0, postTime=0, bPreRelStart=True, bPostRelEnd=True, bLabels=True, yLim=(0,80), xLim=None):
    if type(trialNum) == type(int()):
        trialNum = [trialNum]
    for tn in trialNum:
        trial = jsonData['trials'][tn]
        trialPath = getTrialPath(jsonData, tn, preTime, postTime, bPreRelStart, bPostRelEnd, bFolded = True)
        if trial['bAvoidedShock']:
            pyplot.plot(trialPath[:,0],trialPath[:,1], 'g')
        else:
            pyplot.plot(trialPath[:,0],trialPath[:,1], 'r')
        if len(trialPath)>0:
            xTextPos = trialPath[-1,0]
            if xLim!=None:
                xTextPos = min(trialPath[-1,0], 0.15*xLim[0] + 0.85*xLim[1])
            pyplot.text(xTextPos,getEscapePosition(jsonData)+1, str(tn))
    if bLabels:
        pyplot.xlabel('time (s)')
        pyplot.ylabel('dist from LED side (mm)')
    pyplot.ylim(yLim)
    if xLim != None:
        pyplot.xlim(xLim)
    pyplot.axhline(y=getEscapePosition(jsonData),color='k',ls='--')
    pyplot.plot(0,0,marker='^',mec='r',mfc='r',ms=10)
    pyplot.plot(jsonData['parameters']['LEDTimeMS']/1000.0,0,marker='^',mec='y',mfc='y',ms=10)

def plotAllTrialTimeByDistFromLED(jsonData, preTime=0, postTime=0, bPreRelStart=True, bPostRelEnd=True, yLim=(0,80), xLim=None):
    pyplot.figure(1, figsize=(12,9))
    pyplot.clf()
    pyplot.subplot(5,5,1)
    for nTrial in range(min(len(jsonData['trials']),25)):
        pyplot.subplot(5,5,nTrial+1)
        plotTrialTimeByDistFromLED(jsonData, nTrial, preTime, postTime, bPreRelStart, bPostRelEnd, yLim=yLim, xLim=xLim, bLabels=False)

def getSlopeOfDistFromLED(jsonData, trialNum):
    if type(trialNum) == type(int()):
        trialNum = [trialNum]
    slope = []
    bAvoidedShock = []
    for tn in trialNum:
        trial = jsonData['trials'][tn]
        trialPath = getTrialPath(jsonData, tn, 0, min(trial['endT']-trial['startT'],jsonData['parameters']['LEDTimeMS']/1000.0), bPostRelEnd=False, bFolded = True)
        m, b, r, p, std_err = stats.linregress(trialPath[:,0],trialPath[:,1])
        #pdb.set_trace()
        slope.append(m)
        bAvoidedShock.append(trial['bAvoidedShock'])
    return slope, bAvoidedShock

def plotSlopeOfDistFromLEDAcrossTrials(jsonData):
    slope, bAvoidedShock = getSlopeOfDistFromLED(jsonData, range(len(jsonData['trials'])))
    #c = np.array(['r']*len(slope))
    #c[np.array(bAvoidedShock,dtype='bool')] = 'g'
    #pyplot.bar(range(len(slope)),slope,color=c)
    trials = np.array(range(len(slope)))
    slope = np.array(slope)
    bEsc = np.array(bAvoidedShock,dtype=bool)
    pyplot.plot(trials[np.logical_not(bEsc)],slope[np.logical_not(bEsc)],'ro')
    pyplot.plot(trials[bEsc],slope[bEsc],'go')
    m, b, r, p, std_err = stats.linregress(trials,slope)
    #robust fit
    resid = slope - trials*m+b
    nonOut = abs(resid)<2*np.std(resid)
    m, b, r, p, std_err = stats.linregress(trials[nonOut],slope[nonOut])
    pyplot.plot((0,len(slope)), (m*0+b,m*len(slope)+b), 'k--')
    pyplot.xlabel('trial#')
    pyplot.ylabel('linreg slope (mm/s)')
    pyplot.title('p=%f'% p)

#return velocity at each frame time
#if bXAxisVelocity then positive is away from LED
def getTrialInstantVelocity(jsonData, trialNum, preTime=0, postTime=0, bPreRelStart=True, bPostRelEnd=True, bXAxisVelocity=False):
    trialPath = getTrialPath(jsonData, trialNum, preTime, postTime, bPreRelStart, bPostRelEnd, bFolded = True)
    dt = np.diff(trialPath,1,0)
    if not bXAxisVelocity:
        trialVel = (dt[:,1]**2 + dt[:,2]**2)**0.5 / dt[:,0]
    else:
        trialVel = dt[:,1] / dt[:,0]
    trialTime = trialPath[1:,0]
    return trialVel, trialTime

def plotTrialInstantVelocity(jsonData, trialNum, preTime=0, postTime=0, bPreRelStart=True, bPostRelEnd=True, bXAxisVelocity=False):
    trial = jsonData['trials'][trialNum]
    (vel, time) = getTrialInstantVelocity(jsonData, trialNum, preTime, postTime, bPreRelStart, bPostRelEnd, bXAxisVelocity)
    pyplot.plot(time, vel)
    return vel, time

def plotAllTrialInstantVelocities(jsonData, preTime=0, postTime=0, bPreRelStart=True, bPostRelEnd=True, bXAxisVelocity=False):
    for nTrial in range(jsonData['parameters']['numtrials']):
        pyplot.subplot(4,3,nTrial+1)
        plotTrialInstantVelocity(jsonData, nTrial, preTime, postTime, bPreRelStart, bPostRelEnd, bXAxisVelocity)

#return average velocity in time bins relative to trial start or trial end
#if bins is length 1, then it represents the binsize, otherwise it should specify the bin edges.
#binCenterTime specified where one of the binEdges should fall.
def getTrialVelocity(jsonData, trialNum, preTime=0, postTime=0, bPreRelStart=True, bPostRelEnd=True, bXAxisVelocity=False, bins=1, binCenterTime=0):
    (vel, time) = getTrialInstantVelocity(jsonData, trialNum, preTime, postTime, bPreRelStart, bPostRelEnd, bXAxisVelocity)
    if len(bins) == 1:
        binEdges = np.hstack([np.arange(binCenterTime,time(0)-2*bins,-bins)[-1:0:-1],arange(binCenterTime,time(-1)+2*bins,bins)])
    else:
        binEdges = bins
    countsPerBin = np.histogram(time,binEdges)
    sumsPerBin = np.histogram(time,binEdges,weights=vel)
    binAvgVel = sumsPerBin / countsPerBin
    return binAvgVel, binEdges

def plotTrialVelocity(jsonData, trialNum, preTime=0, postTime=0, bPreRelStart=True, bPostRelEnd=True, bXAxisVelocity=False, bins=1, binCenterTime=0):
    (binAvgVel, binEdges) = getTrialVelocity(jsonData, trialNum, preTime, postTime, bPreRelStart, bPostRelEnd, bXAxisVelocity, bins, binCenterTime)
    pyplot.step(binEdges, np.concatenate([binAvgVel,[0]]), where='post')

#return times at which velocity crosses a threshold
#threshold in mm/s
def getTrialMovementTimes(jsonData, trialNum, preTime=0, postTime=0, bPreRelStart=True, bPostRelEnd=True, velThreshold = 10):
    (vel, time) = getTrialInstantVelocity(jsonData, trialNum, preTime, postTime, bPreRelStart, bPostRelEnd)
    return time[vel>velThreshold]

#return average number of movements per bin
def getTrialMovementsPerSecond(jsonData, trialNum, preTime=0, postTime=0, bPreRelStart=True, bPostRelEnd=True, velThreshold=10, bins=1, binCenterTime=0):
    moveTimes = getTrialMovementTimes(jsonData, trialNum, preTime, postTime, bPreRelStart, bPostRelEnd, velThreshold)
    if len(bins) == 1:
        binEdges = np.hstack([np.arange(binCenterTime,time(0)-2*bins,-bins)[-1:0:-1],arange(binCenterTime,time(-1)+2*bins,bins)])
    else:
        binEdges = bins
    binMovesPerSec = np.histogram(moveTimes,binEdges) / np.diff(binEdges)
    return binMovesPerSec, binEdges

def plotTrialMovementsPerSecond(jsonData, trialNum, preTime=0, postTime=0, bPreRelStart=True, bPostRelEnd=True, velThreshold=10, bins=1, binCenterTime=0):
    (binMovesPerSec, binEdges) = getTrialMovementsPerSecond(jsonData, trialNum, preTime, postTime, bPreRelStart, bPostRelEnd, velThreshold, bins, binCenterTime)
    pyplot.step(binEdges, np.concatenate([binMovesPerSec,[0]]), where='post')

#windows are pairs of times with 0 being startT.
#todo: generalize to n-windows using matrix or var args
def getDeltaXAcrossWindows(jsonData, trialNum, win_1, win_2):
    trialPath = getFoldedTrialPath(jsonData, trialNum, min((win_1[0],win_2[0])), max((win_1[1],win_2[1])), bPostRelEnd=False)
    win_1_startX = trialPath[nonzero(trialPath[:,0]>win_1[0])[0], 1]
    win_1_endX = trialPath[nonzero(trialPath[:,0]<win_1[1])[-1], 1]
    win_2_startX = trialPath[nonzero(trialPath[:,0]>win_2[0])[0], 1]
    win_2_endX = trialPath[nonzero(trialPath[:,0]<win_2[1])[-1], 1]
    return win_1_endX-win_1_startX, win_2_endX-win_2_startX

#windows are pairs of times with 0 being startT.
#todo: generalize to n-windows using matrix or var args
#todo: currently weights all velocities equally (independant of dt)
def getAvgVelocityInWindows(jsonData, trialNum, win_1, win_2):
    (vel, time) = getTrialInstantVelocity(jsonData, trialNum, min((win_1[0],win_2[0])), max((win_1[1],win_2[1])), bPostRelEnd=False)
    win_1_vel = np.mean(vel[np.logical_and(time>win_1[0],time<win_1[1])])
    win_2_vel = np.mean(vel[np.logical_and(time>win_2[0],time<win_2[1])])
    return win_1_vel, win_2_vel

def plotDeltaX(jsonData, win_1, win_2):
    win_1_dx = []
    win_2_dx = []
    for nTrial in range(jsonData['parameters']['numtrials']):
        (dx1, dx2) = getDeltaXAcrossWindows(jsonData, nTrial, win_1, win_2)
        win_1_dx.append(dx1)
        win_2_dx.append(dx2)
    pyplot.plot(range(jsonData['parameters']['numtrials']), win_1_dx, label='window1')
    pyplot.plot(range(jsonData['parameters']['numtrials']), win_2_dx, label='window2')

def plotAvgVel(jsonData, win_1, win_2):
    win_1_vel = []
    win_2_vel = []
    for nTrial in range(jsonData['parameters']['numtrials']):
        (vel1, vel2) = getAvgVelocityInWindows(jsonData, nTrial, win_1, win_2)
        win_1_vel.append(vel1)
        win_2_vel.append(vel2)
    pyplot.plot(range(jsonData['parameters']['numtrials']), win_1_vel, label='window1')
    pyplot.plot(range(jsonData['parameters']['numtrials']), win_2_vel, label='window2')

#TODO
#YES:  Create movie of particular path
#YES:  Create flipbook of TimeXDistToLEDSide

########## METHODS THAT AVERAGE ACROSS SUBJECTS
#TODO
#given a directory CONTROL directory or EXPERIMENTAL directory
#get all the fish.
#load the fish.

#STAT BY TRIAL NUMBER PLOTS:
#average TrialDuration averaged across fish for each trial.
#average DeltaX in two windows averaged across fish for each trial.
#average DeltaX/TrialLength
#average Velocity in two windows averaged across fish for each trial

#AVERAGE STAT BY TIME, ONE PLOT FOR EACH TRIAL
#average velocity histogram
#average X-velocity histogram
#average MovementsPerSec histogram for all fish on a particular trial.
