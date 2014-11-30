class Weight:
    def __init__(self,w):
        self.weightStr=w
        
    def __add__(self,w):
        return Weight(self.weightStr+"*"+w.weightStr)
        
    def get(self):
        return self.weightStr
        
        

c2j0t=Weight("(njets==2)*(ntags==0)")
c2j1t=Weight("(njets==2)*(ntags==1)")
c2j2t=Weight("(njets==2)*(ntags==2)")
c3j0t=Weight("(njets==2)*(ntags==0)")
c3j1t=Weight("(njets==2)*(ntags==1)")
c3j2t=Weight("(njets==2)*(ntags==2)")
c3j3t=Weight("(njets==2)*(ntags==3)")
qcd=Weight("(bdt_qcd>0.4)")
lumiMu=Weight("16872")
lumiEle=Weight("18939")
