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
    {"sets":["DY","DiBoson","WJetsExclLF","WJetsExclCF","WJetsExclBF"],
    "weight":"1.24"},
    {"sets":["sChan","tWChan","TTJetsDi","TTJetsSemi"],
    "weight":"1.1"},
    {"sets":["tChanLeptons"],
    "weight":"1.16"}
]

fitResultNuType=[
    {"sets":["DY","DiBoson","WJetsExclLF","WJetsExclCF","WJetsExclBF"],
    "weight":"((nu_soltype<0.5)*1.06+(nu_soltype>0.5)*1.32)"},
    {"sets":["sChan","tWChan","TTJetsDi","TTJetsSemi"],
    "weight":"((nu_soltype<0.5)*1.09+(nu_soltype>0.5)*1.12)"},
    {"sets":["tChanLeptons"],
    "weight":"((nu_soltype<0.5)*1.18+(nu_soltype>0.5)*1.2)"}
]

applyFitResult(setDict,fitResultNuType)

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
        "sets":["DY","DiBoson","sChan","tWChan","TTJetsDi","TTJetsSemi","WJetsExclLF","WJetsExclCF","WJetsExclBF","tChanLeptons"],
        "weights":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets==2)*(ntags==1)*(bdt_qcd>0.4)*pu_weight*xsweight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*19700"
    },  
    {
        "sets":["SingleMu"],
        "weights":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets==2)*(ntags==1)*(bdt_qcd>0.4)"
    }
]

stack3j1t_mu=[
    {
        "sets":["DY","DiBoson","sChan","tWChan","TTJetsDi","TTJetsSemi","WJetsExclLF","WJetsExclCF","WJetsExclBF","tChanLeptons"],
        "weights":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets==3)*(ntags==1)*(bdt_qcd>0.4)*pu_weight*xsweight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*19700"
    },  
    {
        "sets":["SingleMu"],
        "weights":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets==3)*(ntags==1)*(bdt_qcd>0.4)"
    }
]

stack3j2t_mu=[
    {
        "sets":["DY","DiBoson","sChan","tWChan","TTJetsDi","TTJetsSemi","WJetsExclLF","WJetsExclCF","WJetsExclBF","tChanLeptons"],
        "weights":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets==3)*(ntags==2)*(bdt_qcd>0.4)*pu_weight*xsweight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*19700"
    },  
    {
       "sets":["SingleMu"],
        "weights":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets==3)*(ntags==2)*(bdt_qcd>0.4)"
    }
]

stack2j0t_mu=[
    {
        "sets":["DY","DiBoson","sChan","tWChan","TTJetsDi","TTJetsSemi","WJetsExclLF","WJetsExclCF","WJetsExclBF","tChanLeptons"],
        "weights":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets==2)*(ntags==0)*(bdt_qcd>0.4)*pu_weight*xsweight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*19700"
    },  
    {
        "sets":["SingleMu"],
        "weights":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets==2)*(ntags==0)*(bdt_qcd>0.4)"
    }
]



if __name__=="__main__":
    for stack in stack2j1t_mu:
        stackweight=stack["weights"]
        for setName in stack["sets"]:
            print setName
            setInfo = setDict[setName]
            setweight=setInfo["weight"]
            dataFiles=setInfo["files"]
            weightFiles=setInfo["weights"]
            dataChain=ROOT.TChain("dataframe","data")
            weightChain=ROOT.TChain("dataframe","weight")
            for i in range(len(dataFiles)):
                dataChain.AddFile(dataFiles[i])
                weightChain.AddFile(weightFiles[i])
            dataChain.AddFriend(weightChain)
            
            hist = Histogram1D.projectFromTree(dataChain,"mtw",stackweight+"*"+setweight,EquiBinning(50,0,150))
            cv=Canvas()
            cv.addDrawable(hist)
            cv.draw()
            cv.wait()
            break
        break
    #hist.setStyle(HistogramStyle.createFilled(2))
    '''    


    cv=Canvas()

    histAxisStyle = CoordinateStyle()
    histAxisStyle.applyStyle(hist.GetXaxis(),hist.GetYaxis(),hist.GetXaxis(),"GeV")
    hist.Draw()
    cv.wait()
    '''
