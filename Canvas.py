import random
import ROOT

from Axis import *

class Canvas:
    def __init__(self, widthCM=7.3,heightCM=6.0):
        self.widthCM=widthCM
        self.heightCM=heightCM
        
                
        #by default canvasSize=20x20cm
        
        self.widthPx=800
        self.heightPx=800
        
        if self.widthCM<self.heightCM:
            self.widthPx=int(round(1.0*self.widthPx*self.widthCM/self.heightCM))
        else:
            self.heightPx=int(round(1.0*self.heightPx*self.heightCM/self.widthCM))
        
        
        
        self._drawables=[]
        
        self.rootCanvas=ROOT.TCanvas("canvas"+str(random.random()),"",self.widthPx,self.heightPx)
        if (ROOT.gROOT.IsBatch()):
            self.rootCanvas.SetCanvasSize(self.widthPx,self.heightPx)
        else:
            self.rootCanvas.SetWindowSize(self.widthPx + (self.widthPx - self.rootCanvas.GetWw()), self.heightPx + (self.heightPx - self.rootCanvas.GetWh()))
        
        
        #for the canvas:
        self.rootCanvas.SetBorderMode(0)
        self.rootCanvas.SetFillColor(ROOT.kWhite)
        self.rootCanvas.SetFillStyle(1001)
        self.rootCanvas.SetGridx(False)
        self.rootCanvas.SetGridy(False)


        #For the frame:
        self.rootCanvas.SetFrameBorderMode(0)
        self.rootCanvas.SetFrameBorderSize(1)
        self.rootCanvas.SetFrameFillColor(0)
        self.rootCanvas.SetFrameFillStyle(0)
        self.rootCanvas.SetFrameLineColor(1)
        self.rootCanvas.SetFrameLineStyle(1)
        self.rootCanvas.SetFrameLineWidth(1)


        
        #tdrStyle.SetErrorMarker(20)
        #tdrStyle.SetErrorX(0.)


        # Margins:
        self.rootCanvas.SetTopMargin(0.06)
        self.rootCanvas.SetBottomMargin(0.14)
        self.rootCanvas.SetLeftMargin(0.16)
        self.rootCanvas.SetRightMargin(0.085)

        # For the Global title:

        self.rootCanvas.SetTitle("")

        # For the axis:
        
        self.rootCanvas.SetTickx(1)  # To get tick marks on the opposite side of the frame
        self.rootCanvas.SetTicky(1)

        # Change for log plots:
        self.rootCanvas.SetLogx(0)
        self.rootCanvas.SetLogy(0)
        self.rootCanvas.SetLogz(0)

        
        tdrStyle =  ROOT.TStyle("tdrStyle","Style for P-TDR")
        tdrStyle.SetOptTitle(0)
        tdrStyle.SetOptStat(0)
        tdrStyle.SetOptFit(0)
        tdrStyle.SetOptDate(0)
        tdrStyle.SetOptFile(0)
        tdrStyle.SetStripDecimals(True)
        tdrStyle.SetPaperSize(self.widthCM,self.heightCM) #sets size in cm
        tdrStyle.SetHatchesLineWidth(5)
        tdrStyle.SetHatchesSpacing(0.05)
        tdrStyle.SetLineScalePS(2)
        tdrStyle.SetEndErrorSize(2)
        tdrStyle.SetGridColor(1)
        tdrStyle.SetGridStyle(3)
        tdrStyle.SetGridWidth(1)
        tdrStyle.cd()
        ROOT.TGaxis.SetExponentOffset(0.0,0.0,"XY")
        ROOT.TGaxis.SetMaxDigits(3)
        
        self._coordinateStyle=CoordinateStyle()
        self._grid=None
        
        self._constSpace={"xmin":0.0,"xmax":0.0,"ymin":0.0,"ymax":0.0}
        self._factorSpace={"xmin":1.0,"xmax":1.0,"ymin":1.0,"ymax":1.1}
        
        #print self.rootCanvas.GetXsizeReal(),self.rootCanvas.GetYsizeReal()
        
    def getPtInPx(self,pt=1.0):
        # 1pT=1/72in, 1in=2.54cm, page=20cm height
        return pt/72.0*2.54/20.0*self.heightPx*20.0/self.heightCM #*0.93376068 #for TT fonts
        
    def setCoordinateStyle(self,style):
        self._coordinateStyle=style
        
    def addDrawable(self,drawable):
        self._drawables.append(drawable)
        
    def setConstSpace(self,key,value):
        self._constSpace[key]=value
        
    def setFactorSpace(self,key,value):
        self._factorSpace[key]=value
    
        
    def draw(self):
        self.rootCanvas.cd()
        boundingBox=None
        for i in range(len(self._drawables)):
            if self._drawables[i].hasAxis:
                self._drawables[i].draw(self)
                if boundingBox==None:
                    boundingBox=self._drawables[i].getBoundingBox()
                else:
                    boundingBox.union(self._drawables[i].getBoundingBox())
        self._grid=ROOT.TH2F("axis"+str(random.random()),"",
            50,boundingBox.xmin*self._factorSpace["xmin"]-self._constSpace["xmin"],boundingBox.xmax*self._factorSpace["xmax"]+self._constSpace["xmax"],
            50,boundingBox.ymin*self._factorSpace["ymin"]-self._constSpace["ymin"],boundingBox.ymax*self._factorSpace["ymax"]+self._constSpace["ymax"]
        )
        self._coordinateStyle.applyStyle(self._grid)
        self._grid.Draw("AXIS")
        
        for i in range(len(self._drawables)):
            self._drawables[i].draw(self,"SAME")
        self._grid.Draw("AXIS SAME")
        #self.rootCanvas.Print("test4.pdf")
        
    def wait(self):
        self.rootCanvas.Update()
        self.rootCanvas.WaitPrimitive()
        
        
class CanvasResiduen(Canvas):
    def __init__(self,resSize=0.3,resRange=[-0.3,0.3]):
        Canvas.__init__(self)
        
