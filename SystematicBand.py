import ROOT
import math
import numpy
from Style import *
from Drawable import *

class SystematicVariation:
    def __init__(self):
        self._sampledHist=None
        
    def getUpHistogram(self):
        raise NotImplemented
        
    def getDownHistogram(self):
        raise NotImplemented
        
    def getNominalHistogram(self):
        raise NotImplemented
        
    def getSampleHistogram(self,p=None):
        raise NotImplemented
        
    def addHist(self,sysVariation,scale=1.0):
        def add(self,sysVariation1,sysVariation2):
            self._sampledHist=ROOT.TH1F(sysVariation1.getNominalHistogram())
            self._sampledHist.Scale(0)
            for ibin in range(sysVariation1.GetNbinsX()+2):
                self._sampledHist.SetBinContent(ibin,sysVariation1.GetBinContent(ibin)+scale*sysVariation2.GetBinContent(ibin))
            return self._sampledHist
        return TransformedSystematic(self,sysVariation,add)
        
    def divideHist(self,sysVariation):
        def add(self,sysVariation1,sysVariation2):
            self._sampledHist=ROOT.TH1F(sysVariation1.getNominalHistogram())
            self._sampledHist.Scale(0)
            for ibin in range(sysVariation1.GetNbinsX()+2):
                try:
                    self._sampledHist.SetBinContent(ibin,sysVariation1.GetBinContent(ibin)/sysVariation2.GetBinContent(ibin))
                except Exception,e:
                    pass
            return self._sampledHist
        return TransformedSystematic(self,sysVariation,add)
        
        
class TransformedSystematic(SystematicVariation):
    def __init__(self,sysVariation1,sysVariation2,fct=lambda obj,sysVariation1,sysVariation2:sysVariation1):
        SystematicVariation.__init__(self)
        self._sysVariation1=sysVariation1
        self._sysVariation2=sysVariation2
        self._fct=fct
        
    def getUpHistogram(self):
        return self._fct(self,self._sysVariation1.getUpHistogram(),self._sysVariation2.getUpHistogram())
        
    def getDownHistogram(self):
        return self._fct(self,self._sysVariation1.getDownHistogram(),self._sysVariation2.getDownHistogram())
        
    def getNominalHistogram(self):
        return self._fct(self,self._sysVariation1.getNominalHistogram(),self._sysVariation2.getNominalHistogram())
        
    def getSampleHistogram(self,p=None):
        return self._fct(self,self._sysVariation1.getSampleHistogram(p),self._sysVariation2.getSampleHistogram(p))
        
    
class SystematicVariationPoisson(SystematicVariation):
    STAT,MCSTAT=range(2)
    def __init__(self,histogram,mode=STAT):
        SystematicVariation.__init__(self)
        self._mode=mode
        self._histogram=histogram
        
    def getUpHistogram(self):
        rootHist=self._histogram
        self._sampledHist=ROOT.TH1F(rootHist)
        for ibin in range(rootHist.GetNbinsX()+2):
            if self._mode==SystematicVariationPoisson.STAT:
                self._sampledHist.SetBinContent(ibin,rootHist.GetBinContent(ibin)+ROOT.TMath.Sqrt(rootHist.GetBinContent(ibin)))
            else:
                self._sampledHist.SetBinContent(ibin,rootHist.GetBinContent(ibin)+rootHist.GetBinError(ibin))
        return self._sampledHist
        
    def getDownHistogram(self):
        rootHist=self._histogram
        self._sampledHist=ROOT.TH1F(rootHist)
        for ibin in range(rootHist.GetNbinsX()+2):
            if self._mode==SystematicVariationPoisson.STAT:
                self._sampledHist.SetBinContent(ibin,rootHist.GetBinContent(ibin)-ROOT.TMath.Sqrt(rootHist.GetBinContent(ibin)))
            else:
                self._sampledHist.SetBinContent(ibin,rootHist.GetBinContent(ibin)-rootHist.GetBinError(ibin))
        return self._sampledHist
        
    def getNominalHistogram(self):
        return self._histogram
        
    def getSampleHistogram(self,p=None):
        rootHist=self._histogram
        self._sampledHist=ROOT.TH1F(rootHist)
        for ibin in range(rootHist.GetNbinsX()+2):
            if self._mode==SystematicVariationPoisson.STAT:
                self._sampledHist.SetBinContent(ibin,ROOT.gRandom.Poisson(rootHist.GetBinContent(ibin)))
            else:
                self._sampledHist.SetBinContent(ibin,ROOT.gRandom.Gaus(rootHist.GetBinContent(ibin),rootHist.GetBinError(ibin)))
        return self._sampledHist
                
