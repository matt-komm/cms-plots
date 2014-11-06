import random
import ROOT

from Axis import *

class Canvas:
    def __init__(self):
        self._drawables=[]
    
        self.rootCanvas=ROOT.TCanvas("canvas"+str(random.random()),"blub",700,600)
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
        tdrStyle.SetPaperSize(20.,20.)
        tdrStyle.SetHatchesLineWidth(5)
        tdrStyle.SetHatchesSpacing(0.05)
        tdrStyle.SetLineScalePS(1.2)
        tdrStyle.SetEndErrorSize(2)
        tdrStyle.SetGridColor(1)
        tdrStyle.SetGridStyle(3)
        tdrStyle.SetGridWidth(1)
        tdrStyle.cd()
        ROOT.TGaxis.SetExponentOffset(0.0,0.0,"XY")
        ROOT.TGaxis.SetMaxDigits(3)
        
        self._coordinateStyle=CoordinateStyle()
        
    def setCoordinateStyle(self,style):
        self._coordinateStyle=style
        
    def addDrawable(self,drawable):
        self._drawables.append(drawable)
        
    def draw(self):
        for drawable in self._drawables:
            drawable.draw()
        
        #self._coordinateStyle.applyStyle(self.rootCanvas)
        
    def wait(self):
        self.rootCanvas.Update()
        self.rootCanvas.WaitPrimitive()
        
