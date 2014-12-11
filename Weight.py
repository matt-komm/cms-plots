class Weight:
    def __init__(self,w):
        self.weightStr=w
        
    def __add__(self,w):
        return Weight("("+self.weightStr+"+"+w.weightStr+")")
        
    def __mul__(self,w):
        return Weight(self.weightStr+"*"+w.weightStr)
        
    def get(self):
        return self.weightStr
        
        

c2j0t=Weight("(njets==2)*(ntags==0)")
c2j1t=Weight("(njets==2)*(ntags==1)")
c2j2t=Weight("(njets==2)*(ntags==2)")
c3j0t=Weight("(njets==3)*(ntags==0)")
c3j1t=Weight("(njets==3)*(ntags==1)")
c3j2t=Weight("(njets==3)*(ntags==2)")
c3j3t=Weight("(njets==3)*(ntags==3)")
qcdMuBDT=Weight("(bdt_qcd>0.0)")
qcdEleBDT=Weight("(bdt_qcd>0.2)")
qcdMuMTW=Weight("(mtw>50)")
qcdEleMET=Weight("(met>50)")
lumiMu=Weight("16872")
lumiEle=Weight("18939")

qcd_sf = {}
qcd_sf["mu"] = {}
qcd_sf["ele"] = {}
qcd_sf["mu"]["2j1t"] = Weight("6.094")
qcd_sf["mu"]["2j0t"] = Weight("10.227")
qcd_sf["mu"]["3j1t"] = Weight("0.241")
qcd_sf["mu"]["3j2t"] = Weight("0.077")
qcd_sf["ele"]["2j1t"] = Weight("26.140")
qcd_sf["ele"]["2j0t"] = Weight("44.8777")
qcd_sf["ele"]["3j1t"] = Weight("0.311")
qcd_sf["ele"]["3j2t"] = Weight("0.218")

