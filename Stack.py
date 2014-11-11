from Drawable import *
from Histogram import *

import ROOT

class Stack(Drawable):
    def __init__(self):
        Drawable.__init__(self,hasAxis=True)
        self._rootStack = ROOT.THStack()
        
        self._histograms=[]
        
    def addHistogram(self,histogram):
        self._histograms.append(histogram)
        histogram.getStyle().applyStyle(histogram.getRootHistogram())
        self._rootStack.Add(histogram.getRootHistogram(),histogram.getStyle().drawingOption)
        
    def draw(self,canvas,strech=Strech(),addOptions=""):
        self._rootStack.Draw(addOptions)
        
    def getSum(self):
        hist = Histogram1D.createEmpty(self._histograms[0].getBinning())
        for i,subhist in enumerate(self._histograms):
            hist.addHistogram(subhist)
        return hist
        
    def getBoundingBox(self):
        return BoundingBox(
            BoundingBox.COORDINATES,
            self._rootStack.GetXaxis().GetXmin(),
            0.0,
            self._rootStack.GetXaxis().GetXmax(),
            self._rootStack.GetMaximum() 
        )
        
    def getLegendInfo(self):
        legendInfo=[]
        for histogram in self._histograms:
            legendInfo.extend(histogram.getLegendInfo())
        return legendInfo
