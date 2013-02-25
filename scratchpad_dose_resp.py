import os
import CocaineAnalysis as ca
import matplotlib.pyplot as pyplot

pretestDir = '/home/vburns/data/2012-11-26'
posttestDir = '/home/vburns/data/2012-11-27'

#get all the fish directory in pretestDir and posttestDir
preFishDirs = os.listdir(pretestDir)
preFishDirs.sort()
postFishDirs = os.listdir(posttestDir)
postFishDirs.sort()

#match each directory in pre to a directory in post.
#assume directory order suffices (probably not always safe)

#load all the file names into a matrix (fish)
preJson = []
postJson = []
for nFish in range(len(preFishDirs)):
    p = os.path.join(pretestDir,preFishDirs[nFish])
    filelist = os.listdir(p)
    filelist = filter(lambda x: x.endswith('json'), filelist)
    filelist.sort()
    if not len(filelist) == 1: print('something is wrong')
    preJson.append(os.path.join(p,filelist[0]))

    p = os.path.join(posttestDir,postFishDirs[nFish])
    filelist = os.listdir(p)
    filelist = filter(lambda x: x.endswith('json'), filelist)
    filelist.sort()
    if not len(filelist) == 2: print('post somethin is wrong')
    postJson.append(os.path.join(p,filelist[1]))
jsonFileNames = [preJson,postJson]

#for each element of matrix load the data and extract % on red
#assumes that pre and post testing are always run #0 -- not safe.
allJsonData = [] 
for fileNames in jsonFileNames:
    temp = []
    for fileName in fileNames:
        d = ca.loadDataFromFile(fileName,0)
        print d['parameters']['Cond']
        temp.append(d)
    allJsonData.append(temp)


#plot fish positions
fndx = [8,9,10]
pyplot.figure(1,figsize=(12,9))
pyplot.clf()
n = 1
for f in fndx:
    pyplot.subplot(4,len(fndx),n)
    ca.plotFishPosition(allJsonData[0][f])
    pyplot.title(f)

    pyplot.subplot(4,len(fndx),n+1*len(fndx))
    ca.plotSidePreference(allJsonData[0][f])

    pyplot.subplot(4,len(fndx),n+2*len(fndx))
    ca.plotFishPosition(allJsonData[1][f])

    pyplot.subplot(4,len(fndx),n+3*len(fndx))
    ca.plotSidePreference(allJsonData[1][f])

    n+=1
pyplot.show()

#plot red time



