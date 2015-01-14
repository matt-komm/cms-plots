import random
import ROOT
import copy

from Axis import *
from Drawable import *

class Canvas:
    def __init__(self, widthCM=7.3,heightCM=6.0,margins=BoundingBox(BoundingBox.PERCENTS,0.16,0.14,1-0.055,1-0.065)):
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
        self.rootCanvas.SetTopMargin(1-margins.ymax)
        self.rootCanvas.SetBottomMargin(margins.ymin)
        self.rootCanvas.SetLeftMargin(margins.xmin)
        self.rootCanvas.SetRightMargin(1-margins.xmax)

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
        tdrStyle.SetDrawBorder(0)
        tdrStyle.SetCanvasBorderMode(0)
        tdrStyle.SetCanvasColor(ROOT.kWhite)
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
        #ROOT.TGaxis.SetExponentOffset(0.0,0.0,"XY")
        #ROOT.TGaxis.SetExponentOffset(0.0,0.007,"Y")
        ROOT.TGaxis.SetMaxDigits(3)
        
        self._coordinateStyle=CoordinateStyle()
        self._grid=None
        
        self._constSpace={"xmin":0.0,"xmax":0.0,"ymin":0.0,"ymax":0.0}
        self._factorSpace={"xmin":1.0,"xmax":1.0,"ymin":1.0,"ymax":1.13}
        
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
        
    def save(self,name):
        self.rootCanvas.Print(name)
    
        
    def draw(self):
        self.rootCanvas.cd()
        boundingBox=None
        strech=Strech()
        strech.fontStrech=self.getPtInPx()
        for i in range(len(self._drawables)):
            if self._drawables[i].hasAxis:
                self._drawables[i].draw(self,strech=strech)
                if boundingBox==None:
                    boundingBox=self._drawables[i].getBoundingBox()
                else:
                    boundingBox.union(self._drawables[i].getBoundingBox())
        self._grid=ROOT.TH2F("axis"+str(random.random()),"",
            50,boundingBox.xmin*self._factorSpace["xmin"]-self._constSpace["xmin"],boundingBox.xmax*self._factorSpace["xmax"]+self._constSpace["xmax"],
            50,boundingBox.ymin*self._factorSpace["ymin"]-self._constSpace["ymin"],boundingBox.ymax*self._factorSpace["ymax"]+self._constSpace["ymax"]
        )
        self._coordinateStyle.setFontScale(strech.fontStrech)
        self._coordinateStyle.xaxis.thickScale=1.0/(1-self.rootCanvas.GetLeftMargin()-self.rootCanvas.GetRightMargin())
        self._coordinateStyle.yaxis.thickScale=1.0/(1-self.rootCanvas.GetTopMargin()-self.rootCanvas.GetBottomMargin())
        self._coordinateStyle.applyStyle(self._grid)
        self._grid.Draw("AXIS")
        
        for i in range(len(self._drawables)):
            self._drawables[i].draw(self,strech=strech,addOptions="SAME")
        self._grid.Draw("AXIS SAME")
        #self.rootCanvas.Print("test4.pdf")
        
    def wait(self):
        self.rootCanvas.Update()
        self.rootCanvas.WaitPrimitive()
        
        