class SystematicVariationRate(SystematicVariation):
    def __init__(self,histogram,rate):
        SystematicVariation.__init__(self)
        self._histogram=histogram
        self._rate=rate
        
    def getUpHistogram(self):
        rootHist=self._histogram
        self._sampledHist=ROOT.TH1F(rootHist)
        for ibin in range(rootHist.GetNbinsX()+2):
            self._sampledHist.SetBinContent(ibin,rootHist.GetBinContent(ibin)*(1.0+self._rate))
        return self._sampledHist
        
    def getDownHistogram(self):
        rootHist=self._histogram
        self._sampledHist=ROOT.TH1F(rootHist)
        for ibin in range(rootHist.GetNbinsX()+2):
            self._sampledHist.SetBinContent(ibin,rootHist.GetBinContent(ibin)*(1.0-self._rate))
        return self._sampledHist
        
    def getNominalHistogram(self):
        return self._histogram
        
    def getSampleHistogram(self,p=None):
        if p==None:
            p=ROOT.gRandom.Gaus(0.0,self._rate)
        rootHist=self._histogram
        self._sampledHist=ROOT.TH1F(rootHist)
        for ibin in range(rootHist.GetNbinsX()+2):
            self._sampledHist.SetBinContent(ibin,rootHist.GetBinContent(ibin)*(1.0+p))
        return self._sampledHist
        
    
class SystematicVariationTemplate(SystematicVariation):
    def __init__(self,nominalHist,upHist,downHist):
        SystematicVariation.__init__(self)
        self._nominalHist=nominalHist
        self._upHist=upHist
        self._downHist=downHist
        
    def getUpHistogram(self):
        return self._upHist
        
    def getDownHistogram(self):
        return self._downHist
        
    def getNominalHistogram(self):
        return self._nominalHist
        
    def morphBin(up,nom,down,p):
        if p>1:
            return (up-nom)*math.fabs(d)+nom
        elif p<-1:
            return (down-nom)*math.fabs(d)+nom
        else:
            return nom+d/2.0*(up-down)+(d*d-math.fabs(d*d*d)/2.0)*(up+down-2.0*nom)

    def getSampleHistogram(self,p=None):
        if p==None:
            p=ROOT.gRandom.Gaus(0,1)
        nomHist=self._nominalHist
        upHist=self._upHist
        downHist=self._downHist
        
        self._sampledHist=ROOT.TH1F(nomHist)
        for ibin in range(rootHist.GetNbinsX()+2):
            nom=nomHist.GetBinContent(ibin)
            up=upHist.GetBinContent(ibin)
            down=downHist.GetBinContent(ibin)
            self._sampledHist.SetBinContent(ibin,morphBin(up,nom,down,p))
        return self._sampledHist
            
    
    
class SystematicBandStyle(FillStyle):
    def __init__(self):
        FillStyle.__init__(self)
        self.up=LineStyle()
        self.down=LineStyle()
        
    def applyStyle(self,rootPolyUp,rootPolyDown):
        pass
'''
class SystematicBand(Drawable):
    CORRELATED,UNCORRELATED,TOYS=range(3)
    def __init__(self,mode=UNCORRELATED):
        Drawable.__init__(self,hasAxis=True, allowLayout=False)
        self._systematicVariations={}
        self._style=SystematicBandStyle()
        
    def setStyle(self,style):
        self._style=style
        
    def addSystematicSource(self,name,systematicVariation):
        self._systematicVariations[name]=systematicVariation
        
    def draw(self,canvas,strech=Strech(),addOptions=""):
        BINS = self._systematicVariations.values()[0].getNominalHistogram().GetNbinsX()
        TOYS = 100
        binDist=numpy.zeros((BINS,TOYS))
        for itoy in range(TOYS):
            hist = self._systematicVariations.values()[0].getSampleHistogram()
            for ibin in range(BINS):
                binDist[ibin][itoy]=hist.GetBinContent(ibin+1)
        #print binDist[0]
                
        upEdge=numpy.zeros(BINS)
        downEdge=numpy.zeros(BINS)
        for ibin in range(BINS):
            q = numpy.percentile(binDist[ibin],[0.1585,0.8415])
            upEdge[ibin]=q[0]
            downEdge[ibin]=q[1]
            print ibin,q
        
        
    def getBoundingBox(self):
        raise NotImplemented
        
    def getLegendInfo(self):
        return []
'''     
    
class SystematicBand(Drawable):
    def __init__(self,upHist,downHist):
        Drawable.__init__(self,hasAxis=True, allowLayout=False)
        self._style=SystematicBandStyle()
        self._upHist=upHist
        self._downHist=downHist
        
        self._boxes=[]
        
    def setStyle(self,style):
        self._style=style
        
        
    def draw(self,canvas,strech=Strech(),addOptions=""):
        self._boxes=[]
        for ibin in range(self._upHist.getRootHistogram().GetNbinsX()):
            up=self._upHist.getRootHistogram().GetBinContent(ibin+1)
            down=self._downHist.getRootHistogram().GetBinContent(ibin+1)
            center=self._upHist.getRootHistogram().GetBinCenter(ibin+1)
            width=self._upHist.getRootHistogram().GetBinWidth(ibin+1)
            left=center-0.5*width
            right=center+0.5*width
            box=ROOT.TBox(left,down,right,up)
            box.SetFillStyle(1001)
            box.SetFillColor(ROOT.kGray)
            self._boxes.append(box)
            box.Draw("FSame")
            print left,down,right,up
        
    def getBoundingBox(self):
        raise NotImplemented
        
    def getLegendInfo(self):
        return []
        
