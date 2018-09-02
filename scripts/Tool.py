#############################################################
#Author: Benoit CASTETS
#Date:19/05/2018
#Contents: Definition of tool object
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
class Tool():
    """
    """
    def __init__(self,name,blenderModelPath=None):
        """Create a tool object wich can be fixed on a virutal
        robot arm.

        Parameters
        **********
        name:
            Name of the tool
        blenderModelPath:
            Path of the blender model representing the tool.
            None if the tool is only software.
        """
        self.name=name
        self.blenderModel=blenderModel
    def mountOn(self,robot):
        """Fix the tool on a robot
        """
        pass
