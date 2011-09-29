import sys, os
import pygame, math, random, time, serial, logging, datetime, json, cv
import numpy as np

#IMPORTANT NOTE cvImg are pointers and can be modifed even if passed to a function.
#IMPORTANT NOTE queryImage returns a pointer to the same memory every time it is called. ie. no allocation.

#TODO log time of each frame retrieval, and output frame rate at the end...
#TODO Trying using opencv to grab an image - cv.CaptureFromCam and cv.QueryImage ended up using the macbook camera
#TODO email julie about her camera setup.
#TODO Tranfer code into main program... and save arena info and fish position!!
#TODO Start by converting to grayscale and downsampling?
#TODO Current mixing up cvImages, cvMats... could just use NumPy arrays... all the opencv functions work on them.
#TODO make background image the average of several frames.
#TODO Lower threshold and add erosion, or add minimum area (m00)
#TODO create demo video showing fish tracking.
#TODO find the biggest blog so that speckel doesn't matter / check size of convex hull and erode if necessary?
#TODO track multiple fish
#TODO see if fish spends more time near or far from another fish - background on social behavior

#Currently fixed detection parameters
pgScale = 2;
minArea = 1000
maxArea = 15000
bMask = False

def waitForKeyPress():
    bKeyPress = False
    while not bKeyPress:
        event = pygame.event.poll()
        keyinput = pygame.key.get_pressed()
        if keyinput[pygame.K_ESCAPE]:
            raise SystemExit
        elif event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            bKeyPress = True
            
def cvImg2pgSurf(cvImg):
	cvrgb = cv.CreateMat(cvImg.height, cvImg.width, cv.CV_8UC3)
	cv.CvtColor(cvImg, cvrgb, cv.CV_BGR2RGB)
	return pygame.image.frombuffer(cvrgb.tostring(), cv.GetSize(cvrgb), "RGB")
	
def draw_cvImgInPyGame(cvImg):
    pgImg = cvImg2pgSurf(cvImg)
    screen = pygame.display.get_surface()
    pgImg = pygame.transform.scale(pgImg,(screen.get_width(),screen.get_height()))
    screen.blit(pgImg, pgImg.get_rect())
	
def subtractAndThreshold(img, baseImg, threshold, mask):
    imgM = cv.GetMat(img)
    baseImgM = cv.GetMat(baseImg)
    sub_cvImg = cv.CloneMat(imgM)
    cv.AbsDiff(img, baseImgM , sub_cvImg)
    cv.Threshold ( sub_cvImg , sub_cvImg , threshold , 255 , cv.CV_THRESH_BINARY )
    if bMask:
        cv.And( sub_cvImg, mask, sub_cvImg )
    return sub_cvImg
    
def getFirstMoments(cvImg):
    grayImg = cv.CreateImage((cvImg.width,cvImg.height), 8L, 1) #1channel vs 3
    cv.CvtColor(cvImg,grayImg,cv.CV_BGR2GRAY)
    moments = cv.Moments(cv.GetMat(grayImg));    
    if(moments.m00 > minArea and moments.m00 < maxArea):
        return (True, (moments.m10/moments.m00,moments.m01/moments.m00))
    else:
        return (False, (0,0))
   
def isOnSide1(point, line, side1Sign):
    side = (line[1][0] - line[0][0]) * (point[1] - line[0][1]) - (line[1][1] - line[0][1]) * (point[0] - line[0][0])
    return cmp(side,0)==side1Sign  
    
def processArenaCorners(arenaCorners):
    ac = np.array(arenaCorners)
    arenaDivideLine = [tuple(np.mean(ac[(0,3),:],axis = 0)),tuple(np.mean(ac[(1,2),:],axis = 0))]
    side1Sign = 1
    if not isOnSide1(arenaCorners[1], arenaDivideLine, side1Sign):
        side1Sign = -1
    return (arenaDivideLine, side1Sign)
    
def getArenaMask(cvImg, arenaCorners):        
    arenaCvMask = cv.CreateImage((cvImg.width,cvImg.height), cvImg.depth, cvImg.channels) 
    cv.SetZero(arenaCvMask)
    print arenaCorners
    cv.FillConvexPoly(arenaCvMask, arenaCorners, (255,)*cvImg.channels)
    return arenaCvMask
    
