from Drawable import *
from Position import *

import ROOT

class LegendEntry:
    def __init__(self,title="",addtitle="",rootObj="",drawOptions="L",priority=0):
        self.title=title
        self.addtitle=addtitle
        self.rootObj=rootObj
        self.drawOptions=drawOptions
        self.priority=priority
        
class Legend(Drawable):
    def __init__(self,position=Position.Legend.LEFT_SIDEWAYS):
        Drawable.__init__(self,hasAxis=False,allowLayout=True)
        self.textsize=10
        self._xmin=position.xmin
        self._xmax=position.xmax
        self._ymin=position.ymin
        self._ymax=position.ymax
        self._legendEntries=[]
        
    def addEntry(self,legendEntry):
        self._legendEntries.append(legendEntry)
        
    def draw(self,canvas,strech=Strech(),addOptions=""):
        self._ymin=self._ymax
        textHeight=0.7*ROOT.FontMetrics.GetTextWidth(43,self.textsize*strech.fontStrech,"Test")/canvas.heightPx
        for entry in self._legendEntries:
            self._ymin-=textHeight
            if entry.addtitle!="":
                self._ymin-=textHeight
        self._legend=ROOT.TLegend(self._xmin,self._ymin,self._xmax,self._ymax)
        self._legend.SetFillColor(0)
        self._legend.SetBorderSize(0)
        self._legend.SetTextFont(43)
        self._legend.SetTextAlign(12)
        self._legend.SetTextSize(self.textsize*strech.fontStrech)
        for entry in reversed(sorted(self._legendEntries,cmp=lambda x,y: x.priority-y.priority)):
            self._legend.AddEntry(entry.rootObj,entry.title,entry.drawOptions)
            if entry.addtitle!="":
                self._legend.AddEntry("",entry.addtitle,"")
        self._legend.Draw("Same")
        
    def getBoundingBox(self):
        return BoundingBox(
            BoundingBox.PERCENTS,
            self._xmin,
            self._ymin,
            self._xmax,
            self._ymax
        )
        
    def getLegendInfo(self):
        pass
        
