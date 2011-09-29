import sys, os
import pygame, math, random, time, logging, datetime, json, cv
import numpy as np
import scipy.stats as stats
import matplotlib as mpl
import matplotlib.pyplot as pyplot
import matplotlib.patches
import tkFileDialog
import PerspectiveTransform 
import pdb

def loadData(fishDir):
	filelist = os.listdir(fishDir)
	filelist = filter(lambda x: x.endswith('json'), filelist)
	if len(filelist) != 1:
		return None 
	f = open(fishDir + os.sep + filelist[0])
	jsonData = json.load(f)
	f.close()
	
	#Clean up the tracking data and save it for other analysis.
	arena_mm = [(0,0),(0,35),(80,35),(80,0)] #arena in mm.
	jsonData['warpedTracking'] = getWarpedAndCleanedTracking(jsonData, warpTarget = arena_mm)
	
	return jsonData

def getWarpedAndCleanedTracking(jsonData, warpTarget):
	#Get and clean up data
	tracking = np.array(jsonData['tracking'])
	tracking = tracking[tracking[:,1]!=-1,:] #remove frames where tracking failed
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

def uiLoadData():
	f = tkFileDialog.askopenfile()
	jsonData = json.load(f)
	f.close()
	return jsonData

#Get the Durations of every trial (for each trial time until fish escaped or escape time expired)
def getTrialDurations(jsonData):
	trialTimes = []
	for trial in jsonData['trials']:
		trialTimes.append(trial['endT'] - trial['startT'])
	print trialTimes
	aTrialTimes = np.array(trialTimes)
	return aTrialTimes
	
def plotTrialDurations(jsonData):
	aTrialTimes = getTrialDurations(jsonData)
	pyplot.plot(aTrialTimes)
	
def getFrameRate(jsonData):
	fr = np.array(jsonData['tracking'])
	ufr = np.mean(fr[:,0])
	print "frame rate: ", ufr
	#Output number of failed track times
	totalFrames = fr.shape[0]
	missedFrames = np.sum(fr[:,1]==-1)
	print "fraction of frames where tracking failed: " , missedFrames, 'of', totalFrames, ':', float(missedFrames)/totalFrames

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
	trial = jsonData['trials'][trialNum]
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



