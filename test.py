from Canvas import *
from Histogram import *
from Stack import *
from Axis import *

import os

import ROOT


def applyFitResult(setDict,fitResults):
    for res in fitResults:
        for setName in res["sets"]:
            setDict[setName]["weight"]+="*"+res["weight"]

setDict = {
    "tChan":{
        "folders":["T_t","Tbar_t"],
        "style":ROOT.kMagenta,
        "legend":{"entry":"tChan","draw":"F"},
        "weight":"1.0"
    },
    "tChanLeptons":{
        "folders":["T_t_ToLeptons","Tbar_t_ToLeptons"],
        "style":ROOT.kMagenta,
        "legend":{"entry":"tChan","draw":"F"},
        "weight":"1.0"
    },
    
    "DY":{
        "folders":["DYJets"],
        "style":ROOT.kViolet+1,
        "legend":{"entry":"DY","draw":"F"},
        "weight":"1.0"
    },
    "sChan":{
        "folders":["T_s","Tbar_s"],
        "style":ROOT.kYellow,
        "legend":{"entry":"sChan","draw":"F"},
        "weight":"1.0"
    },
    "tWChan":{
        "folders":["T_tW","Tbar_tW"],
        "style":ROOT.kYellow,
        "legend":{"entry":"tWChan","draw":"F"},
        "weight":"1."
    },
    "TTJetsDi":{
        "folders":["TTJets_FullLept"],
        "style":ROOT.kOrange+10,
        "legend":{"entry":"TTJets l+l","draw":"F"},
        "weight":"(top_weight)"
    },
    "TTJetsSemi":{
        "folders":["TTJets_SemiLept"],
        "style":ROOT.kRed,
        "legend":{"entry":"TTJets l+j","draw":"F"},
        "weight":"(top_weight)"
    },
    "TTJetsFull":{
        "folders":["TTJets_MassiveBinDECAY"],
        "style":ROOT.kOrange-3,
        "legend":{"entry":"TTJets","draw":"F"},
        "weight":"(top_weight)"
    },
    "WJetsExclBF":{
        "folders":["W1Jets_exclusive","W2Jets_exclusive","W3Jets_exclusive","W4Jets_exclusive"],
        "style":ROOT.kGreen+2,
        "legend":{"entry":"WJets Xb","draw":"F"},
        "weight":"(abs(ljet_id)==5 || abs(bjet_id)==5 || abs(sjet1_id)==5 || abs(sjet2_id)==5)"
    },
    "WJetsExclCF":{
        "folders":["W1Jets_exclusive","W2Jets_exclusive","W3Jets_exclusive","W4Jets_exclusive"],
        "style":ROOT.kGreen-4,
        "legend":{"entry":"WJets Xc","draw":"F"},
        "weight":"((abs(ljet_id)!=5 && abs(bjet_id)!=5 && abs(sjet1_id)!=5 && abs(sjet2_id)!=5) && (abs(ljet_id)==4 || abs(bjet_id)==4 || abs(sjet1_id)==4 || abs(sjet2_id)==4))"
    },
    "WJetsExclLF":{
        "folders":["W1Jets_exclusive","W2Jets_exclusive","W3Jets_exclusive","W4Jets_exclusive"],
        "style":ROOT.kTeal+2,
        "legend":{"entry":"WJets LF","draw":"F"},
        "weight":"(abs(ljet_id)!=5 && abs(bjet_id)!=5 && abs(sjet1_id)!=5 && abs(sjet2_id)!=5 && abs(ljet_id)!=4 && abs(bjet_id)!=4 && abs(sjet1_id)!=4 && abs(sjet2_id)!=4)"
    },
    "WJetsExcl":{
        "folders":["W1Jets_exclusive","W2Jets_exclusive","W3Jets_exclusive","W4Jets_exclusive"],
        "style":ROOT.kTeal+2,
        "legend":{"entry":"WJets","draw":"F"},
        "weight":"1.0"
    },
    "DiBoson":{
        "folders":["WW","WZ","ZZ"],
        "style":ROOT.kBlue,
        "legend":{"entry":"DiBoson","draw":"F"},
        "weight":"1.0"
    },
    "SingleMu":{
        "folders":["SingleMu1","SingleMu2","SingleMu3","SingleMu_miss"],
        "style":ROOT.kBlack,
        "legend":{"entry":"data","draw":"PE"},
        "weight":"1"
    },
    "SingleEle":{
        "folders":["SingleEle1","SingleEle2","SingleEle_miss"],
        "style":ROOT.kBlack,
        "legend":{"entry":"data","draw":"PE"},
        "weight":"1"
    }
}




