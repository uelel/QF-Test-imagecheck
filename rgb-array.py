from time import time
from java.awt import Color
from java.awt.image import BufferedImage
from de.qfs.apps.qftest.shared.extensions.image import ImageRep

global RGBArray
class RGBArray:
    """
    Custom implementation of array holding RGB data of image
    Basic init/get/set operations defined
    """
    
    def __init__(self,img):
        """
        Load given image buffer into flattened array
        @param{BufferedImage/ImageRep} img - input image
        """
        startTime = time()
        
        if type(img) == BufferedImage:
            self.width = img.getWidth()
            self.height = img.getHeight()
            self.data = img.getRGB(0,0,
                                   self.width,
                                   self.height,
                                   None,0,
                                   self.width)
                                   
        elif type(img) == ImageRep:
            self.width = img.getWidth()
            self.height = img.getHeight()
            self.data = img.getARGB()
            
        self.loadingTime = time() - startTime
       
    def Iter(self,ax,val):
        """
        Generator yielding partial indices for flattened 1D array
        corresponding to given indices of given axis in 2D array
        Note: Formulas for conversion of indices between 1D and 2D arrays:
              i = x + y*width
              x = i % width
              y = (i-x)/width
        @param{int} ax - axis; x=0, y=1
        @param{slice/int} val - indices in given axis
        @return{int} subindex; resulting index i = subindex(x)+subindex(y)
        """
        if type(val) == slice:
            if val.start == None: start = 0
            else: start = val.start
            if val.stop == None:
                if ax == 0: stop = self.width
                elif ax == 1: stop = self.height
            else: stop = val.stop
            for i in range(start,stop):
                if ax == 0:
                    if i < 0 or i > self.width:
                        raise Exception("x dimension "+str(i)+
                                        " out of range for width "+str(self.width))
                    yield i
                if ax == 1:
                    if i < 0 or i > self.height:
                        raise Exception("y dimension "+str(i)+
                                        " out of range for height "+str(self.height))
                    yield i*self.width
        else:
            if ax == 0:
                if val < 0 or val > self.width:
                    raise Exception("x dimension "+str(val)+
                                    " out of range for width "+str(self.width))
                yield val
            if ax == 1:
                if val < 0 or val > self.height:
                    raise Exception("y dimension "+str(val)+
                                    " out of range for height "+str(self.height))
                yield val*self.width
    
    def __getitem__(self, keys):
        """
        Get items from array
        @param{int/tuple} keys - can refer to both 1D/2D indices
        """
        if type(keys) == tuple:
            x,y = keys
            lst = list()
            for i in self.Iter(0,x):
                for j in self.Iter(1,y):
                    lst.append(self.data[i+j])
            return lst
        elif type(keys) == int:
            i = keys
            return self.data[i]   
            
    def __setitem__(self, keys, val):
        """
        Set array items
        @param{int/tuple} keys - can refer to both 1D/2D indices
        @param{int} val - setter value 
        """
        if type(keys) == tuple:
            x,y = keys
            for i in self.Iter(0,x):
                for j in self.Iter(1,y):
                    self.data[i+j] = val
        elif type(keys) == int:
            i = keys
            self.data[i] = val

    @property
    def length(self):
        """
        Get length of flattened 1D array
        """
        return len(self.data)

    @property
    def shape(self):
        """
        Get shape of original 2D array
        """
        return self.width, self.height
