#############################################################
#Author: Benoit CASTETS
#Date:19/05/2018
#Contents: Definition of trajecotry object
#############################################################

#############################################################
#LIBRARIES
#############################################################

#External libraries
###################

#numpy: library for array manipulation and mathematics
from blenderLibImport import *

#Custom Libraries
#################
import geoTools as gt

#############################################################
#CLASS
#############################################################

class Trajectory():
    """Class to create a trajectory object.
    
    A trajectory is a succession of placements (location,orientation) with associated action.
    """
    def __init__(self,locationArray=None,angleArray=None,actionList=None,closed=False):
        """
        Parameters
        -----------
        locationArray:
            Numpy arrray with trajectory waypoint location verticaly stacked
        angleArray:
            Numpy array with trajectory waypoint orientation (eurler angle) verticaly stacked
        actionList:
            List of functions to execute on each waypoint. If no actions function is replaced by None
        closed:
            True if the trajectory is closed. False if the trajectory is open
        """
        #Locations of each placement of the trajectory in a numpy array
        self.locationArray=locationArray
        #Angle of each placement of the trajectory in a numpy array
        self.angleArray=angleArray
        #Action list
        if actionList is None:
            self.actionList=[]
        else:
            self.actionList=actionList
        #True if the trajectory is close
        self.closed=closed
    def __str__(self):
        """Convert objec to string. Used by print() function
        """
        if self.locationArray is None:
            return "Empty trajectory"
        else:
            nbrPlacement=self.locationArray.shape[0]
            i=0
            strOut=""
            while i<nbrPlacement:
                location=self.locationArray[i,:]
                locationStr=location.__str__()
                angle=self.angleArray[i,:]
                angleStr=angle.__str__()
                action=self.actionList[i]
                actionStr=str(type(action))
                if len(strOut)==0:
                    strOut="Loc: {} ||Agl: {}||Act: {}".format(locationStr,angleStr,actionStr)
                else:
                    strOut=strOut+"\n"+"Loc: {} ||Agl: {}||Act: {}".format(locationStr,angleStr,actionStr)
                i+=1
            return strOut
    def length(self):
        """Return the number of placements in the trajectory
        """
        nbrPlacements=0
        
        if (self.locationArray is None) or (self.locationArray.size==0):
            nbrPlacements=0
        else:
            nbrPlacements=self.locationArray.shape[0]
        
        return nbrPlacements
    
    def delPlacement(self,id=0):
        """Delete the placement at the input id
        
        Parameters
        ----------
        id:
            id of the placement to be deleted
        """
        if self.locationArray.shape[0]>1:
            self.locationArray=np.vstack((self.locationArray[:id,:],self.locationArray[id+1:,:]))
            self.angleArray=np.vstack((self.angleArray[:id,:],self.angleArray[id+1:,:]))
            self.actionList.pop(id)
        else:
            self.locationArray=None
            self.angleArray=None
            self.actionList=[]
        
    def addPlacement(self,location,angle,action=None):
        """Add a placement to the trajectory
        
        Parameters
        ----------
        location:
            np array vector with location
        angle:
            np vector with euler angle
        action:
            function to be executed at the placement
        """
        #Add location
        if self.locationArray is None:
            self.locationArray=location.reshape((1,3))
        else:
            self.locationArray=np.vstack((self.locationArray,location))
        
        #Add angle
        if self.angleArray is None:
            self.angleArray=angle.reshape((1,3))
            
        else:
            self.angleArray=np.vstack((self.angleArray,angle))
            
        #Add action
        self.actionList.append(action)
        
    def toLocationVectorArray(self):
        """Return all location vectors composing the trajectory
        verticaly stacked in a numpy array.
        
        Return
        ------
        locationVectorArray:
            vectors composing the trajectory verticaly stacked in a numpy array.
        """
        
        if self.locationArray is None:
            print("Empty trajectory")
            return None
        elif self.locationArray.shape[0]<2:
            #Less than 2 points: impossible to calculate a vector
            print("Only one point in trajectory. Cannot calculate vector.")
            return None
        else:
            locationVectorArray=self.locationArray[1:,:]-self.locationArray[:-1,:]
            
            #If closed add a vector to close the trajectory
            if self.closed:
                closeVector=self.locationArray[0,:]-self.locationArray[-1,:]
                locationVectorArray=np.vstack(locationVectorArray,closeVector)
            
            return locationVectorArray
    
    def distLocation(self,location):
        """Return the distance between point and trajectory and the closest point
        on the trajectory
        
        Parameter
        ---------
        location:
            location as numpy array np.array([x,y,z])
        
        Return
        ------
        minDist:
            minimum distance between point and trajectory
        closestPt:
            closest point on trajectory. np.array([x,y,z])
        vectorId:
            Id of the vector where the closest point if located.
        """
        minDist=None
        closestPt=None
        vectorId=None
        
        
        
        if self.locationArray is None:
            print("Empty trajectory")
            return None
        elif self.locationArray.shape[0]<2:
            minDist=np.linalg.norm(location-self.locationArray[0,:])
            closestPt=self.locationArray[0,:]
            vectorId=0
        else:
            #Get distance and closest point to each vector of the trajectory
            distArray=None
            pointArray=None
            n=0
            while n<(self.locationArray.shape[0]-1):
                
                ptA=self.locationArray[n,:]
                ptB=self.locationArray[n+1,:]
                ptC=location
                
                dist,ptCp=gt.distanceSegmentPoint(ptA,ptB,ptC)
                if distArray is None:
                    distArray=[dist]
                else:
                    distArray.append(dist)
                
                if pointArray is None:
                    pointArray=ptCp.reshape((1,3))
                else:
                    pointArray=np.vstack((pointArray,ptCp))
                
                n+=1
            #Additional segement in case of a closed trajectory
            if self.closed:
                ptA=self.locationArray[-1,:]
                ptB=self.locationArray[0,:]
                ptC=location
                
                dist,ptCp=gt.distanceSegmentPoint(ptA,ptB,ptC)
                
                if distArray is None:
                    disArray=[dist]
                else:
                    distArray.append(dist)
                
                if pointArray is None:
                    pointArray=ptCp.reshape((1,3))
                else:
                    pointArray=np.vstack((pointArray,ptCp))
            #Convert list ot numpy array
            distArray=np.array(distArray)
            
            closestId=np.argmin(distArray)
        
            minDist=distArray[closestId]
            closestPt=pointArray[closestId,:]
            vectorId=closestId
        return vectorId,minDist,closestPt
    
    def onTrajectory(self,location, tolerance):
        """Return True if the location is on trajectory within the input tolerance
        
        Parameters
        ----------
        location:
            location in a numpy array vector
        tolerance:
            tolerance of proximity
        """
        onTrajTest=False
        
        #Distance to trajectory is in an interval of tolerance
        vectorId,minDist,closestPt=distLocation(location)
        
        if minDist<tolerance:
            onTrajTest=True
        
        return ontrajTest            
        
    def concatenate(self,trajectory):
        """Concatenate trajectory
        
        Parameter
        ---------
        trajectory
            Trajectory object to be concatenate.
        """
        #Manage case of an empty trjectory
        if (self.locationArray is None) or (location.locationArray is None):
            pass
        elif (self.locationArray.shape[0]==0) or (location.locationArray.shape[0]==0):
            pass
        else:
            self.locationArray=np,vstack((self.locationArray,trajectory.locationArray))
            self.angleArray=np,vstack((self.angleArray,trajectory.angleArray))
            self.actionList.append(trajectory.actionList)
    
    def linearInterpolation(self,speed,vectorId):
        """Interpole trajectory to have one placement for each frame.
        Parameters
        ----------
        speed:
            distance traveled during one frame.
        segmentId:
            Id of the trajectory vector to be interpolated
        
        Return
        ------
        interTraj:
            Interpolated trajectory
        """
        
        
        #Get Vector start location
        startLocation=self.locationArray[vectorId,:]
        startAngle=self.angleArray[vectorId,:]
        #Get vector end location (warning: may not exist)
        endLocation=self.locationArray[vectorId+1,:]
        endAngle=self.angleArray[vectorId+1,:]
        #vector
        vector=endLocation-startLocation
        #Norm
        vectorNorm=np.linalg.norm(vector)
        
        #Number full steps
        nbrSteps=int((vectorNorm//speed)+1)
        
        #Interpolate location
        interX=np.linspace(startLocation[0],endLocation[0],nbrSteps)
        interY=np.linspace(startLocation[1],endLocation[1],nbrSteps)
        interZ=np.linspace(startLocation[2],endLocation[2],nbrSteps)
        
        interLocation=np.vstack((interX,interY,interZ))
        interLocation=np.transpose(interLocation)
        
        #Interpolation rotation
        interAlpha=np.linspace(startAngle[0],endAngle[0],nbrSteps)
        interBeta=np.linspace(startAngle[1],endAngle[1],nbrSteps)
        interGamma=np.linspace(startAngle[2],endAngle[2],nbrSteps)
        
        interAngle=np.vstack((interAlpha,interBeta,interGamma))
        interAngle=np.transpose(interAngle)
        
        #Interpolation action
        interAction=[None]*nbrSteps
        interAction[0]=self.actionList[vectorId]
        interAction[-1]=self.actionList[vectorId+1]
        
        #Output initialisation
        interTraj=Trajectory(interLocation,interAngle,interAction)
        return interTraj

#Test Trajectory class
if False:
    traj=Trajectory()
    
    #Test __str__
    print(traj)
    
    #Test addPlacement
    location=np.array([-2,-2,0])
    angle=np.array([0.1,0.2,0.3])
    action=None
    traj.addPlacement(location,angle,action)
    print(traj)
    
    #Test toLocationVectorArray
    locationVectorArray=traj.toLocationVectorArray()
    print(locationVectorArray)
    
    #Add a second point in trajectory
    location=np.array([2,2,0])
    angle=np.array([0.4,0.1,0.2])
    action=None
    traj.addPlacement(location,angle,action)
    print(traj)
    
    #Test toLocationVectorArray
    locationVectorArray=traj.toLocationVectorArray()
    print(locationVectorArray)
    
    #Test distance between a locatino and a trajectory
    location=np.array([2,-2,0])
    vectorID,minDist,closestPt=traj.distLocation(location)
    print(vectorID)
    print(minDist)
    print(closestPt)
    
    ###
    location=np.array([7,1,6])
    angle=np.array([0.4,0.1,0.2])
    action=None
    traj.addPlacement(location,angle,action)
    
    location=np.array([2,2,9])
    angle=np.array([0.4,0.1,0.2])
    action=None
    traj.addPlacement(location,angle,action)
    
    location=np.array([5,2,1])
    angle=np.array([0.4,0.1,0.2])
    action=None
    traj.addPlacement(location,angle,action)
    
    print(traj)
    print("interpolated trajectory")
    intertraj=traj.linearInterpolation(0.1,0)
    print(interTraj)

#Test interpolation trajectoire
if False:
    traj=Trajectory()
    print(traj)
    print(traj.actionList)
    
    location=np.array([0,0,0])
    angle=np.array([0.4,0.1,0.2])
    action=None
    traj.addPlacement(location,angle,action)
    
    location=np.array([10,0,0])
    angle=np.array([0.4,0.1,0.2])
    
    def action():
        pass
    traj.addPlacement(location,angle,action)
    
    print(traj)
    print(traj.actionList)
    traj2=Trajectory()
    print(traj2)
    print(traj2.actionList)
    
    interTraj=traj.linearInterpolation(1,0)
    print(interTraj)
    
    interTraj.delPlacement()
    print("Delete first element")
    print(interTraj)
    
    print(interTraj.length())
