from Drawable import *

class Position:
    class CMSText:
        LEFT_SIDEWAYS=BoundingBox(BoundingBox.PERCENTS,0.19,0.86,0.53,0.86)
        RIGHT_SIDEWAYS=BoundingBox(BoundingBox.PERCENTS,0.64,0.86,0.94,0.86)
        
        LEFT_STACKED=BoundingBox(BoundingBox.PERCENTS,0.19,0.78,0.53,0.88)
        RIGHT_STACKED=BoundingBox(BoundingBox.PERCENTS,0.64,0.78,0.94,0.88)
        
    class Legend:
        LEFT_SIDEWAYS=BoundingBox(BoundingBox.PERCENTS,0.19,0.62,0.45,0.84)
        RIGHT_SIDEWAYS=BoundingBox(BoundingBox.PERCENTS,0.64,0.62,0.94,0.84)
        
        LEFT_STACKED=BoundingBox(BoundingBox.PERCENTS,0.19,0.56,0.45,0.78)
        RIGHT_STACKED=BoundingBox(BoundingBox.PERCENTS,0.64,0.56,0.94,0.78)
        
        OUTSIDE=BoundingBox(BoundingBox.PERCENTS,0.81,0.35,0.99,0.9)
        
    class Lumi:
        RIGHT=BoundingBox(BoundingBox.PERCENTS,0.6,0.995,0.965,0.995)
        
        OUTSIDE=BoundingBox(BoundingBox.PERCENTS,0.5,0.995,0.8,0.995)
        
    class Canvas:
        FILLED=BoundingBox(BoundingBox.PERCENTS,0.16,0.14,1-0.055,1-0.065)
        OUTSIDE=BoundingBox(BoundingBox.PERCENTS,0.16,0.14,1-0.2,1-0.065)
        
class GlobalPosition:
    def __init__(self):
        self.cmstext=Position.CMSText.RIGHT_STACKED
        self.legend=Position.Legend.RIGHT_STACKED
        self.lumi=Position.Lumi.RIGHT
        self.canvas=Position.Canvas.FILLED
        
    def makeRight(self):
        self.cmstext=Position.CMSText.RIGHT_STACKED
        self.legend=Position.Legend.RIGHT_STACKED
        self.lumi=Position.Lumi.RIGHT
        self.canvas=Position.Canvas.FILLED
        
    def makeLeft(self):
        self.cmstext=Position.CMSText.LEFT_STACKED
        self.legend=Position.Legend.LEFT_STACKED
        self.lumi=Position.Lumi.RIGHT
        self.canvas=Position.Canvas.FILLED
        
    def makeLegendOutside(self):
        self.cmstext=Position.CMSText.LEFT_SIDEWAYS
        self.legend=Position.Legend.OUTSIDE
        self.lumi=Position.Lumi.OUTSIDE
        self.canvas=Position.Canvas.OUTSIDE
        
globalPosition=GlobalPosition()
    
