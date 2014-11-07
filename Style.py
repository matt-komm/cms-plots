class LineStyle:
    def __init__(self):
        self.lineColor=1
        self.lineStyle=1
        self.lineWidth=1
        
    def applyStyle(self,rootHistogram):
        rootHistogram.SetLineColor(self.lineColor)
        rootHistogram.SetLineStyle(self.lineStyle)
        rootHistogram.SetLineWidth(self.lineWidth)
        
class FillStyle:
    def __init__(self):
        self.fillColor=1
        self.fillStyle=1001
        
    def applyStyle(self,rootHistogram):
        rootHistogram.SetFillColor(self.fillColor)
        rootHistogram.SetFillStyle(self.fillStyle)
        
class MarkerStyle:
    def __init__(self):
        self.markerColor=1
        self.markerStyle=20
        self.markerSize=1.0
        
    def applyStyle(self,rootHistogram):
        rootHistogram.SetMarkerColor(self.markerColor)
        rootHistogram.SetMarkerStyle(self.markerStyle)
        rootHistogram.SetMarkerSize(self.markerSize)