class CanvasResiduen:
    def __init__(self, widthCM=7.3,heightCM=6.0,resHeight=0.37,resRange=[0.2,1.90],margins=BoundingBox(BoundingBox.PERCENTS,0.16,0.14,1-0.055,1-0.065)):
        self.widthCM=widthCM
        self.heightCM=heightCM
        self.resHeight=resHeight
        self.resRange=resRange
        self.margins=margins
                
        #by default canvasSize=20x20cm
        
        self.widthPx=800
        self.heightPx=800
        
        if self.widthCM<self.heightCM:
            self.widthPx=int(round(1.0*self.widthPx*self.widthCM/self.heightCM))
        else:
            self.heightPx=int(round(1.0*self.heightPx*self.heightCM/self.widthCM))
        
        
        
        
        self._drawables=[]
        self._drawablesRes=[]
        
        self.rootCanvas=ROOT.TCanvas("canvas"+str(random.random()),"",self.widthPx,self.heightPx)
        if (ROOT.gROOT.IsBatch()):
            self.rootCanvas.SetCanvasSize(self.widthPx,self.heightPx)
        else:
            self.rootCanvas.SetWindowSize(self.widthPx + (self.widthPx - self.rootCanvas.GetWw()), self.heightPx + (self.heightPx - self.rootCanvas.GetWh()))
        
        
        self.rootCanvas.Divide(1,2,0,0)
        
        
        #overlay two transparent pads
        self.rootCanvas.GetPad(1).SetPad(0.0, 0.0, 1.0, 1.0)
        self.rootCanvas.GetPad(1).SetFillStyle(4000)
        self.rootCanvas.GetPad(2).SetPad(0.0, 0.00, 1.0,1.0)
        self.rootCanvas.GetPad(2).SetFillStyle(4000)
        
        
        
        for i in range(1,3):
            #for the canvas:
            self.rootCanvas.GetPad(i).SetBorderMode(0)
            self.rootCanvas.GetPad(i).SetGridx(False)
            self.rootCanvas.GetPad(i).SetGridy(False)


            #For the frame:
            self.rootCanvas.GetPad(i).SetFrameBorderMode(0)
            self.rootCanvas.GetPad(i).SetFrameBorderSize(1)
            self.rootCanvas.GetPad(i).SetFrameFillColor(0)
            self.rootCanvas.GetPad(i).SetFrameFillStyle(0)
            self.rootCanvas.GetPad(i).SetFrameLineColor(1)
            self.rootCanvas.GetPad(i).SetFrameLineStyle(1)
            self.rootCanvas.GetPad(i).SetFrameLineWidth(1)

            # Margins:
            self.rootCanvas.GetPad(i).SetLeftMargin(margins.xmin)
            self.rootCanvas.GetPad(i).SetRightMargin(1-margins.xmax)
            
            # For the Global title:
            self.rootCanvas.GetPad(i).SetTitle("")
            
            # For the axis:
            self.rootCanvas.GetPad(i).SetTickx(1)  # To get tick marks on the opposite side of the frame
            self.rootCanvas.GetPad(i).SetTicky(1)

            # Change for log plots:
            self.rootCanvas.GetPad(i).SetLogx(0)
            self.rootCanvas.GetPad(i).SetLogy(0)
            self.rootCanvas.GetPad(i).SetLogz(0)
        
        
        
        self.rootCanvas.GetPad(2).SetTopMargin(1-margins.ymax)
        self.rootCanvas.GetPad(2).SetBottomMargin(self.resHeight)
        self.rootCanvas.GetPad(1).SetTopMargin(1-self.resHeight)
        self.rootCanvas.GetPad(1).SetBottomMargin(margins.ymin)

        
        
        

        
        tdrStyle =  ROOT.TStyle("tdrStyle","Style for P-TDR")
        tdrStyle.SetOptTitle(0)
        tdrStyle.SetOptStat(0)
        tdrStyle.SetOptFit(0)
        tdrStyle.SetOptDate(0)
        tdrStyle.SetOptFile(0)
        tdrStyle.SetDrawBorder(0)
        tdrStyle.SetCanvasBorderMode(0)
        tdrStyle.SetCanvasColor(ROOT.kWhite)
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
        #ROOT.TGaxis.SetExponentOffset(0.0,0.0,"XY")
        #ROOT.TGaxis.SetExponentOffset(0.0,0.007,"Y")
        ROOT.TGaxis.SetMaxDigits(3)
        
        self._coordinateStyle=CoordinateStyle()
        self._grid=None
        
        self._constSpace={"xmin":0.0,"xmax":0.0,"ymin":0.0,"ymax":0.0}
        self._factorSpace={"xmin":1.0,"xmax":1.0,"ymin":1.0,"ymax":1.25}
        
       
        
        #print self.rootCanvas.GetXsizeReal(),self.rootCanvas.GetYsizeReal()
        
    def getPtInPx(self,pt=1.0):
        # 1pT=1/72in, 1in=2.54cm, page=20cm height
        return pt/72.0*2.54/20.0*self.heightPx*20.0/self.heightCM #*0.93376068 #for TT fonts
        
    def setCoordinateStyle(self,style):
        self._coordinateStyle=copy.deepcopy(style)
        self._coordinateStyle.xaxis.titleSize=0.00000000000000000000001
        self._coordinateStyle.xaxis.lableSize=0.00000000000000000000001
        self._coordinateStyleRes=copy.deepcopy(style)
        #self._coordinateStyleRes.yaxis.labelSize=0.000001
        self._coordinateStyleRes.yaxis.title="data/MC"
        self._coordinateStyleRes.yaxis.ndiv=504
        self._coordinateStyleRes.yaxis.enableUnit=False
        '''
        self._coordinateStyleRes.yaxis.ownLabels=[]
        for i in range(50):
            if i%5==0:
                self._coordinateStyleRes.yaxis.ownLabels.append(str(i))
            else:
                self._coordinateStyleRes.yaxis.ownLabels.append("")
        '''
        
    def addDrawable(self,drawable):
        self._drawables.append(drawable)
        
    def addResiduen(self,drawable):
        self._drawablesRes.append(drawable)
        
    def setConstSpace(self,key,value):
        self._constSpace[key]=value
        
    def setFactorSpace(self,key,value):
        self._factorSpace[key]=value
        
    def save(self,name):
        self.rootCanvas.Print(name)
    
    def draw(self):
        strech = Strech()
        strech.fontStrech=self.getPtInPx()
        strech.ymaxStrech=1
        strech.yminStrech=1
        
        self.rootCanvas.cd(2)
        boundingBox=None
        
        for i in range(len(self._drawables)):
            if self._drawables[i].hasAxis:
                self._drawables[i].draw(self,strech=strech)
                if boundingBox==None:
                    boundingBox=self._drawables[i].getBoundingBox()
                else:
                    boundingBox.union(self._drawables[i].getBoundingBox())
    
        self.rootCanvas.cd(1)
        
        self._resgrid=ROOT.TH2F("res"+str(random.random()),"",
            50,boundingBox.xmin*self._factorSpace["xmin"]-self._constSpace["xmin"],boundingBox.xmax*self._factorSpace["xmax"]+self._constSpace["xmax"],
            50,self.resRange[0],self.resRange[1]
        )
        
        
        self._coordinateStyleRes.xaxis.fontScale=strech.fontStrech
        self._coordinateStyleRes.yaxis.fontScale=strech.fontStrech
        self._coordinateStyleRes.xaxis.thickScale=1.0/(1-self.rootCanvas.GetPad(1).GetLeftMargin()-self.rootCanvas.GetPad(1).GetRightMargin())
        self._coordinateStyleRes.yaxis.thickScale=1.0/(1-self.rootCanvas.GetPad(1).GetTopMargin()-self.rootCanvas.GetPad(1).GetBottomMargin())

        self._coordinateStyleRes.applyStyle(self._resgrid)
        self._resgrid.Draw("AXIS")
        for i in range(len(self._drawablesRes)):
            self._drawablesRes[i].draw(self,strech=strech,addOptions="SAME")
            
        height = 0.004+1.0*ROOT.FontMetrics.GetTextHeight(self._coordinateStyleRes.yaxis.labelFont,self._coordinateStyleRes.yaxis.labelSize*strech.fontStrech,"0.0")/self.heightPx
        width = 1.0*ROOT.FontMetrics.GetTextWidth(self._coordinateStyleRes.yaxis.labelFont,self._coordinateStyleRes.yaxis.labelSize*strech.fontStrech,"0.0")/self.widthPx
        self._box=ROOT.TPaveText(self.margins.xmin-0.02-width,self.resHeight-height*0.5,self.margins.xmin-0.005,self.resHeight+height*0.5,"NDC")
        self._box.SetFillColor(ROOT.kWhite)
        self._box.SetFillStyle(1001)
        self._box.Draw("Same")
        
        self._resgridaxis=ROOT.TF1("resaxis"+str(random.random()),"1",boundingBox.xmin*self._factorSpace["xmin"]-self._constSpace["xmin"],boundingBox.xmax*self._factorSpace["xmax"]+self._constSpace["xmax"])
        self._resgridaxis.SetLineColor(1)
        self._resgridaxis.SetLineStyle(1)
        self._resgridaxis.SetLineWidth(1)
        self._resgridaxis.Draw("SAME")
        self._resgrid.Draw("AXIS SAME")
        
        
    
        self.rootCanvas.cd(2)
        self._grid=ROOT.TH2F("axis"+str(random.random()),"",
            50,boundingBox.xmin*self._factorSpace["xmin"]-self._constSpace["xmin"],boundingBox.xmax*self._factorSpace["xmax"]+self._constSpace["xmax"],
            50,boundingBox.ymin*self._factorSpace["ymin"]-self._constSpace["ymin"],boundingBox.ymax*self._factorSpace["ymax"]+self._constSpace["ymax"]
        )

        self._coordinateStyle.xaxis.fontScale=0
        self._coordinateStyle.yaxis.fontScale=strech.fontStrech
        self._coordinateStyle.xaxis.thickScale=1.0/(1-self.rootCanvas.GetPad(2).GetLeftMargin()-self.rootCanvas.GetPad(2).GetRightMargin())
        self._coordinateStyle.yaxis.thickScale=1.0/(1-self.rootCanvas.GetPad(2).GetTopMargin()-self.rootCanvas.GetPad(2).GetBottomMargin())
        
        self._coordinateStyle.applyStyle(self._grid)
        self._grid.Draw("AXIS")
        
        for i in range(len(self._drawables)):
            self._drawables[i].draw(self,strech=strech,addOptions="SAME")
        self._grid.Draw("AXIS SAME")

        
    def wait(self):
        self.rootCanvas.Update()
        self.rootCanvas.WaitPrimitive()
