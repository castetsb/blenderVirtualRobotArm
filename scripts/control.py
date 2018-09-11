#############################################################
#Author: Benoit CASTETS
#Date:19/05/2018
#Contents: Script used to control blender robot arm model
#############################################################

#############################################################
#LIBRARIES
#############################################################

#External libraries
###################

#Internal libraries
###################
#bge: Blender game engine library
#Note: bge can only be imported if the script is placed in a python controllers of logic editor.
import bge
#System library used to manage library seearch path
import sys
#System library used for path manupulation
import os

#Custom libraries
#################
#Add blender virtual robot arm project scripts path
FILEPATH=bge.logic.expandPath("//")
CUSTOMLIBPATH=os.path.join(FILEPATH,"scripts")
print(CUSTOMLIBPATH)
#CUSTOMLIBPATH="/media/bcastets/data/racine/Loisir/IT/git/blenderVirtualRobotArm/scripts"
if CUSTOMLIBPATH not in sys.path:
    sys.path.append(CUSTOMLIBPATH)

#Custom Libraries
#################
#RobotArm: define robot arm object
from RobotArm import *
from Trajectory import *
from CamSensor import *

#############################################################
#Variables
#############################################################

#Get Blender scene object to access objects of the scene
scene = bge.logic.getCurrentScene()
#Get the controler which is running this python script to access
#armature channels (pose bone)
ob=bge.logic.getCurrentController().owner
#Get armature target pose bone
#Note: There are 2 versions of the same bone.
#The raw "bone" data as it appear in edit mode
#The "pose bone" which is a the transformed version of the "bone" using for animation
tcpPBone=ob.channels["Armature.target"]
####
toolCamera = scene.objects["Tool.camera"]
envCamera = scene.objects["Env.camera"]
####

#Create a Robot object
robot=RobotArm(ob,tcpPBone)
#Create a trajectory
traj=Trajectory()
location=np.array([0,5,6])
angle=np.array([0,3.14,0])
traj.addPlacement(location,angle,None)
location=np.array([5,0,6])
angle=np.array([0,3.14,0])
traj.addPlacement(location,angle,None)
location=np.array([0,-5,6])
angle=np.array([0,3.14,0])
traj.addPlacement(location,angle,None)
location=np.array([-5,0,6])
angle=np.array([0,3.14,0])
traj.addPlacement(location,angle,None)
traj.closed=True

#Load trajectory as robot routine trajectory
robot.routineTrajectory=traj

#Create a camera sensor
camSensor=CamSensor(toolCamera)

#vision check period
#vision check is perform every visionPeriod frame
visionPeriod=0 #Vision check every 30 frame

#############################################################
#Functions
#############################################################
def poseRefresh():
    """Fonction refreshing robot pose
    """
    global robot
    global camSensor
    global visionPeriod
    global traj

    objectNpLocation=None

    #Interruptions:
    if visionPeriod<1:
        pxLocation=camSensor.redDetect()
        if pxLocation is not None:
            objectNpLocation=camSensor.pixelWorkSpaceLocation(pxLocation)
            redTraj=Trajectory()
            location=np.array([0,5,6])
            angle=np.array([0,3.14,0])
            redTraj.addPlacement=(location,angle,None)
            robot.routineTrajectory=redTraj
        else:
            robot.routineTrajectory=traj
        visionPeriod=30
    else:
        visionPeriod-=1
    robot.refresh()

