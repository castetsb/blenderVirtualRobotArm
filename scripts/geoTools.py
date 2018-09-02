#############################################################
#Author: Benoit CASTETS
#Date:19/05/2018
#Contents:Tools for 3D geometry
#############################################################

#############################################################
#LIBRARIES
#############################################################

#External libraries
#numpy: library for array manipulation and mathematics
from blenderLibImport import *

#############################################################
#FUNCTIONS
#############################################################

def distanceSegmentPoint(linePtA,linePtB,ptC):
    """Retrun the distance between the point and a segment defined by 2 points and the
    closest point.
    
    Paramaters
    ----------
    linePtA:
        Point defined as 1-D numpy array: np.array([x,y,z]) of extremity 1 of the segment.
    linePtB:
        Point defined as 1-D numpy array: np.array([x,y,z]) of extremity 2 of the segment.
    ptC:
        Point defined as 1-D numpy array: np.array([x,y,z]) for which we want to calculate
        the distance to the segment.
    
    Return
    ------
    distance:
        Distance between point C and segment AB
    closestPt:
        Closest point to C on AB segment. Point defined as 1-D numpy array: np.array([x,y,z]).
    """
    #Initialise Output
    distance=None
    closestPt=None
    
    #Define some vectors for futur calculation
    vectorAB=linePtB-linePtA
    vectorAC=ptC-linePtA
    
    #Define some distance
    distAB=np.linalg.norm(vectorAB)
    
    #Check if the projection of the point on the line is in the segment
    #Use scalaire product
    dotABAC= np.dot(vectorAB,vectorAC)
    #Cp for C projected
    distACp=dotABAC/distAB
    if distACp>=0 and distACp<=distAB:
        #If on the segment, evaluate the distance using vectorial product
        ptCp=linePtA+(vectorAB/distAB)*distACp
        distance=np.linalg.norm(ptC-ptCp)
        closestPt=ptCp
    else:
        #If not on the segment, evaluate the distance between each extremity
        #and return the lowest distance.
        distAC=np.linalg.norm(linePtA-ptC)
        distBC=np.linalg.norm(linePtB-ptC)
        if distAC>distBC:
            distance=distBC
            closestPt=linePtB
        else:
            distance=distAC
            closestPt=linePtA
    
    return distance, closestPt

#Test distanceSegmentPoint(linePtA,linePtB,ptC)
if False:
    linePtA=np.array([-2,0,0])
    linePtB=np.array([5,0,0,])
    ptC=np.array([0,7,0])
    distance,closestPt=distanceSegmentPoint(linePtA,linePtB,ptC)
    print(distance)
    print(closestPt)
    
    linePtA=np.array([-2,-2,0])
    linePtB=np.array([2,2,0,])
    ptC=np.array([3,-3,0])
    distance,closestPt=distanceSegmentPoint(linePtA,linePtB,ptC)
    print(distance)
    print(closestPt)


