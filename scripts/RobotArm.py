#Faire herite de la classe pose bone        
#############################################################
#Author: Benoit CASTETS
#Date:19/05/2018
#Contents: Definition of robot arm object
#############################################################

#############################################################
#LIBRARIES
#############################################################

#External libraries
###################
#Numpy: basic numerical array processing
from blenderLibImport import *

#Internal libraries
###################

#Custom Libraries
#################
from Trajectory import *
import convertTools as cvTools

class RobotArm():
    """Define robotic arm object
    """
    def __init__(self,ctrlOwner,tcpPBone,toolPBone=None,speed=0.1):
        """Create a robotArm object.
        
        Parameters
        ----------
        tcpPBone:
            Pose bone used as inverse kinematic target
        speed:
            Robot translation speed in dist unit per frame
        """
        #Base referential
        self.refLocation=None
        self.refAngle=None
        
        #ControlerOwner (use to access armature pose bone)
        self.ctrlOwner=ctrlOwner
        
        #Bone where is attached the tool
        self.toolPBone=toolPBone
        
        #Tool center point pose bone
        self.tcpPBone=tcpPBone
        #print("Target location",tcpPBone.location)
        
        #Tools
        #Dictionnary of tools mounted ont he robot
        self.tools={}
        
        #Robotic arm base position in global referential
        self.restTcpPosition=tcpPBone.location
        #Robotic arm base orientation in global referential
        self.restTcpRotation=tcpPBone.joint_rotation
        
        #displacmeent speed (in dist unit /frame)
        self.speed=0.1
        
        #Routine trajectory
        self.routineTrajectory=Trajectory()
        #Non interpolated trajectory to be executed by the robot
        self.bufferTrajectory=Trajectory()
        #Interpolated trajectory for the on going routine trajectory vector or vector
        #If None the robot freeze
        self.bufferInterTrajectory=Trajectory()
        #Id of the interpolated vector
        self.bufferVectorId=-1
        #On trajectory flag
        self.onTrajectory=False
        #Progress on routine trajectory
        self.onRoutine=False
        
        #Dictionnary which can be used by skills algorithm
        self.customDic={}
        #Skills
        self.skillDic={}
    
    def _baseRefToTargetRef(self,location,angle):
        """Convert base ref placement to target ref placement
        """
        #Rotation matrix
        rotMat=np.array([[0,1,0],[0,0,1],[1,0,0]])
        translation=np.array([0,0,-15.5])
        locationTrans=location+translation
        
        targetRefLocation=np.dot(rotMat,locationTrans)
        
        targetRefAngle=np.dot(rotMat,np.transpose(angle))
        
        return targetRefLocation,targetRefAngle
    
    def _targetRefToBaseRef(self,location,angle):
        """Convert target ref placement to base ref placement
        """
        #Rotation matrix
        rotMat=np.array([[0,0,1],[1,0,0],[0,1,0]])
        translation=np.array([0,0,15.5])
        
        locationRot=np.dot(rotMat,location)
        baseRefLocation=locationRot+translation
        baseRefAngle=np.dot(rotMat,np.transpose(angle))
        
        return baseRefLocation, baseRefAngle
    
    def getTcpPlacement(self):
        """Return TCP placement in base referential
        """
        blenderLocation=self.tcpPBone.location
        blenderAngle=self.tcpPBone.joint_rotation
        
        location=cvTools.blenderToNp(blenderLocation)
        angle=cvTools.blenderToNp(blenderAngle)
        
        location,angle=self._targetRefToBaseRef(location,angle)
        
        return location,angle
    
    def setTcpPlacement(self,location,angle,action=None):
        """Place the arm tcp (tool center point) at the input
        position with the input orientation in global referential.
        
        Parameters
        ----------
        location:
            position in robotic arm base referencial (mathutils.Vector)
        angle:
            euler angle defining the orientation of the tcp (mathutils.Euler)
        action:
            action to be executed at the placement
        """
        location,angle=self._baseRefToTargetRef(location,angle)
        #Location
        self.tcpPBone.location=cvTools.npToBlenderVector(location)
        
        
        #Angle
        blenderAngle=cvTools.npToBlenderAngle(angle)
        #Switch to euler angle mode
        self.tcpPBone.joint_rotation=blenderAngle
        #Action
        if action is not None:
            action()
        
        #Refresh
        self.ctrlOwner.update()
    
    def tcpMove(self,translationVector,eulerAngle):
        """Move the arm tcp (tool center point) of the input
        translation vector and rotate of the input euler angle.
        
        Parameters
        ----------
        translationVector:
            Translation vector to translate the tcp (mathutils.Vector)
        eulerAngle:
            euler angle to rotate the tcp (mathutils.Euler)
        """
        
        #Position
        pBone.location=pBone.location+translationVector#Addition is working with mathutils.Vector
        
        #Orientation
        #Switch to euleur angle mode
        boneAlpha=pBone.joint_rotation.x
        boneBeta=pBone.joint_rotation.y
        boneGamma=pBone.joint_rotation.z
        
        alpha=eulerAngle.x
        beta=eulerAngle.y
        gamma=eulerAngle.z
        vector=mathutils.Vector((boneAlpha+alpha,boneBeta+beta,boneGama+gamma))
        
        pBone.joint_rotation=mathutils.Eurler(vector,"XYZ")
    
    def tcpGoto(self,posVector,eulerAngle):
        """travel from current position to input placement in a defined number of steps
        
        Parameters
        ----------
        posVector:
            position in robotic arm base referencial (mathutils.Vector)
        eulerAngle:
            euler angle defining the orientation of the tcp (mathutils.Euler)
        """
        pass
    
    def putOnTrajectory(self):
        """Load a trajectory in buffer to go to the closest point on routine
        trajectory.
        """
        if self.routineTrajectory.length()>0:
            
            #Find the closest point on trajectory
            
            tcpLocation,tcpAngle=self.getTcpPlacement()
            """
            print(type(tcpLocation))
            print(tcpLocation)
            print(type(tcpAngle))
            print(tcpAngle)
            """
            vectorId,minDist,closestPt=self.routineTrajectory.distLocation(tcpLocation)
            
            print("Travel to a point of routine trajectory on vector N {}".format(vectorId))
            """
            print("Closest point on trajectory: ",closestPt)
            print("Distance from trajectory: ",minDist)
            print("Closest vector ID :",vectorId)
            """
            angle=self.routineTrajectory.angleArray[vectorId]
            
            #Transition trajectory
            transTraj=Trajectory()
            transTraj.addPlacement(tcpLocation,tcpAngle,None)
            transTraj.addPlacement(closestPt,angle,None)
            print(transTraj.actionList)            #A verifier
            endLocation=self.routineTrajectory.locationArray[vectorId+1]
            endAngle=self.routineTrajectory.angleArray[vectorId+1]
            
            def endAction(rob=self,vectorId=vectorId):
                """Load routine trajectory in trajectory buffer
                """
                print("Tcp is now back on routine trajectory")
                rob.bufferTrajectory=rob.routineTrajectory
                rob.bufferVectorId=vectorId
            
            transTraj.addPlacement(endLocation,endAngle,endAction)
            
            self.bufferTrajectory=transTraj
            
            self.onTrajectory=True
            #vectorId is -1 because the robot is starting first vector of buffer trajectory
            self.bufferVectorId=-1
    
    def loadNextTrajectoryVector(self):
        """Load next trajectory segment to interpolated trajectory buffer
        """
        self.bufferVectorId+=1
        print("VectorId",self.bufferVectorId+1,"/",self.bufferTrajectory.length()-1)
        if self.bufferVectorId>=self.bufferTrajectory.length()-1:
            self.bufferVectorId+=1
            #If all trajectory vector have been travelled
            if self.bufferTrajectory.closed:
                print("Close routine trajectory")
                #The trajectory is closed
                #Transition trajectory
                loopTraj=Trajectory()
                
                tcpLocation,tcpAngle=self.getTcpPlacement()
                loopTraj.addPlacement(tcpLocation,tcpAngle,None)
                
                startLocation=self.bufferTrajectory.locationArray[0]
                startAngle=self.bufferTrajectory.angleArray[0]
                startAction=self.bufferTrajectory.actionList[0]
                loopTraj.addPlacement(startLocation,startAngle,startAction)
                
                #Interpolate transition trajectory
                interLoopTraj=loopTraj.linearInterpolation(self.speed,0)
                
                self.bufferInterTrajectory=interLoopTraj
                
                self.bufferVectorId=-1
            else:
                #Do nothing
                pass
        else:
            #Load next vector
            self.bufferInterTrajectory=self.bufferTrajectory.linearInterpolation(self.speed,self.bufferVectorId)
    def tcpPlacementFromBuffer(self):
        """Place the tcp to the first placement in interpolation
        trajectory buffer
        """
        if self.bufferInterTrajectory.length()>0:
            #Interpolated trajectory buffer not empty
            #Get first placement in buffer inter trajectory
            location=self.bufferInterTrajectory.locationArray[0,:]
            angle=self.bufferInterTrajectory.angleArray[0,:]
            action=self.bufferInterTrajectory.actionList[0]
            
            #Go to the first placement in buffer inter trajectory
            self.setTcpPlacement(location,angle,action)
            #Remove the first placement in buffer inter trajectory
            self.bufferInterTrajectory.delPlacement()
        else:
            #Load next trajectory vector in buffer interpolated trajectory
            print("Load next buffer trajectory vector")
            self.loadNextTrajectoryVector()
            if self.bufferTrajectory.length()>0:
                #If bufferInterTrajectory have been loaded
                self.tcpPlacementFromBuffer()
    
    def followRoutineTrajectory(self):
        """
        """
        
        if self.onTrajectory:
            #On trajectory
            #print("On trajectory. Continue on trajectory.")
            self.tcpPlacementFromBuffer()
        else:
            #Not on trajectory
            #print("Not on trajectory. Put back on trajectory.")
            
            self.putOnTrajectory()
    
    def refresh(self):
        """If the robot is not frozen and if it did not reach its final position,
        this function update robot position toward its final position.
        """
        self.followRoutineTrajectory()

