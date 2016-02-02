from Style import *
from Drawable import *
from Legend import *

from decimal import Decimal

import ROOT
import numpy
import random
import re
        
class HistogramStyle(LineStyle,FillStyle,MarkerStyle):
    def __init__(self):
        LineStyle.__init__(self)
        FillStyle.__init__(self)
        MarkerStyle.__init__(self)
        self.drawingOption=""
        
    @staticmethod
    def createFilled(fillColor=1,lineColor=-1,fillStyle=1001):
        s = HistogramStyle()
        if lineColor<0:
            s.lineColor=getDarkerColor(fillColor)
        else:
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
    def createLine(lineColor=-1):
        s = HistogramStyle()
        s.lineColor=lineColor
        s.lineStyle=1
        s.lineWidth=1
        
        s.fillColor=0
        s.fillStyle=0
        
        s.markerColor=0
        s.markerStyle=0
        s.markerSize=0
        
        s.drawingOption="HISTL"
        
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
        
class Binning(object):
    def __init__(self):
        pass

    def getArray(self):
        raise NotImplemented
        
    def getN(self):
        raise NotImplemented
        
    def __eq__(self,other):
        if not isinstance(other, Binning):
            return False
        if self.getN()!=other.getN():
            return False
        array1=self.getArray()
        array2=other.getArray()
        
        for i in range(self.getN()+1):
            if Decimal(array1[i])!=Decimal(array2[i]):
                return False
        return True
        
    def __ne__(self,other):
        return not (self==other)
        
class EquiBinning(Binning):
    def __init__(self,N,start,end):
        Binning.__init__(self)
        self.N=N
        self.start=start
        self.end=end
        
    def getArray(self):
        return numpy.linspace(self.start,self.end,num=self.N+1,endpoint=True)
        
    def getN(self):
        return self.N
        
    def __str__(self):
        return str((self.N,self.start,self.end))
        
        
class ArrayBinning(Binning):
    def __init__(self,array):
        Binning.__init__(self)
        self.array=array
        
    @staticmethod
    def fromRootHistogram(rootHist):
        binningArray=numpy.zeros(rootHist.GetNbinsX()+1)
        for i in range(rootHist.GetNbinsX()+1):
            binningArray[i]=rootHist.GetXaxis().GetBinLowEdge(i+1)
        return ArrayBinning(binningArray)
        
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
        
    def removeNegativeEntries(self):
        for ibin in range(self._rootHistogram.GetNbinsX()+2):
            self._rootHistogram.SetBinContent(ibin,max(0.0,self._rootHistogram.GetBinContent(ibin)))
            
        
    def setLegend(self,title,drawOptions,addtitle="",priority=0):
        self._legend=LegendEntry()
        self._legend.title=title
        self._legend.addtitle=addtitle
        self._legend.rootObj=self._rootHistogram
        self._legend.drawOptions=drawOptions
        self._legend.priority=priority
        
    def addHistogram(self,otherHistogram,scale=1.0):
        self._rootHistogram.Add(otherHistogram._rootHistogram,scale)
        
    def scale(self,scale=1.0):
        self._rootHistogram.Scale(scale)
        
    def rebin(self,n):
        self._rootHistogram.Rebin(n)
        self._binning=ArrayBinning.fromRootHistogram(self._rootHistogram)
        
    def divideHistogram(self,otherHistogram):
        self._rootHistogram.Divide(otherHistogram._rootHistogram)
        
    def getRootHistogram(self):
        return self._rootHistogram
        
    def getBinning(self):
        return self._binning
        
    @staticmethod
    def createFromRootHist(rootHist):
        h = Histogram1D()
        h._rootHistogram=rootHist.Clone("hist"+str(random.random()))
        h._rootHistogram.SetDirectory(0)
        h._binning=ArrayBinning.fromRootHistogram(rootHist)
        return h
        
    @staticmethod
    def createFromSearchInFile(filename,searchList):
        f = ROOT.TFile(filename,"r")
        
        allKeys=[]
        
        for k in f.GetListOfKeys():
            allKeys.append(k.GetName())
        matchedHists=[]
        for item in searchList:
            expr = re.compile(item.replace(".","\.").replace("*","[0-9a-zA-Z_\-]*"))
            for k in allKeys:
                if (expr.match(k)!=None):
                    matchedHists.append(f.Get(k))
        if len(matchedHists)==0:
            return None
        h=None
        for hist in matchedHists:
            if (h==None):
                h = Histogram1D.createFromRootHist(hist)
            else:
                h.getRootHistogram().Add(hist)
        f.Close()
        return h
        
    @staticmethod
    def createEmpty(binning):
        h = Histogram1D()
        h._rootHistogram=ROOT.TH1F("hist"+str(random.random()),"",binning.getN(),binning.getArray())
        h._rootHistogram.SetDirectory(0)
        h._rootHistogram.Sumw2()
        h._binning=binning
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
        

