class AxisStyle:
    def __init__(self,title="",scale=1.0):
        self.scale=scale
    
        self.title=title
        self.unit=""
        
        self.titleSize=0.06
        self.titleOffset=1
        self.titleFont=42
        self.titleColor=1
        
        self.labelSize=0.05
        self.labelOffset=0.015
        self.labelFont=42
        self.labelColor=1
        
        self.tickLength=0.03 
        self.ndiv=510
        self.exponent=True
        
        
    def applyStyle(self,rootAxis):
        if self.title=="":
            rootAxis.SetTitle(rootAxis.GetTitle()+self.unit)
        else:
            rootAxis.SetTitle(self.title+self.unit)
            
        rootAxis.SetTitleSize(self.titleSize*self.scale)
        rootAxis.SetTitleOffset(self.titleOffset*self.scale)
        rootAxis.SetTitleColor(self.titleColor)
        
        rootAxis.SetLabelSize(self.labelSize*self.scale)
        rootAxis.SetLabelOffset(self.labelOffset*self.scale)
        rootAxis.SetLabelFont(self.labelFont)
        rootAxis.SetLabelColor(self.labelColor)
        
        rootAxis.SetTickLength(self.tickLength)
        rootAxis.SetNdivisions(self.ndiv)
        rootAxis.SetNoExponent(not self.exponent)
        rootAxis.SetDecimals(True)
        
        
class CoordinateStyle:
    def __init__(self,xtitle="",ytitle="",unitBinning=None,unit="",xscale=1,yscale=1):
        self.xaxis=AxisStyle(xtitle,xscale)
        self.yaxis=AxisStyle(ytitle,yscale)
        
        self.xaxis.titleOffset=1.05
        self.yaxis.titleOffset=1.3
        
        self.unitBinning=unitBinning
        self.unit=unit
        
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
            else:
                self.yaxis.unit=" / "+str(round(diff,2))+" "+unit
        self.xaxis.applyStyle(rootGrid.GetXaxis())
        self.yaxis.applyStyle(rootGrid.GetYaxis())
        
        
        
        
        
    
        
