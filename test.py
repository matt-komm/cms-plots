from Canvas import *
from Histogram import *
from Stack import *
from Axis import *
from InfoText import *
from Position import *

import os, sys

import ROOT
ROOT.gSystem.Load("libpowerlib.so")

def applyFitResult(setDict,fitResults):
    for res in fitResults:
        for setName in res["sets"]:
            setDict[setName]["weight"]+="*"+res["weight"]

setDict = {
    "tChan":{
        "folders":["iso/nominal/T_t","iso/nominal/Tbar_t"],
        "style":ROOT.kMagenta,
        "legend":{"entry":"tChan","draw":"F"},
        "weight":"xsweight"
    },
    "tChanLeptons":{
        "folders":["iso/nominal/T_t_ToLeptons","iso/nominal/Tbar_t_ToLeptons"],
        "style":ROOT.kMagenta,
        "legend":{"entry":"tChan","draw":"F"},
        "weight":"xsweight"
    },
    
    "DY":{
        "folders":["iso/nominal/DYJets"],
        "style":ROOT.kViolet+1,
        "legend":{"entry":"DY","draw":"F"},
        "weight":"xsweight"
    },
    "sChan":{
        "folders":["iso/nominal/T_s","iso/nominal/Tbar_s"],
        "style":ROOT.kYellow,
        "legend":{"entry":"sChan","draw":"F"},
        "weight":"xsweight"
    },
    "tWChan":{
        "folders":["iso/nominal/T_tW","iso/nominal/Tbar_tW"],
        "style":ROOT.kYellow,
        "legend":{"entry":"tWChan","draw":"F"},
        "weight":"xsweight"
    },
    "TTJetsDi":{
        "folders":["iso/nominal/TTJets_FullLept"],
        "style":ROOT.kOrange+10,
        "legend":{"entry":"TTJets l+l","draw":"F"},
        "weight":"(top_weight*xsweight)"
    },
    "TTJetsSemi":{
        "folders":["iso/nominal/TTJets_SemiLept"],
        "style":ROOT.kRed,
        "legend":{"entry":"TTJets l+j","draw":"F"},
        "weight":"(top_weight*xsweight)"
    },
    "TTJetsFull":{
        "folders":["iso/nominal/TTJets_MassiveBinDECAY"],
        "style":ROOT.kOrange-3,
        "legend":{"entry":"TTJets","draw":"F"},
        "weight":"(top_weight*xsweight)"
    },
    "WJetsExclBF":{
        "folders":["iso/nominal/W1JetsToLNu","iso/nominal/W2JetsToLNu","iso/nominal/W3JetsToLNu","iso/nominal/W4JetsToLNu"],
        "style":ROOT.kGreen+2,
        "legend":{"entry":"WJets Xb","draw":"F"},
        "weight":"(abs(ljet_id)==5 || abs(bjet_id)==5 || abs(sjet1_id)==5 || abs(sjet2_id)==5)"
    },
    "WJetsExclCF":{
        "folders":["iso/nominal/W1JetsToLNu","iso/nominal/W2JetsToLNu","iso/nominal/W3JetsToLNu","iso/nominal/W4JetsToLNu"],
        "style":ROOT.kGreen-4,
        "legend":{"entry":"WJets Xc","draw":"F"},
        "weight":"((abs(ljet_id)!=5 && abs(bjet_id)!=5 && abs(sjet1_id)!=5 && abs(sjet2_id)!=5) && (abs(ljet_id)==4 || abs(bjet_id)==4 || abs(sjet1_id)==4 || abs(sjet2_id)==4))"
    },
    "WJetsExclLF":{
        "folders":["iso/nominal/W1JetsToLNu","iso/nominal/W2JetsToLNu","iso/nominal/W3JetsToLNu","iso/nominal/W4JetsToLNu"],
        "style":ROOT.kTeal+2,
        "legend":{"entry":"WJets LF","draw":"F"},
        "weight":"(abs(ljet_id)!=5 && abs(bjet_id)!=5 && abs(sjet1_id)!=5 && abs(sjet2_id)!=5 && abs(ljet_id)!=4 && abs(bjet_id)!=4 && abs(sjet1_id)!=4 && abs(sjet2_id)!=4)"
    },
    "WJetsExcl":{
        "folders":["iso/nominal/W1JetsToLNu","iso/nominal/W2JetsToLNu2","iso/nominal/W3JetsToLNu2","iso/nominal/W4JetsToLNu2"],
        "style":ROOT.kTeal+2,
        "legend":{"entry":"WJets","draw":"F"},
        "weight":"xsweight"
    },
    "WJetsExcl1":{
        "folders":["iso/nominal/W1JetsToLNu"],
        "style":ROOT.kTeal+2,
        "legend":{"entry":"WJets","draw":"F"},
        "weight":"0.0003464"
    },
    "WJetsExcl2":{
        "folders":["iso/nominal/W2JetsToLNu"],
        "style":ROOT.kTeal+2,
        "legend":{"entry":"WJets","draw":"F"},
        "weight":"3.559e-05"
    },
    "WJetsExcl3":{
        "folders":["iso/nominal/W3JetsToLNu"],
        "style":ROOT.kTeal+2,
        "legend":{"entry":"WJets","draw":"F"},
        "weight":"2.695e-05"
    },
    "WJetsExcl4":{
        "folders":["iso/nominal/W4JetsToLNu"],
        "style":ROOT.kTeal+2,
        "legend":{"entry":"WJets","draw":"F"},
        "weight":"1.313e-05"
    },
    "DiBoson":{
        "folders":["iso/nominal/WW","iso/nominal/WZ","iso/nominal/ZZ"],
        "style":ROOT.kBlue,
        "legend":{"entry":"DiBoson","draw":"F"},
        "weight":"xsweight"
    },
    "SingleMu":{
        "folders":["iso/data/SingleMu"],
        "style":ROOT.kBlack,
        "legend":{"entry":"data","draw":"PE"},
        "weight":"1"
    },
    "SingleEle":{
        "folders":["iso/data/SingleEle"],
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

#applyFitResult(setDict,fitResultComp)

for sample in setDict.keys():
    setDict[sample]["files"]=[]
    setDict[sample]["weights"]=[]
    for folder in setDict[sample]["folders"]:
        path = os.path.join("/home/mkomm/Analysis/STpol/Oct28_reproc_v5",folder)
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".root") and file.find("output")!=-1:
                     setDict[sample]["files"].append(os.path.join(root,file))
                if file.endswith(".root.added") and file.find("output")!=-1:
                     setDict[sample]["weights"].append(os.path.join(root,file))
    if len(setDict[sample]["files"])==len(setDict[sample]["weights"]):
        print "found ... ",sample,"...",len(setDict[sample]["files"])," files"
    else:
        print "ERROR"
    setDict[sample]["files"]=sorted(setDict[sample]["files"])
    setDict[sample]["weights"]=sorted(setDict[sample]["weights"])
        
lumiMu="16872"
lumiEle="18939"



stack2j1t_ele=[
    {
        "sets":["noTop","otherTop","signal"],
        "weights":"(n_signal_mu==0)*(n_signal_ele==1)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_ele==1)*(njets==2)*(ntags==1)*(bdt_qcd>0.4)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*"+lumiEle
    },  
    {
        "sets":["SingleEle"],
        "weights":"(n_signal_mu==0)*(n_signal_ele==1)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_ele==1)*(njets==2)*(ntags==1)*(bdt_qcd>0.4)"
    }
]

stack3j1t_mu=[
    {
        "sets":["noTop","otherTop","signal"],
        "weights":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets==3)*(ntags==1)*(bdt_qcd>0.4)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*"+lumiMu
    },  
    {
        "sets":["SingleMu"],
        "weights":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets==3)*(ntags==1)*(bdt_qcd>0.4)"
    }
]