def getNextImage(cvCam):
    cvImg = cv.QueryFrame(cvCam)
    return (True, cvImg)
    #IF USING BUFFERIMAGES.cpp to write TIFFs to disk, then ...
    #Modify BUFFERIMAGES to use naming convention such that one of the following work:
    #simple way: each file is numbered with a larger number: get all filenames alphabetically, 
    #   check if the greatest number is greater than last image. 
    #save memory: finite number of buffer images named ib_img01_time...ib_img30_time.
    #   load all the filenames, choose the one with the newest time, check that time has changed.
    #if debugging:
    #    maintain current imgNum, if 30ms have passed return a new image, otherwise (false, NULL)
    #    fn = "%s%sib_%d.tiff" % (imgBuffDir, os.sep, nImg%1000)
    #    curr_cvImg = cv.LoadImage(fn)

#Create directory for experiment (or directory where debug images are stored):
imgBuffDir = raw_input('Enter directory [""="/Users/andalman/Documents/Stanford/AVTImageBuffer]:')
if imgBuffDir == '':
	imgBuffDir = '/Users/andalman/Documents/Stanford/AVTImageBuffer';
    
# SETUP THE CAMERA (output cvCam, imgBuffDir, scr_size, scr_w, scr_h)
# raw_input("Start the image capture software now. Press Enter to continue.")
# Get directory for files
# imgBuffDir = raw_input('Enter directory [""="/Users/andalman/Documents/Stanford/AVTImageBuffer]:')
# if imgBuffDir == '':
# 	imgBuffDir = '/Users/andalman/Documents/Stanford/AVTImageBuffer';
# bCamera = False
# TODO write loop with pygame rather than raw_input
# while not bCamera:
#     camNdx = raw_input('Enter the opencv camera index [0]:')
#     if camNdx == 'q':
#         raise SystemExit
#     try:
#         cvCam = cv.CaptureFromCAM(int(camNdx))
#         (bNewImage, cvImg) = getNextImage(cvCam)
#         scr_size = scr_w, scr_h = cvImg.width/pgScale, cvImg.height/pgScale
#         screen = pygame.display.set_mode(scr_size)
#         draw_cvImgInPyGame(cvImg)
#         pygame.display.flip()
#         resp = raw_input('Was the correct camera loaded (y,n)?')
#         if resp.lower()[0] == 'y':
#             bCamera = True
#     except:
#         print "The camera failed to load try again, or press q to quit."

#INIT PYGAME (handy for user interaction especially with PGU module; could also learn pyqt or wxPython or Tkinker
pygame.quit()
pygame.init()

# SETUP THE CAMERA (output cvCam, imgBuffDir, scr_size, scr_w, scr_h)
bCamera = False
scr_size = scr_w, scr_h = 640, 480
screen = pygame.display.set_mode(scr_size)
pygame.display.set_caption("Press cv camera number [0,1..]. Press 'a' for any. Press 'y' if the camera looks correct.")
while not bCamera:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        raise SystemExit
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            raise SystemExit
        elif event.key == pygame.K_y:
            bCamera = True
        else:
            try:
                print event
                print event.unicode
                if event.unicode == 'a':
                    camNdx = -1
                else:
                    camNdx = int(event.unicode)
                print camNdx
                cvCam = cv.CaptureFromCAM(int(camNdx))
                (bNewImage, cvImg) = getNextImage(cvCam)
                scr_size = scr_w, scr_h = cvImg.width/pgScale, cvImg.height/pgScale
                screen = pygame.display.set_mode(scr_size)
                draw_cvImgInPyGame(cvImg)
                pygame.display.flip()     
            except:
                print "Cam load failed."

