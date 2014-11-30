import ROOT

colors=[]
def newColor(red,green,blue):
    newColor.colorindex+=1
    color=ROOT.TColor(newColor.colorindex,red,green,blue)
    colors.append(color)
    return color
    
newColor.colorindex=301

def getDarkerColor(color):
    darkerColor=newColor(color.GetRed()*0.6,color.GetGreen()*0.6,color.GetBlue()*0.6)
    return darkerColor.GetNumber()
    


class LineStyle:
    def __init__(self):
        self.lineColor=1
        self.lineStyle=1
        self.lineWidth=1
        
    def applyStyle(self,rootHistogram):
        if type(self.lineColor)==type(ROOT.TColor()):
            rootHistogram.SetLineColor(self.lineColor.GetNumber())
        else:
            rootHistogram.SetLineColor(self.lineColor)
        rootHistogram.SetLineStyle(self.lineStyle)
        rootHistogram.SetLineWidth(self.lineWidth)
        
class FillStyle:
    def __init__(self):
        self.fillColor=1
        self.fillStyle=1001
        
    def applyStyle(self,rootHistogram):
        if type(self.fillColor)==type(ROOT.TColor()):
            rootHistogram.SetFillColor(self.fillColor.GetNumber())
        else:
            rootHistogram.SetFillColor(self.fillColor)
        rootHistogram.SetFillStyle(self.fillStyle)
        
class MarkerStyle:
    def __init__(self):
        self.markerColor=1
        self.markerStyle=20
        self.markerSize=0.9
        
    def applyStyle(self,rootHistogram):
        if type(self.markerColor)==type(ROOT.TColor()):
            rootHistogram.SetMarkerColor(self.markerColor.GetNumber())
        else:
            rootHistogram.SetMarkerColor(self.markerColor)
        rootHistogram.SetMarkerStyle(self.markerStyle)
        rootHistogram.SetMarkerSize(self.markerSize)
