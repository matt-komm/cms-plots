import SampleBuilder
from Weight import *

class StackSource:
    def __init__(self,sampleList,weightStr="1"):
        self.sampleList=sampleList
        self.weight=Weight(weightStr)
        
        
    def getSamples(self):
        samples=[];
        for sampleName in self.sampleList:
            samples.append(SampleBuilder.sampleDict[sampleName])
        return samples
        
        

stackDict={}

def addStack(name,sampleList,weightStr="1"):
    stackDict[name]=StackSource(sampleList,str(weightStr))
    
    
addStack("MC_mu_comb",["noTop","otherTop","signal"],"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")
addStack("MC_mu_single",["other","ttbar","WJetsExclBF","WJetsExclCF","WJetsExclLF","otherST","tChan"],"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")
addStack("data_mu",["SingleMu"],"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)")


addStack("MC_ele_comb",["noTop","otherTop","signal"],"(n_signal_mu==0)*(n_signal_ele==1)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_ele==1)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")
addStack("MC_ele_single",["other","ttbar","WJetsExclBF","WJetsExclCF","WJetsExclLF","otherST","tChan"],"(n_signal_mu==0)*(n_signal_ele==1)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_ele==1)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")
addStack("data_ele",["SingleEle"],"(n_signal_mu==0)*(n_signal_ele==1)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_ele==1)")