#Test placement
if False:
    robot=RobotArm(ob,tcpPBone)
    baseRefLocation=np.array([0,5,0])
    baseRefAngle=np.array([0,3.14,0])
    #print(baseRefLocation,baseRefAngle)
    #location=np.array([5,-15.5,0])
    #angle=np.array([3.14,0,0])
    robot.setTcpPlacement(baseRefLocation,baseRefAngle,None)
    #WARNING: getTcpPlacement give the position of the current frame
    print(robot.getTcpPlacement())

if False:
    robot=RobotArm(ob,tcpPBone)
    #Prepare trajectory
    traj=Trajectory()
    #location=np.array([0,5,5])
    #angle=np.array([0,3.14,0])
    #action=None
    #traj.addPlacement(location,angle,action)
    location=np.array([0,5,0])
    angle=np.array([0,3.14,0])
    traj.addPlacement(location,angle,None)
    location=np.array([5,0,0])
    angle=np.array([0,3.14,0])
    traj.addPlacement(location,angle,None)
    location=np.array([0,-5,0])
    angle=np.array([0,3.14,0])
    traj.addPlacement(location,angle,None)
    location=np.array([-5,0,0])
    angle=np.array([0,3.14,0])
    traj.addPlacement(location,angle,None)
    traj.closed=True
    
    print("Routine trajectory")
    print(traj)
    print("End routine trajectory")
    
    #Load trajectory
    robot.routineTrajectory=traj
