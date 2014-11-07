from Style import *
from Task import *
from Drawable import *

import ROOT
import numpy
import random
        
class HistogramStyle(LineStyle,FillStyle,MarkerStyle):
    def __init__(self):
        LineStyle.__init__(self)
        FillStyle.__init__(self)
        MarkerStyle.__init__(self)
        self.drawingOption=""
        
    @staticmethod
    def createFilled(fillColor=1,lineColor=1,fillStyle=1001):
        s = HistogramStyle()
        s.lineColor=lineColor
        s.lineStyle=1
        s.lineWidth=2
        
        s.fillColor=fillColor
        s.fillStyle=fillStyle
        
        s.markerColor=1
        s.markerStyle=20
        s.markerSize=1.0
        
        s.drawingOption="HISTF"
        
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
        
        s.drawingOption="PEX0"
        
        return s
        
    def applyStyle(self,rootHistogram):
        LineStyle.applyStyle(self,rootHistogram)
        FillStyle.applyStyle(self,rootHistogram)
        MarkerStyle.applyStyle(self,rootHistogram)
        
class Binning:
    def getArray(self):
        raise NotImplemented
        
    def getN(self):
        raise NotImplemented
        
class EquiBinning(Binning):
    def __init__(self,N,start,end):
        self.N=N
        self.start=start
        self.end=end
        
    def getArray(self):
        return numpy.linspace(self.start,self.end,num=self.N+1,endpoint=True)
        
    def getN(self):
        return self.N
        
class ArrayBinning:
    def __init__(self,array):
        self.array=array
        
    def getArray(self):
        return self.array
        
    def getN(self):
        return len(self.array)-1
        
        

class Histogram1D(Drawable):
    def __init__(self):
        Drawable.__init__(self,hasAxis=True)
        self._style=HistogramStyle()
        self._binning=None
        self._rootHistogram=None
        
    def setStyle(self,style):
        self._style=style
        
    def getStyle(self):
        return self._style
        
    def addHistogram(self,otherHistogram,scale=1.0):
        self._rootHistogram.Add(otherHistogram._rootHistogram,scale)
        
    def getRootHistogram(self):
        return self._rootHistogram
        
    @staticmethod
    def createEmpty(binning):
        h = Histogram1D()
        h._rootHistogram=ROOT.TH1F("hist"+str(random.random()),"",binning.getN(),binning.getArray())
        h._rootHistogram.Sumw2()
        h._binning=binning
        return h
        
    @staticmethod
    def projectFromTree(rootTree,varStr,cutStr,binning):
        h = Histogram1D()
        
        h._rootHistogram=ROOT.TH1F("hist"+str(random.random()),"",binning.getN(),binning.getArray())
        h._rootHistogram.Sumw2()
        h._binning=binning
        rootTree.Project(h._rootHistogram.GetName(),varStr,cutStr)
        return h
        
    def draw(self,addOptions=""):
        self._style.applyStyle(self._rootHistogram)
        self._rootHistogram.Draw(self._style.drawingOption+addOptions)
        
    def getBoundingBox(self):
        return BoundingBox(
            BoundingBox.COORDINATES,
            self._rootHistogram.GetXaxis().GetXmin(),
            self._rootHistogram.GetMinimum(),
            self._rootHistogram.GetXaxis().GetXmax(),
            self._rootHistogram.GetMaximum() 
        )
        
    def getLegendInfo(self):
        return None
        
        

