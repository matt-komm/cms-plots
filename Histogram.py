from Style import *
from Drawable import *
from Legend import *

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
        s.lineWidth=1
        
        s.fillColor=fillColor
        s.fillStyle=fillStyle
        
        s.markerColor=1
        s.markerStyle=0
        s.markerSize=0
        
        s.drawingOption="HISTF"
        
        return s
        
    @staticmethod
    def createMarkers(markerColor=1,markerStyle=20,markerSize=1.15):
        s = HistogramStyle()
        s.lineColor=markerColor
        s.lineStyle=1
        s.lineWidth=1
        
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
        self._legend=None
        
    def setStyle(self,style):
        self._style=style
        
    def getStyle(self):
        return self._style
        
    def setLegend(self,title,drawOptions,addtitle="",priority=0):
        self._legend=LegendEntry()
        self._legend.title=title
        self._legend.addtitle=addtitle
        self._legend.rootObj=self._rootHistogram
        self._legend.drawOptions=drawOptions
        self._legend.priority=priority
        
    def addHistogram(self,otherHistogram,scale=1.0):
        self._rootHistogram.Add(otherHistogram._rootHistogram,scale)
        
    def divideHistogram(self,otherHistogram):
        self._rootHistogram.Divide(otherHistogram._rootHistogram)
        
    def getRootHistogram(self):
        return self._rootHistogram
        
    def getBinning(self):
        return self._binning
        
    @staticmethod
    def createFromRootHist(rootHist):
        h = Histogram1D()
        h._rootHistogram=rootHist
        binningArray=numpy.zeros(h._rootHistogram.GetNbinsX()+1)
        for i in range(h._rootHistogram.GetNbinsX()+1):
            binningArray[i]=h._rootHistogram.GetXaxis().GetBinLowEdge(i)
        b._binning=ArrayBinning(binningArray)
        return h
        
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
        
    def draw(self,canvas,strech=Strech(),addOptions=""):
        self._style.applyStyle(self._rootHistogram)
        self._rootHistogram.Draw(self._style.drawingOption+addOptions)
        
    def getBoundingBox(self):
        return BoundingBox(
            BoundingBox.COORDINATES,
            self._rootHistogram.GetXaxis().GetXmin(),
            0.0,
            self._rootHistogram.GetXaxis().GetXmax(),
            self._rootHistogram.GetMaximum() 
        )
        
    def getLegendInfo(self):
        if self._legend!=None:
            return [self._legend]
        else:
            return []
        

