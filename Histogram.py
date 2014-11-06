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
        
        s.drawingOption="HIST"
        
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
        
        s.drawingOption="P"
        
        return s
        
    def applyStyle(self,histogram):
        histogram.SetLineColor(self.lineColor)
        
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
        self.binning=None
        self.rootHistogram=None
        
    def setStyle(self,style):
        self._style=style
        
    @staticmethod
    def projectFromTree(rootTree,varStr,cutStr,binning):
        h = Histogram1D()
        h.rootHistogram=ROOT.TH1F("hist"+str(random.random()),"",binning.getN(),binning.getArray())
        h.binning=binning
        rootTree.Project(h.rootHistogram.GetName(),varStr,cutStr)
        return h
        
    def draw(self):
        self._style.applyStyle(self.rootHistogram)
        self.rootHistogram.Draw(self._style.drawingOption)
        
        

