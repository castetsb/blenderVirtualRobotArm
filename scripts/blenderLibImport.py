#############################################################
#Author: Benoit CASTETS
#Date:19/05/2018
#Contents: Issue to import external libraries in Blender
#Python interpretor
#############################################################

#############################################################
#Notes
#############################################################

#Check Python version of Blender by using the folling commands
#in Blender python console

#import sys
#print(sys.version)

#Build an external python environment (ex:Conda) with same version
#as blender and install the libraries you want to use in Blender

#Check library path of external library by using the following
#commands in external python console

#Here is an example to get numpy library path

#import numpy
#print(numpy.__file__)

#Put external library path in the following property
EXTLIBPATH="/home/bcastets/anaconda3/envs/blenderVision/lib/python3.5/site-packages"

#############################################################
#LIBRARIES
#############################################################

#sys: tools to interact with base computer system
import sys

#Add external library path
if EXTLIBPATH not in sys.path:
    sys.path.append(EXTLIBPATH)

#Numpy: basic numerical array processing
import numpy as np

#scipy: dvanced numerical array processing
import scipy

#ndimage: tools for image processing
import scipy.ndimage as ndimage

#imageio: tools for image file read and write
import imageio