stack3j2t_mu=[
    {
        "sets":["noTop","otherTop","signal"],
        "weights":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets==3)*(ntags==2)*(bdt_qcd>0.4)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*"+lumiMu
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
        "weights":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets==2)*(ntags==0)*(bdt_qcd>0.4)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*"+lumiMu
    },  
    {
        "sets":["SingleMu"],
        "weights":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets==2)*(ntags==0)*(bdt_qcd>0.4)"
    }
]    
stack_mu=[
    {
        #"sets":["DY","DiBoson","sChan","tWChan","TTJetsDi","TTJetsSemi","WJetsExclLF","WJetsExclCF","WJetsExclBF","tChanLeptons"],
        "sets":["noTop","otherTop","signal"],
        "weights":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets>=2)*(ntags>=0)*(bdt_qcd>0.4)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*"+lumiMu
    },  
    {
        "sets":["SingleMu"],
        "weights":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets>=2)*(ntags>=0)*(bdt_qcd>0.4)"
    }
]

'''
colorSignal=ROOT.TColor(300,0.984, 0, 0.071,"") 
colorOtherTop=ROOT.TColor(302,1.00, 0.58, 0.0,"") 
colorNoTop=ROOT.TColor(304,0.031, 0.282, 0.816,"")
colorQCD=ROOT.TColor(306,0.7,0.7,0.7,"") 
'''

'''
colorSignal=ROOT.TColor(300,1.00, 0.192, 0,"") 
colorOtherTop=ROOT.TColor(302,1.00, 0.839, 0,"") 
colorNoTop=ROOT.TColor(304,0.463, 0.149, 0.859,"")
colorQCD=ROOT.TColor(306,0.7,0.7,0.7,"") 
'''


colorSignal=ROOT.TColor(300,236/255.0,208/255.0,120/255.0,"") 
colorOtherTop=ROOT.TColor(302,192/255.0,41/255.0,66/255.0,"") 
colorNoTop=ROOT.TColor(304,83/255.0,119/255.0,122/255.0,"")
colorQCD=ROOT.TColor(306,0.7,0.7,0.7,"") 


