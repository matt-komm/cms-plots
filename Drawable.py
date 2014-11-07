class BoundingBox:
    COORDINATES,PERCENTS=range(2)
    def __init__(self,boxType,x1=0,y1=0,x2=0,y2=0):
        self.boxType=boxType
        self.xmin=min(x1,x2)
        self.xmax=max(x1,x2)
        self.ymin=min(y1,y2)
        self.ymax=max(y1,y2)
    
    
    def union(self,otherBB):
        self.xmin=min(self.xmin,otherBB.xmin)
        self.xmax=max(self.xmax,otherBB.xmax)
        self.ymin=min(self.ymin,otherBB.ymin)
        self.ymax=max(self.ymax,otherBB.ymax)
        
    def __str__(self):
        return "x=["+str(self.xmin)+";"+str(self.xmax)+"], y=["+str(self.ymin)+";"+str(self.ymax)+"]"
        

class Drawable:
    def __init__(self,hasAxis=True, allowLayout=False):
        self.hasAxis=hasAxis
        self.allowLayout=allowLayout
        
    def draw(self,addOptions=""):
        raise NotImplemented
        
    def getBoundingBox(self):
        raise NotImplemented
        
    def getLegendInfo(self):
        raise NotImplemented
