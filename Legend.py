from Drawable import *

import ROOT

class LegendEntry:
    def __init__(self,title="",addtitle="",rootObj="",drawOptions="L",priority=0):
        self.title=title
        self.addtitle=addtitle
        self.rootObj=rootObj
        self.drawOptions=drawOptions
        self.priority=priority
        
class Legend(Drawable):
    def __init__(self,scale=1.0):
        Drawable.__init__(self,hasAxis=False,allowLayout=True)
        self.scale=scale
        self.textsize=11
        self._xmin=0.2
        self._xmax=0.45
        self._ymin=0.65
        self._ymax=0.9
        self._legendEntries=[]
        
    def addEntry(self,legendEntry):
        self._legendEntries.append(legendEntry)
        
    def draw(self,canvas,addOptions=""):
        self._legend=ROOT.TLegend(self._xmin,self._ymin,self._xmax,self._ymax)
        self._legend.SetFillColor(0)
        self._legend.SetBorderSize(0)
        self._legend.SetTextFont(43)
        self._legend.SetTextSize(self.textsize*self.scale)
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
        
