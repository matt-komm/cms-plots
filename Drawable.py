class Drawable:
    def __init__(self,hasAxis=True, allowLayout=False):
        self.hasAxis=hasAxis
        self.allowLayout=allowLayout
        self.boundingBox={"x":0,"y":0,"w":0,"h":0}
        
    def draw(self):
        raise NotImplemented