colorSignalDark=ROOT.TColor(301,colorSignal.GetRed()*0.5, colorSignal.GetGreen()*0.5, colorSignal.GetBlue()*0.5,"") 
colorOtherTopDark=ROOT.TColor(303,colorOtherTop.GetRed()*0.5, colorOtherTop.GetGreen()*0.5, colorOtherTop.GetBlue()*0.5,"") 
colorNoTopDark=ROOT.TColor(305,colorNoTop.GetRed()*0.5, colorNoTop.GetGreen()*0.5, colorNoTop.GetBlue()*0.5,"")
colorQCDDark=ROOT.TColor(307,colorQCD.GetRed()*0.5, colorQCD.GetGreen()*0.5, colorQCD.GetBlue()*0.5,"")

combinedSets={
    "signal":{
        "sets":["tChanLeptons"],
        "style":HistogramStyle.createFilled(colorSignal.GetNumber(),colorSignalDark.GetNumber()),
        "legend":LegendEntry(title="SM signal",drawOptions="F",priority=0)
    },
    "otherTop":{
        "sets":["sChan","tWChan","TTJetsDi","TTJetsSemi"],
        "style":HistogramStyle.createFilled(colorOtherTop.GetNumber(),colorOtherTopDark.GetNumber()),
        "legend":LegendEntry(title="other top",drawOptions="F",priority=0)
    },
    "noTop":{
        "sets":["DY","DiBoson","WJetsExcl"],
        "style":HistogramStyle.createFilled(colorNoTop.GetNumber(),colorNoTopDark.GetNumber()),
        "legend":LegendEntry(title="EWK",drawOptions="F",priority=0)
    },
    "SingleMu":{
        "sets":["SingleMu"],
        "style":HistogramStyle.createMarkers(),
        "legend":LegendEntry(title="data",drawOptions="PE",priority=10)
    },
    "SingleEle":{
        "sets":["SingleEle"],
        "style":HistogramStyle.createMarkers(),
        "legend":LegendEntry(title="data",drawOptions="PE",priority=10)
    }
    
}

#sys.exit(0)


if __name__=="__main__":
    '''
    h = Histogram1D.createFromSearchInFile("/home/mkomm/Analysis/STpol/bdt_scan/hists/preselection/2j_1t/mu/abs_ljet_eta.root",
        ["*T_t_ToLeptons__iso"]
    
    )
    cv=ROOT.TCanvas("cv","",800,600)
    h.getRootHistogram().Draw()
    cv.WaitPrimitive()
    '''
    #ROOT.gROOT.SetBatch(True)
    binning = EquiBinning(80,0.0,200)
    cv=CanvasResiduen()
    #cv=Canvas()
    cv.setCoordinateStyle(CoordinateStyle(xtitle="MTW",unit="GeV",ytitle="Events",unitBinning=binning))
    
    stackList=[]
    legend=Legend(position=Position.Legend.RIGHT_STACKED)
    for stackInfo in stack2j1t_ele:
        stackweight=stackInfo["weights"]
        stack=Stack()
        stackList.append(stack)
        for setName in stackInfo["sets"]:
            setHist=Histogram1D.createEmpty(binning)
            setHist.setStyle(combinedSets[setName]["style"])
            legendEntry=combinedSets[setName]["legend"]
            legendEntry.rootObj=setHist.getRootHistogram()
            legend.addEntry(legendEntry)
            
            
            for singleSet in combinedSets[setName]["sets"]:
                
                setInfo = setDict[singleSet]
                setweight=setInfo["weight"]
                dataFiles=setInfo["files"]
                weightFiles=setInfo["weights"]
                
                #openedFiles=[]
                #projectionGroup = ROOT.ProjectionGroup(setHist.getRootHistogram())
                for i in range(len(dataFiles)):
                    sys.stdout.write('%s: %i/%i\r' % (singleSet,i+1,len(dataFiles)))
                    sys.stdout.flush()
                    p = ROOT.Projector(setHist.getRootHistogram(), dataFiles[i], "dataframe", "mtw", stackweight+"*"+setweight);
                    p.addFriend(weightFiles[i],"dataframe")
                    p.Project()
                print
                #projectionGroup.Project(4)
            stack.addHistogram(setHist)
            
        
        cv.addDrawable(stack)
    cv.addDrawable(legend)
    cv.addDrawable(InfoText.createCMSText(orientation=InfoText.STACKED,position=Position.CMSText.RIGHT_STACKED))
    cv.addDrawable(InfoText.createLumiText())
    
    
    dataResHist=stackList[1].getSum()
    dataResHist.divideHistogram(stackList[0].getSum())
    dataResHist.setStyle(HistogramStyle.createMarkers())
    cv.addResiduen(dataResHist)
    
    cv.draw()
    cv.wait()
    #hist.setStyle(HistogramStyle.createFilled(2))
    
