import ROOT
import math
from Style import *

class SystematicVariation:
    def __init__(self):
        pass
        
    def getUpHistogram(self):
        raise NotImplemented
        
    def getDownHistogram(self):
        raise NotImplemented
        
    def getNominalHistogram(self):
        raise NotImplemented
        
    def getSampleHistogram(self,p=None):
        raise NotImplemented
    
class SystematicVariationPoisson(SystematicVariation):
    STAT,MCSTAT=range(2)
    def __init__(self,histogram,mode=STAT):
        SystematicVariation.__init__(self)
        self._histogram=histogram
        
    def getUpHistogram(self):
        rootHist=self._histogram.getRootHistogram()
        sampledHist=ROOT.TH1F(rootHist)
        for ibin in range(rootHist.GetNbinsX()+2):
            if mode==STAT:
                sampledHist.SetBinContent(ibin,rootHist.GetBinContent(ibin)+ROOT.TMath.Sqrt(rootHist.GetBinContent(ibin)))
            else:
                sampledHist.SetBinContent(ibin,rootHist.GetBinContent(ibin)+rootHist.GetBinError(ibin))
        return sampledHist
        
    def getDownHistogram(self):
        rootHist=self._histogram.getRootHistogram()
        sampledHist=ROOT.TH1F(rootHist)
        for ibin in range(rootHist.GetNbinsX()+2):
            if mode==STAT:
                sampledHist.SetBinContent(ibin,rootHist.GetBinContent(ibin)-ROOT.TMath.Sqrt(rootHist.GetBinContent(ibin)))
            else:
                sampledHist.SetBinContent(ibin,rootHist.GetBinContent(ibin)-rootHist.GetBinError(ibin))
        return sampledHist
        
    def getSampleHistogram(self,p=None):
        rootHist=self._histogram.getRootHistogram()
        sampledHist=ROOT.TH1F(rootHist)
        for ibin in range(rootHist.GetNbinsX()+2):
            if mode==STAT:
                sampledHist.SetBinContent(ibin,ROOT.gRandom.PoissonD(rootHist.GetBinContent(ibin)))
            else:
                sampledHist.SetBinContent(ibin,ROOT.gRandom.Gaus(rootHist.GetBinContent(ibin),rootHist.GetBinError(ibin)))
        return sampledHist
                
class SystematicVariationRate(SystematicVariation):
    def __init__(self,histogram,rate):
        SystematicVariation.__init__(self)
        self._histogram=histogram
        self._rate=rate
        
    def getUpHistogram(self):
        rootHist=self._histogram.getRootHistogram()
        sampledHist=ROOT.TH1F(rootHist)
        for ibin in range(rootHist.GetNbinsX()+2):
            sampledHist.SetBinContent(ibin,rootHist.GetBinContent(ibin)*(1.0+self._rate))
        return sampledHist
        
    def getDownHistogram(self):
        rootHist=self._histogram.getRootHistogram()
        sampledHist=ROOT.TH1F(rootHist)
        for ibin in range(rootHist.GetNbinsX()+2):
            sampledHist.SetBinContent(ibin,rootHist.GetBinContent(ibin)*(1.0-self._rate))
        return sampledHist
        
    def getSampleHistogram(self,p=None):
        if p==None:
            p=ROOT.gRandom.Gaus(0.0,self._rate)
        rootHist=self._histogram.getRootHistogram()
        sampledHist=ROOT.TH1F(rootHist)
        for ibin in range(rootHist.GetNbinsX()+2):
            sampledHist.SetBinContent(ibin,rootHist.GetBinContent(ibin)*(1.0+p))
        return sampledHist
        
    
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
        nomHist=self._nominalHist.getRootHistogram()
        upHist=self._upHist.getRootHistogram()
        downHist=self._downHist.getRootHistogram()
        
        sampledHist=ROOT.TH1F(nomHist)
        for ibin in range(rootHist.GetNbinsX()+2):
            nom=nomHist.GetBinContent(ibin)
            up=upHist.GetBinContent(ibin)
            down=downHist.GetBinContent(ibin)
            sampledHist.SetBinContent(ibin,morphBin(up,nom,down,p))
        return sampledHist
            
    
    
class SystematicBandStyle(FillStyle):
    def __init__(self):
        FillStyle.__init__(self)
        self.up=LineStyle()
        self.down=LineStyle()
        
    def applyStyle(self,rootPolyUp,rootPolyDown):
        pass
    
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
        if 
        
    def getBoundingBox(self):
        raise NotImplemented
        
    def getLegendInfo(self):
        return []
        
    
        
