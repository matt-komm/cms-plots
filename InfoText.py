from Drawable import *
from Position import *

import ROOT
import ctypes
import numpy


class TextItem:
    def __init__(self,text="",font=43,size=10):
        self.text=text
        self.font=font
        self.size=size

class InfoText(Drawable):
    SIDEWAYS,STACKED=range(2)
    def __init__(self,textItemList=[],orientation=SIDEWAYS,position=Position.CMSText.LEFT_SIDEWAYS,alignment=11):
        Drawable.__init__(self,hasAxis=False, allowLayout=True)
        self.textItemList=textItemList
        self._orientation=orientation
        self._xmin=position.xmin
        self._xmax=position.xmax
        self._ymin=position.ymin
        self._ymax=position.ymax
        self._alignment=alignment
        self._paves=[]
        
    @staticmethod
    def createCMSText(preliminary=True,simulation=False, orientation=SIDEWAYS,position=Position.CMSText.LEFT_SIDEWAYS):
        textItemList=[]
        textItemList.append(TextItem("CMS",63,10))
        addtext=""
        if simulation:
            addtext+="Simulation"
        if preliminary:
            addtext+="Preliminary"
        if addtext!="":
            textItemList.append(TextItem(addtext,53,10))
        infoText = InfoText(textItemList,position=position,orientation=orientation)
        return infoText  
    
    @staticmethod
    def createLumiText(position=Position.Lumi.RIGHT,alignment=33,lumi="19.7"):
        textItemList=[TextItem(lumi+" fb^{-1} #lower[-0.1]{#scale[0.9]{(}}8 TeV#lower[-0.1]{#scale[0.9]{)}}",43,9)]
        infoText = InfoText(textItemList,position=position,alignment=alignment,orientation=InfoText.SIDEWAYS)
        return infoText
        
        
    def draw(self,canvas,strech=Strech(),addOptions=""):
        del self._paves[:]
        if self._orientation==InfoText.SIDEWAYS:
            #splitting according to number of characters
            xstart=self._xmin
            xend=self._xmin
            
            for i,item in enumerate(self.textItemList):  
                #xend=self._xmin*strech.xminStrech+(self._xmax*strech.xmaxStrech-self._xmin*strech.xminStrech)/length*ROOT.FontMetrics.GetTextWidth(item.font,item.size,item.text)*(i+1)
                xend+=1.0*ROOT.FontMetrics.GetTextWidth(item.font,item.size*strech.fontStrech,item.text)/canvas.widthPx+0.005
                
                self.rootPaveText=ROOT.TPaveText(xstart,self._ymin,xstart,self._ymin,"NDC")
                self.rootPaveText.SetFillColor(0)
                self.rootPaveText.SetFillStyle(0)
                self.rootPaveText.SetTextAlign(13) 
                self.rootPaveText.SetBorderSize(0)
                self.rootPaveText.SetTextFont(item.font)
                self.rootPaveText.SetTextSize(item.size*strech.fontStrech)
                self.rootPaveText.AddText(item.text)
                self.rootPaveText.Draw("SAME")
                self._paves.append(self.rootPaveText)
                xstart=xend
        elif self._orientation==InfoText.STACKED:
            ystart=self._ymin
            yend=self._ymin
            for i,item in enumerate(self.textItemList):  
                ystart-=1.0*ROOT.FontMetrics.GetTextHeight(item.font,item.size*strech.fontStrech,item.text)/canvas.heightPx-0.004
                print ystart,yend,item.text
                self.rootPaveText=ROOT.TPaveText(self._xmin,ystart,self._xmin,ystart,"NDC")
                self.rootPaveText.SetFillColor(0)
                self.rootPaveText.SetFillStyle(0)
                self.rootPaveText.SetTextAlign(11) 
                self.rootPaveText.SetBorderSize(0)
                self.rootPaveText.SetTextFont(item.font)
                self.rootPaveText.SetTextSize(item.size*strech.fontStrech)
                self.rootPaveText.AddText(item.text)
                self.rootPaveText.Draw("SAME")
                self._paves.append(self.rootPaveText)
                yend=ystart
        
        
    def getBoundingBox(self):
        return BoundingBox(
            BoundingBox.PERCENTS,
            self._xmin,
            self._ymin,
            self._xmax,
            self._ymax
        )
        
    def getLegendInfo(self):
        return []
