#############################################################
#Author: Benoit CASTETS
#Date:19/05/2018
#Contents: Definition of camera sensor object
#############################################################

#############################################################
#LIBRARIES
#############################################################

#External libraries
###################

#numpy: library for array manipulation and mathematics
#imageio: library to read and write image
import blenderLibImport

#Custom Libraries
#################
import geoTools as gt
import imgProcess as ipros

#############################################################
#CLASS
#############################################################

class CamSensor():
    """
    """
    def __init__(self,blenderCamera):
        """Create a camera sensor
        
        Parameters:
        ----------
        blenderCamera:
            Blender camera object
        """
        self.cam=blenderCamera
        self.width=None
        self.height=None
        self.image=None
    
    def redDetect(self):
        """Return True if red is detected by the camera with mass center location
        """
        pass
    def getImage(self):
        """Get camera image as numpy array
        """
        #https://blender.stackexchange.com/questions/88459/capture-video-from-cameras-in-blender-game-engine-for-artificial-intelligence?rq=1
        
        #https://blender.stackexchange.com/questions/88459/capture-video-from-cameras-in-blender-game-engine-for-artificial-intelligence?rq=1
        
        
        source = bge.texture.ImageRender(self.cam.scene,self.cam) 
        
        #Need to have a viewer port larger then 100x100
        #!! Need to check capsize order [width,height] or [height,width] 
        source.capsize=[self.width,self.height]

        imageArray = bge.texture.imageToArray(source, 'RGB') 

        image = np.array(imageArray.to_list())
        image=image.reshape(self.height,self.width,3)
        image=image.astype(np.uint8)
        
        #filePath="/media/bcastets/data/racine/Loisir/wordPress/articles/cobot/illustration/blender/render/gameImage.png"
        #scipy.misc.imsave(filePath,image)
        
        self.image=image
    def saveImage(self,filePath):
        """Take a picture with head camera and save it as a file
        """
        #print("Save head camera view in file")
        self.getImage()
        imageio.imwrite(filePath,self.image)
    
    def redDetect(self):
        """Return True if red is detected by the camera with mass center location
        
        Output
        ******
        detected:
            Ture is red cube detected False if not detected
        
        location:
            ndArray (n,p) with n,p being the coordinate of the position of the red
            cube from the center of the image
        """    
        
        detected=False
        direction=np.array([0,0])
        
        img=self.image
        #Convert to HSV
        imgHsv=ipros.rgbToHsv(img)

        #Detect red
        #reminder: hue is between 0 and 182
        redMask=(s>30)*np.logical_or((h<10),(h>172))
        
        
        #print("center max position")
        #print(np.argmax(np.sum(redMask,1)))
        #print(np.argmax(np.sum(redMask,0)))
        
        #print(np.sum(redMask))
        if np.sum(redMask)==0:
            detected=False
            direction=np.array([0,0])
        else:
            detected=True 
            massCenter=ndimage.measurements.center_of_mass(redMask*1)
            #print("mass center :",massCenter)
            direction=np.array([massCenter[0]-(self.height//2-1),massCenter[1]-(self.width//2-1)])
            direction=direction.astype(np.int)
        return detected,direction
    def pixelProjection(planPoint,planNormal)
        """Return the projection of a camera pixel on a plan
        """

if False:
    camSensor=CamSensor(toolCamera)
    filePath="/media/bcastets/data/racine/Loisir/wordPress/articles/cobot/illustration/blender/render/gameImage.png"
