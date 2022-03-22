from java.io import File
from java.util import Arrays
from imagewrapper import ImageWrapper
from java.awt.image import BufferedImage
from javax.imageio import ImageIO, IIOException
from de.qfs.apps.qftest.shared.extensions.image import ImageRep
from de.qfs.apps.qftest.shared.exceptions import UnresolvedComponentIdException

global ImageComparator
class ImageComparator:
    """
    Compares pixel-by-pixel of two images with same resolution
    Ignores defined subregions during comparison
    """
    
    def LoadFile(self, fileName):
        """
        Load image with given fileName into image buffer
        Use javax.imageio.ImageIO class
        Note: iw.loadPng does not handle exceptions properly
        Save actual screen into given fileName in case it does not exist
        @param{str} fileName
        @retun{BufferedImage}
        """
        f = File(fileName)
        try:
            img = ImageIO.read(f)
            if type(img) != BufferedImage:
                raise Exception("ImageComparator: Could not load "
                                "image from file: "+fileName)
            return img
        except IIOException:
            self.iw.savePng(fileName, self.act_buf)
            return self.act_buf

    def GetScreen(self,ID):
        """
        Get screenshot of SUT component with given ID
        Use QF-Test ImageWrapper object
        @param{str} ID - QF-Test ID of given component
        @return{ImageRep}
        """
        try:
            img = self.iw.grabImage(rc.getComponent(ID))
            if type(img) != ImageRep:
                raise Exception("ImageComparator: Getting screenshot of SUT: "
                                "unknown type '"+type(img)+"' "
                                "of resulting object")
            return img
        except UnresolvedComponentIdException:
            raise Exception("ImageComparator: Getting screenshot of SUT: "
                            "unknown component "+ID)

    def HiddenRegion(self,x1=None,x2=None,y1=None,y2=None):
        """
        Register hidden region into the instance
        @param{int} x1,x2,y1,y2 - pixel boundaries of given region 
        """
        self.HiddenRegions.append([x1,x2,y1,y2])

    def ArraysAreEqual(self):
        """
        Compare RGB arrays of actual and expected images
        Use java.util.Arrays
        @return{bool} True in case arrays are equal, False otherwise
        """
        if self.act_arr.shape != self.exp_arr.shape:
            raise Exception("ImageComparator: shape of expected image "+
                            str(self.exp_arr.shape)+
                            " is not equal to shape of actual screen "+
                            str(self.act_arr.shape))
    
        if Arrays.deepEquals(self.act_arr.data, self.exp_arr.data):
            return True
        else:
            return False
    
    def GetArrayDiff(self):
        from java.util import HashSet
        hash_act = HashSet(Arrays.asList(self.act_arr.data))
        hash_act2 = HashSet(Arrays.asList(self.act_arr.data))
        print hash_act.size()
        
        hash_exp = HashSet(Arrays.asList(self.exp_arr.data))
        hash_exp2 = HashSet(Arrays.asList(self.exp_arr.data))
        print hash_exp.size()
        
        diff1 = hash_act.removeAll(hash_exp)
        print hash_act.size()
        
        diff2 = hash_exp2.removeAll(hash_act2)
        print hash_exp2.size()

    def LogError(self):
        """
        Calls rc.checkImage for actual and expected images
        In case images differ, the error is logged together
        with graphical comparison of both images into runlog
        """
        exp = self.iw.loadPng(self.FileName)
        rc.checkImage(self.act_buf,
                      exp,
                      "ImageComparator: Some differences were found!",
                      rc.ERROR,
                      1)
    
    def Run(self):
        # Load actual image
        self.act_buf = self.GetScreen(self.CompID)
        self.act_arr = RGBArray(self.act_buf)
        
        # Load expected image
        self.exp_buf = self.LoadFile(self.FileName)
        self.exp_arr = RGBArray(self.exp_buf)
        
        # Hide regions
        for reg in self.HiddenRegions:
            x1,x2,y1,y2 = reg
            if x1<0: x1=0
            if x2>self.act_arr.shape[0]: x2=self.act_arr.shape[0]
            if y1<0: y1=0
            if y2>self.act_arr.shape[1]: y2=self.act_arr.shape[1]
            self.exp_arr[x1:x2,y1:y2] = 0
            self.act_arr[x1:x2,y1:y2] = 0
        
        # Compare images
        if self.ArraysAreEqual():
            rc.logMessage("ImageComparator: no differences were found")
        else:
            self.LogError()
            
    def __init__(self):
        self.iw = ImageWrapper(rc)
        self.FileName = None
        self.CompID = None
        self.HiddenRegions = list()
