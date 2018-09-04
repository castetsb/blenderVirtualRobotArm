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
    """This class define what is tool. A tool is a physical
    or non physical object which provide functionnalities to
    a robot.

    This class is under construction and may be used in
    a futur version.
    """
    def __init__(self,name,blenderModelPath=None):
        """Create a tool object wich can be fixed on a virtual
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
    def mountOn(self,flange):
        """Fix the tool on a robot

        Parameters:
        ***********
        flange:
            3D object on which is fied/parented the tool.
        """
        pass
