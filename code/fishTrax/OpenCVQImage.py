from PyQt4 import QtGui
import cv

class OpenCVQImage(QtGui.QImage):

    def __init__(self, opencvImg):
		depth, nChannels = opencvImg.depth, opencvImg.nChannels
		if depth == cv.IPL_DEPTH_8U and nChannels == 3:
			#image is assumed to be in BGR because that is cv standard.
			w, h = cv.GetSize(opencvImg)
			opencvRgbImg = cv.CreateImage((w, h), depth, nChannels)
			cv.CvtColor(opencvImg, opencvRgbImg, cv.CV_BGR2RGB)
			self._imgData = opencvRgbImg.tostring()
			super(OpenCVQImage, self).__init__(self._imgData, w, h, \
				QtGui.QImage.Format_RGB888)
		elif depth == cv.IPL_DEPTH_8U and nChannels == 1:
			w, h = cv.GetSize(opencvImg)
			opencvRgbImg = cv.CreateImage((w, h), depth, 3)
			cv.CvtColor(opencvImg, opencvRgbImg, cv.CV_GRAY2BGR)
			cv.CvtColor(opencvRgbImg, opencvRgbImg, cv.CV_BGR2RGB)
			self._imgData = opencvRgbImg.tostring()
			super(OpenCVQImage, self).__init__(self._imgData, w, h, \
				QtGui.QImage.Format_RGB888)
		else:
			raise ValueError("Convert CV to QImage: image type not handled.")  
