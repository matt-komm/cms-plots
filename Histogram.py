from Style import *
        
class HistogramStyle(LineStyle,FillStyle,MarkerStyle):
    def __init__(self):
        LineStyle.__init__(self)
        FillStyle.__init__(self)
        MarkerStyle.__init__(self)
        
    @staticmethod
    def createFilled(fillColor=1,fillStyle=1001):
        s = HistogramStyle()
        s.lineColor=fillColor
        s.lineStyle=0
        s.lineWidth=0
        
        s.fillColor=fillColor
        s.fillStyle=fillStyle
        
        s.markerColor=1
        s.markerStyle=20
        s.markerSize=1.0
        
        return s
        
    @staticmethod
    def createMarkers(markerColor=1,markerStyle=20,markerSize=1.0):
        s = HistogramStyle()
        s.lineColor=markerColor
        s.lineStyle=0
        s.lineWidth=0
        
        s.fillColor=0
        s.fillStyle=0
        
        s.markerColor=markerColor
        s.markerStyle=markerStyle
        s.markerSize=markerSize
        
        return s

class Histogram:
    def __init__(self):
        self._style=HistogramStyle()
        
    def setStyle(self,style):
        self._style=style
        
    def projectFromTree(rootTree,varStr,cutStr):
        pass
