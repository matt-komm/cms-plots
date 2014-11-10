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
        
    class Lumi:
        RIGHT=BoundingBox(BoundingBox.PERCENTS,0.6,0.995,0.965,0.995)
