#############################################################
#Author: Benoit CASTETS
#Date:19/05/2018
#Contents: Module with some useful function image processing
#############################################################

#############################################################
#LIBRARIES
#############################################################

#External libraries
###################

#numpy: library for array manipulation and mathematics
import blenderLibImport

#Libraries used for testing
if False:
    import imageio
    from matplotlib import pyplot as plt
    import numpy as np


#############################################################
#FUNCTIONS
#############################################################


#value
def rgbToHsv(imgRgb):
	"""Return the HSV version of the RGB input image

	Parameters
	**********
	imgRgb:
		Numpy format rgb image
	
	Return
	******
	imgHsv:
		Numpy fomart hsv image
	"""
	v=np.min(img,2)
	satImg=imgRgb-np.dstack((v,v,v))
	#Saturation
	s=np.max(satImg,2)

	orVector=1
	ogVector=-0.5+1j*np.sqrt(3)/2
	obVector=-0.5-1j*np.sqrt(3)/3

	colorVector=orVector*satImg[:,:,0]+ogVector*satImg[:,:,1]+obVector*satImg[:,:,2]

	h=np.degrees(np.angle(colorVector))
	
	#Keep hue between 0 and 365
	h=(h%360+360)%360
	#Code hue between 0 and 182 to save data on 8 bits
	h=h/2
	h=h.astype(np.uint8)

	hsvImg=np.dstack((h,s,v))

	return hsvImg

#Test
if False:
    
    img=imageio.imread("diffuse.JPG")
    
    imgHsv=rgbToHsv(img)
    plt.subplot(1,3,1)
    plt.imshow(imgHsv[:,:,0])
    plt.subplot(1,3,2)
    plt.imshow(imgHsv[:,:,1])
    plt.subplot(1,3,3)
    plt.imshow(imgHsv[:,:,2])
    plt.show()
    