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
    def __init__(self,xtitle="",ytitle="",xscale=1,yscale=1):
        self.xaxis=AxisStyle(xtitle,xscale)
        self.yaxis=AxisStyle(ytitle,yscale)
        
        self.xaxis.titleOffset=1.05
        self.yaxis.titleOffset=1.3
        
    def applyStyle(self,rootXaxis,rootYaxis,unitAxis=None,unit=""):
        if unitAxis:
            if unit!="":
                self.xaxis.unit=" ("+unit+")"
            else:
                unit="units"
            if unitAxis.GetBinWidth(1)==1.0*int(unitAxis.GetBinWidth(1)):
                self.yaxis.unit=" / "+str(int(unitAxis.GetBinWidth(1)))+" "+unit
            else:
                self.yaxis.unit=" / "+str(round(unitAxis.GetBinWidth(1),2))+" "+unit
        self.xaxis.applyStyle(rootXaxis)
        self.yaxis.applyStyle(rootYaxis)
        
        
        
        
        
    
        