fitResultComp=[
    {"sets":["DY","DiBoson","WJetsExclLF","WJetsExclCF","WJetsExclBF","WJetsExcl"],
    "weight":"1.24"},
    {"sets":["sChan","tWChan","TTJetsDi","TTJetsSemi"],
    "weight":"1.1"},
    {"sets":["tChanLeptons"],
    "weight":"1.16"}
]

fitResultNuType=[
    {"sets":["DY","DiBoson","WJetsExclLF","WJetsExclCF","WJetsExclBF","WJetsExcl"],
    "weight":"((nu_soltype<0.5)*1.06+(nu_soltype>0.5)*1.32)"},
    {"sets":["sChan","tWChan","TTJetsDi","TTJetsSemi"],
    "weight":"((nu_soltype<0.5)*1.09+(nu_soltype>0.5)*1.12)"},
    {"sets":["tChanLeptons"],
    "weight":"((nu_soltype<0.5)*1.18+(nu_soltype>0.5)*1.2)"}
]

applyFitResult(setDict,fitResultComp)

for sample in setDict.keys():
    setDict[sample]["files"]=[]
    setDict[sample]["weights"]=[]
    for folder in setDict[sample]["folders"]:
        path = os.path.join("/home/mkomm/Analysis/STpol/nominal",folder)
        
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith("output.root"):
                     setDict[sample]["files"].append(os.path.join(root,file))
                if file.endswith("output.root.added"):
                     setDict[sample]["weights"].append(os.path.join(root,file))
    if len(setDict[sample]["files"])==len(setDict[sample]["weights"]):
        print "found ... ",sample,"...",len(setDict[sample]["files"])," files"
    else:
        print "ERROR"

stack2j1t_mu=[
    {
        "sets":["noTop","otherTop","signal"],
        "weights":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets==2)*(ntags==1)*(bdt_qcd>0.4)*pu_weight*xsweight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*19700"
    },  
    {
        "sets":["SingleMu"],
        "weights":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets==2)*(ntags==1)*(bdt_qcd>0.4)"
    }
]

stack3j1t_mu=[
    {
        "sets":["noTop","otherTop","signal"],
        "weights":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets==3)*(ntags==1)*(bdt_qcd>0.4)*pu_weight*xsweight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*19700"
    },  
    {
        "sets":["SingleMu"],
        "weights":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets==3)*(ntags==1)*(bdt_qcd>0.4)"
    }
]

stack3j2t_mu=[
    {
        "sets":["noTop","otherTop","signal"],
        "weights":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets==3)*(ntags==2)*(bdt_qcd>0.4)*pu_weight*xsweight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*19700"
    },  
    {
       "sets":["SingleMu"],
        "weights":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets==3)*(ntags==2)*(bdt_qcd>0.4)"
    }
]

stack2j0t_mu=[
    {
        #"sets":["DY","DiBoson","sChan","tWChan","TTJetsDi","TTJetsSemi","WJetsExclLF","WJetsExclCF","WJetsExclBF","tChanLeptons"],
        "sets":["noTop","otherTop","signal"],
        "weights":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets==2)*(ntags==0)*(bdt_qcd>0.4)*pu_weight*xsweight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*19700"
    },  
    {
        "sets":["SingleMu"],
        "weights":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets==2)*(ntags==0)*(bdt_qcd>0.4)"
    }
]
'''
colorSignal=ROOT.TColor(300,1.00, 0.431, 0.027,"") 
colorNoTop=ROOT.TColor(301,0.447, 0.914, 0.0,"") 

colorOtherTop=ROOT.TColor(302,0.243, 0.322, 0.80,"") 
colorQCD=ROOT.TColor(303,0.7,0.7,0.7,"") 
'''

