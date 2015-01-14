from Drawable import *

class Graph(Drawable):
    def __init__(self,xvalues,yvalues):
        Drawable.__init__(self,hasAxis=True, allowLayout=False)
        self._xmin,self._xmax,self._ymin,self._ymax=xmin,xmax,ymin,ymax
        
    def draw(self,canvas,strech=Strech(),addOptions=""):
        pass
        
    def getBoundingBox(self):
        return BoundingBox(
            BoundingBox.COORDINATES,
            self._xmin,
            self._ymin,
            self._xmax,
            self._ymax
        )
        
        
    def getLegendInfo(self):
        return []
