import cv
import numpy as np

# returns M such that warp_point(x,y,w)' = M * orig_point(x,y,1)'
def getWarpMatrix(corners, target):
    mat = np.zeros((3,3))
    cv.GetPerspectiveTransform(corners, target, cv.fromarray(mat))
    return mat
    
# points: nparray where x is column 0, y in column 1
def warpPoints(points, warpMat):
	#convert to homogeneous coordinates
	points = np.hstack([points,np.ones((points.shape[0],1))])
	#warp
	warpP = np.dot(warpMat,points.T).T
	#convert back to cartesian
	#warpP = np.dot(np.diag(1/warpP[:,2]),warpP[:,0:2])
	#A= scipy.sparse.dia_matrix(([1,2,3,4],0),shape=(4,4))
	warpP = (warpP[:,0:2].T * 1/warpP[:,2]).T
	return warpP
	
def warpImage(image, corners, target):
    mat = cv.CreateMat(3, 3, cv.CV_32F)
    cv.GetPerspectiveTransform(corners, target, cv.fromarray(mat))
    out = cv.CreateMat(height, width, cv.CV_8UC3)
    cv.WarpPerspective(image, out, mat, cv.CV_INTER_CUBIC)
    return out

if __name__ == '__main__':
    width, height = 400, 250
    corners = [(171,72),(331,93),(333,188),(177,210)]
    target = [(0,0),(width,0),(width,height),(0,height)]
    image = cv.LoadImageM('fries.jpg')
    out = warpImage(image, corners, target)
    cv.SaveImage('fries_warped.jpg', out)