colorSignal=ROOT.TColor(300,0.984, 0, 0.071,"") 
colorSignalDark=ROOT.TColor(301,0.494, 0, 0.012,"") 
colorOtherTop=ROOT.TColor(302,1.00, 0.58, 0.0,"") 
colorOtherTopDark=ROOT.TColor(303,0.398, 0.24, 0,"") 
colorNoTop=ROOT.TColor(304,0.031, 0.282, 0.816,"")
colorNoTopDark=ROOT.TColor(305,0, 0.114, 0.333,"")
colorQCD=ROOT.TColor(306,0.7,0.7,0.7,"") 
colorQCDDark=ROOT.TColor(307,0.55,0.55,0.55,"") 

combinedSets={
    "signal":{
        "sets":["tChanLeptons"],
        "style":HistogramStyle.createFilled(colorSignal.GetNumber(),colorSignalDark.GetNumber()),
        "legend":"t-chan. single top"
    },
    "otherTop":{
        "sets":["sChan","tWChan","TTJetsDi","TTJetsSemi"],
        "style":HistogramStyle.createFilled(colorOtherTop.GetNumber(),colorOtherTopDark.GetNumber()),
        "legend":"other top"
    },
    "noTop":{
        "sets":["DY","DiBoson","WJetsExcl"],
        "style":HistogramStyle.createFilled(colorNoTop.GetNumber(),colorNoTopDark.GetNumber()),
        "legend":"non resonant top"
    },
    "SingleMu":{
        "sets":["SingleMu"],
        "style":HistogramStyle.createMarkers(),
        "legend":"data"
    },
    "SingleEle":{
        "sets":["SingleEle"],
        "style":HistogramStyle.createMarkers(),
        "legend":"data"
    }
    
}




if __name__=="__main__":
    binning = EquiBinning(30,0,200)
    cv=Canvas()
    cv.setCoordinateStyle(CoordinateStyle(xtitle="MTW",ytitle="Events",unit="GeV",unitBinning=binning))
    
    
    for stackInfo in stack2j1t_mu:
        stackweight=stackInfo["weights"]
        stack=Stack()
        for setName in stackInfo["sets"]:
            setHist=Histogram1D.createEmpty(binning)
            setHist.setStyle(combinedSets[setName]["style"])
            for singleSet in combinedSets[setName]["sets"]:
                print singleSet
                setInfo = setDict[singleSet]
                setweight=setInfo["weight"]
                dataFiles=setInfo["files"]
                weightFiles=setInfo["weights"]
                dataChain=ROOT.TChain("dataframe","data")
                weightChain=ROOT.TChain("dataframe","weight")
                for i in range(len(dataFiles)):
                    dataChain.AddFile(dataFiles[i])
                    weightChain.AddFile(weightFiles[i])
                dataChain.AddFriend(weightChain)
                
                temp = Histogram1D.projectFromTree(dataChain,"mtw",stackweight+"*"+setweight+"*(bdt_sig_bg>0.6)",binning)
                setHist.addHistogram(temp)
                
            stack.addHistogram(setHist)
            
        
        cv.addDrawable(stack)
        
    cv.draw()
    cv.wait()
    #hist.setStyle(HistogramStyle.createFilled(2))
    '''    


    cv=Canvas()

    histAxisStyle = CoordinateStyle()
    histAxisStyle.applyStyle(hist.GetXaxis(),hist.GetYaxis(),hist.GetXaxis(),"GeV")
    hist.Draw()
    cv.wait()
    '''