#GET A BACKGROUND IMAGE FOR SUBTRACTION (output: bcvImg)
#fn = imgBuffDir + os.sep + 'ib_base.tiff'
bLive = True
bBaseSelected = False
pygame.display.set_caption('Press p to pause/play. Press return when case is aligned:')
while not bBaseSelected:
    if bLive: 
        (bNewImage, cvImg) = getNextImage(cvCam)
        draw_cvImgInPyGame(cvImg)
        pygame.display.flip()
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        raise SystemExit
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            bBaseSelected = True
        elif event.key == pygame.K_ESCAPE:
            raise SystemExit
        elif event.key == pygame.K_p:
            bLive = not bLive
bcvImg = cv.CloneImage(cvImg)

#ASK USER TO SPECIFY LOCATION OF THE ARENA (output: arenaCorners, arenaDivideLine, side1Sign, arenaCVMask)
#TODO: Allow more complex polygons
pygame.display.set_caption('Carefully click on 4 inside corners of the arena. Start two corners on side 1, and go clockwise.')
nNumClicks = 0
bCancel = False
arenaCorners = [];
while nNumClicks<4 and not bCancel:
    event = pygame.event.poll()
    keyinput = pygame.key.get_pressed()
    # exit on corner 'x' click or escape key press
    if keyinput[pygame.K_ESCAPE]:
        raise SystemExit
    elif event.type == pygame.QUIT:
        raise SystemExit
    elif event.type == pygame.MOUSEBUTTONDOWN:
        arenaCorners.append((event.pos[0]*pgScale, event.pos[1]*pgScale))
        nNumClicks = nNumClicks+1;
        pygame.draw.circle(screen, (0,0,0), event.pos, 5, 2)
        pygame.display.flip()
(arenaDivideLine, side1Sign) = processArenaCorners(arenaCorners)
arenaCvMask = getArenaMask(bcvImg, arenaCorners)

#ASK USER TO SET THE DIFFERENCE THRESHOLD (output: nThreshold)
bThresholdSet = False
nThreshold = 50
view = 0
formatCap = 'set threshold with up/down. press v to change view. return to finish. thres=%d' 
pygame.display.set_caption( formatCap % nThreshold)
while not bThresholdSet:
    #Handle input
    event = pygame.event.poll()
    keyinput = pygame.key.get_pressed()
    if keyinput[pygame.K_ESCAPE]:
        raise SystemExit
    elif event.type == pygame.QUIT:
        raise SystemExit
    elif keyinput[pygame.K_RETURN]:
        bThresholdSet = True
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            nThreshold = nThreshold + 1
            pygame.display.set_caption(formatCap % nThreshold)
        elif event.key == pygame.K_DOWN:
            nThreshold = nThreshold - 1
            pygame.display.set_caption(formatCap % nThreshold)
        elif event.key == pygame.K_v:
            view = (view + 1) % 4
            
    #DISPLAY BACKGRND SUBTRACTED THRESHOLDED IMAGE
    (bNewImage, curr_cvImg) = getNextImage(cvCam)
    if bNewImage: 
        #background subtract and find center of mass
        diff_cvImg = subtractAndThreshold(curr_cvImg, bcvImg, nThreshold, arenaCvMask)
        (bSucc, centerOfMass) = getFirstMoments(diff_cvImg)  
        #choose fish color based on side of cage
        fishColor = (0,255,0)
        if not isOnSide1(centerOfMass,arenaDivideLine, side1Sign):
            fishColor = (255,0,0)
        #draw the current view
        if(view == 0):
            draw_cvImgInPyGame(diff_cvImg)
        elif(view == 1):
            draw_cvImgInPyGame(curr_cvImg)
            pygame.draw.circle(screen, fishColor, map(lambda x:x/pgScale,centerOfMass), 3, 2)
        elif(view == 2):
            cv.And(curr_cvImg, arenaCvMask, curr_cvImg)
            cv.Line(curr_cvImg, arenaDivideLine[0], arenaDivideLine[1], cv.CV_RGB(0,0,255), thickness=1, lineType=8, shift=0)
            draw_cvImgInPyGame(curr_cvImg)
            pygame.draw.circle(screen, fishColor, map(lambda x:x/pgScale,centerOfMass), 3, 2)  
        elif(view == 3):
            draw_cvImgInPyGame(bcvImg)
        pygame.display.flip()   


