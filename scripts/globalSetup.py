#Author: Benoit CASTETS
#Date: 19/05/2018
#Description: Libraries used for virtual robotic arm project.

#############################################################
#############################################################

#Libraries importation
#######################

#Available by default in Blender Python interpretor

#Blender Game Engine (available by default in Blender Python interpretor)
#Note: bge can only be imported if the script is placed in a python controllers of logic editor.
import bge
#math: basic matematical tols
import math
#math: basic matematical tols
import mathutils
#sys: tools to interact with base computer system
import sys

#External libraries imported from Conda Blender environment
#Add Conda environement library path
sys.path.append("/home/bcastets/anaconda3/envs/blenderVision/lib/python3.5/site-packages")

#Numpy: basic numerical array processing
import numpy as np
#scipy: dvanced numerical array processing
import scipy
#ndimage: tools for image processing
import scipy.ndimage as ndimage
#imageio: tools for image file read and write
import imageio



#Get Blender scene object to access objects of the scene
scene = bge.logic.getCurrentScene()
#Get the controler which is running this python script to access
#armature channels (pose bone)
ob=bge.logic.getCurrentController().owner
#Get armature target pose bone
#Note: There are 2 versions of the same bone.
#The raw "bone" data as it appear in edit mode
#The "pose bone" which is a the transformed version of the "bone" using for animation
tcpBone=ob.channels["Armature.target"]
