#############################################################
#Author: Benoit CASTETS
#Date:19/05/2018
#Contents:Tools to convert 3D geometry object format
#############################################################

#############################################################
#LIBRARIES
#############################################################

#mathutils: basic mathematical tools used by blender
import mathutils

#External libraries
#numpy: library for array manipulation and mathematics
from blenderLibImport import *

#############################################################
#FUNCTIONS
#############################################################

def blenderToNp(blenderVector):
    """Convert a blender vector in a numpy vector
    
    Parameter
    ---------
    blenderVector:
        blender vector like mathutils.Vector or mathutils.Euler
    
    Return
    ------
    npVector:
        Vector in numpy format.        
    """
    x=blenderVector.x
    y=blenderVector.y
    z=blenderVector.z
    
    npVector=np.array([x,y,z])
    
    return npVector

#Test
if False:
    blenderVector=mathutils.Vector((1,2,3))
    npVector=blenderToNp(blenderVector)
    print(type(npVector))
    print(npVector)

#############################################################

def npToBlenderVector(npVector):
    """Convert a numpy vector in a blender vector
    
    Parameter
    ---------
    npVector:
        numpy vector
    
    Return
    ------
    blenderVector:
        Vector in blender format. mathutils.Vector
    """
    blenderVector=mathutils.Vector(tuple(npVector))
    return blenderVector

#Test
if False:
    npVector=np.array([1,2,3])
    blenderVector=npToBlenderVector(npVector)
    print(blenderVector)

#############################################################

def npToBlenderAngle(npAngle):
    """Convert a numpy vector in a blender angle.
    
    Parameter
    ---------
    npAngle:
        numpy vector with euler angle values
    
    Return
    ------
    blenderAngle:
        Vector in blender format. mathutils.Vector
    """
    blenderAngle=mathutils.Euler(tuple(npAngle),"XYZ")
    return blenderAngle

#Test
if False:
    npAngle=np.array([1,2,3])
    blenderAngle=npToBlenderAngle(npAngle)
    print(blenderAngle)
