class AxisStyle:
    def __init__(self,title="",fontScale=1.0,offsetScale=1.0,thickScale=1.0):
        self.fontScale=fontScale
        self.offsetScale=offsetScale
        self.thickScale=thickScale
        self.title=title
        self.unit=""
        
        self.enableUnit=True
        
        self.titleSize=11
        self.titleOffset=1
        self.titleFont=43
        self.titleColor=1
        
        self.labelSize=9
        self.labelOffset=0.015
        self.labelFont=43
        self.labelColor=1
        
        self.ownLabels=[]
        
        self.tickLength=0.02 
        self.ndiv=510
        self.exponent=True
        
        
    def applyStyle(self,rootAxis):
        title = ""
        if self.title=="":
            title +=rootAxis.GetTitle()
        else:
            title +=self.title
        if self.enableUnit:
            title+=self.unit
        
        rootAxis.SetTitle(title)    
        
        rootAxis.SetTitleSize(self.titleSize*self.fontScale)
        rootAxis.SetTitleOffset(self.titleOffset*self.offsetScale)
        rootAxis.SetTitleFont(self.titleFont)
        rootAxis.SetTitleColor(self.titleColor)
        
        
        rootAxis.SetLabelSize(self.labelSize*self.fontScale)
        rootAxis.SetLabelOffset(self.labelOffset*self.offsetScale)
        rootAxis.SetLabelFont(self.labelFont)
        rootAxis.SetLabelColor(self.labelColor)
        
        if len(self.ownLabels)>0:
            for i,label in enumerate(self.ownLabels):
                rootAxis.SetBinLabel(i,label)
        
        rootAxis.SetTickLength(self.tickLength*self.thickScale)
        rootAxis.SetNdivisions(self.ndiv)
        rootAxis.SetNoExponent(not self.exponent)
        rootAxis.SetDecimals(True)
        
        
class CoordinateStyle:
    def __init__(self,xtitle="",ytitle="",unitBinning=None,unit="",fontScale=1):
        self.xaxis=AxisStyle(xtitle,fontScale)
        self.yaxis=AxisStyle(ytitle,fontScale)
        
        self.xaxis.titleOffset=1.0
        self.xaxis.ndiv=505
        self.xaxis.exponent=False
        self.yaxis.titleOffset=1.25
        
        self.unitBinning=unitBinning
        self.unit=unit
        
    def setFontScale(self,fontScale=1):
        self.xaxis.fontScale=fontScale
        self.yaxis.fontScale=fontScale
        
    def applyStyle(self,rootGrid):
        unit=""
        if self.unitBinning:
            if self.unit!="":
                unit=self.unit
                self.xaxis.unit=" ("+unit+")"
            else:
                unit="units"
            diff = self.unitBinning.getArray()[1]-self.unitBinning.getArray()[0]
            if diff==1.0*int(diff):
                self.yaxis.unit=" / "+str(int(diff))+" "+unit
            elif (round(diff,2)>=0.02):
                self.yaxis.unit=" / "+str(round(diff,2))+" "+unit
            elif (1000.0*diff)==1.0*int(1000.0*diff):
                self.yaxis.unit=" / "+str(int(diff*1000))+"#upoint 10^{-3} "+unit
            else:
                self.yaxis.unit=" / "+str(round(diff*1000,2))+"#upoint 10^{-3} "+unit
        self.xaxis.applyStyle(rootGrid.GetXaxis())
        self.yaxis.applyStyle(rootGrid.GetYaxis())
        
        
        
        
        
        
    
        
