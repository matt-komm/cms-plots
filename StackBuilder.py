import SampleBuilder
from Weight import *

class StackSource:
    def __init__(self,name,sampleList,weightStr="1"):
        self.name=name
        self.sampleList=sampleList
        self.weight=Weight(weightStr)
        
        
    def getSamples(self):
        samples=[];
        for sampleName in self.sampleList:
            samples.append(SampleBuilder.sampleDict[sampleName])
        return samples
        
        

stackDict={}

def addStack(name,sampleList,weightStr="1"):
    stackDict[name]=StackSource(name,sampleList,str(weightStr))
    
    
addStack("ttonly",["ttbarSemi"],"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(ljet_dr>0.3)*(bjet_dr>0.3)")
    
addStack("MC_mu_comb",["QCDMu","noTop","otherTop","signal"],"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(ljet_dr>0.3)*(bjet_dr>0.3)")
addStack("MC_mu_single",reversed(["QCDMu","other","ttbar","WJetsExclBF","WJetsExclCF","WJetsExclLF","otherST","tChan"]),"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(ljet_dr>0.3)*(bjet_dr>0.3)")
addStack("MC_mu_fit",reversed(["QCDMu","other","ttbar","WJetsExcl","otherST","tChan"]),"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(ljet_dr>0.3)*(bjet_dr>0.3)")

#addStack("MC_mu_single",reversed(["other","ttbar","WJetsExclBF","WJetsExclCF","WJetsExclLF","otherST","tChan"]),"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(ljet_dr>0.3)*(bjet_dr>0.3)")

addStack("data_mu",["SingleMu"],"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(ljet_dr>0.3)*(bjet_dr>0.3)")


addStack("MC_ele_comb",["QCDEle","noTop","otherTop","signal"],"(n_signal_mu==0)*(n_signal_ele==1)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_ele==1)*(ljet_dr>0.3)*(bjet_dr>0.3)")
addStack("MC_ele_single",reversed(["QCDEle","other","ttbar","WJetsExclBF","WJetsExclCF","WJetsExclLF","otherST","tChan"]),"(n_signal_mu==0)*(n_signal_ele==1)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_ele==1)*(ljet_dr>0.3)*(bjet_dr>0.3)")
addStack("MC_ele_fit",reversed(["QCDEle","other","ttbar","WJetsExcl","otherST","tChan"]),"(n_signal_mu==0)*(n_signal_ele==1)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_ele==1)*(ljet_dr>0.3)*(bjet_dr>0.3)")
addStack("data_ele",["SingleEle"],"(n_signal_mu==0)*(n_signal_ele==1)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_ele==1)*(ljet_dr>0.3)*(bjet_dr>0.3)")
