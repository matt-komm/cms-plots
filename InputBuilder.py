import os
import copy
from Weight import *

class InputSource:
    def __init__(self,name,folderList,weightStr="1"):
        self.name=name
        self.folderList=folderList
        self.weight=Weight(weightStr)
        self.datafiles=[]
        self.weightfiles=[]
        

inputDict = {}

def addInput(name,folderList,weightStr="1"):
    inputDict[name]=InputSource(name,folderList,str(weightStr))
    
def cloneInputs(nameList,postFix):
    for name in nameList:
        inputDict[name+postFix]=copy.deepcopy(inputDict[name])

#signal    
addInput("tChanLeptons",["iso/nominal/T_t_ToLeptons","iso/nominal/Tbar_t_ToLeptons"],
    "pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")

#other top
addInput("sChan",["iso/nominal/T_s","iso/nominal/Tbar_s"],
    "pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")
addInput("tWChan",["iso/nominal/T_tW","iso/nominal/Tbar_tW"],
    "pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")
addInput("TTJetsDi",["iso/nominal/TTJets_FullLept"],
    "top_weight*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")
addInput("TTJetsSemi",["iso/nominal/TTJets_SemiLept"],
    "top_weight*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")
addInput("TTJetsFull",["iso/nominal/TTJets_MassiveBinDECAY"],
    "top_weight*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")

#EWK
addInput("DY",["iso/nominal/DYJets"],
    "pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")
addInput("DiBoson",["iso/nominal/WW","iso/nominal/WZ","iso/nominal/ZZ"],
    "pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")

wjetsFolders=["iso/nominal/W1JetsToLNu","iso/nominal/W2JetsToLNu2","iso/nominal/W3JetsToLNu2","iso/nominal/W4JetsToLNu2"]
addInput("WJetsExclBF",wjetsFolders,
    "(abs(ljet_id)==5 || abs(bjet_id)==5 || abs(sjet1_id)==5 || abs(sjet2_id)==5)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")
addInput("WJetsExclCF",wjetsFolders,
    "((abs(ljet_id)!=5 && abs(bjet_id)!=5 && abs(sjet1_id)!=5 && abs(sjet2_id)!=5) && (abs(ljet_id)==4 || abs(bjet_id)==4 || abs(sjet1_id)==4 || abs(sjet2_id)==4))*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")
addInput("WJetsExclLF",wjetsFolders,
    "(abs(ljet_id)!=5 && abs(bjet_id)!=5 && abs(sjet1_id)!=5 && abs(sjet2_id)!=5 && abs(ljet_id)!=4 && abs(bjet_id)!=4 && abs(sjet1_id)!=4 && abs(sjet2_id)!=4)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")
addInput("WJetsExcl",wjetsFolders,
    "pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")

#data
addInput("SingleMu",["iso/data/SingleMu"])
addInput("SingleEle",["iso/data/SingleEle"])

#anti iso data
addInput("AntiIsoSingleMu",["antiiso/data/SingleMu"],"(1.0/("+lumiMu.get()+"))")
addInput("AntiIsoSingleEle",["antiiso/data/SingleEle"],"(1.0/("+lumiEle.get()+"))")

#anti iso mc
addInput("AntiIsotChanLeptons",["antiiso/nominal/T_t_ToLeptons","antiiso/nominal/Tbar_t_ToLeptons"],"(-1)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")
addInput("AntiIsosChan",["antiiso/nominal/T_s","antiiso/nominal/Tbar_s"],"(-1)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")
addInput("AntiIsotWChan",["antiiso/nominal/T_tW","antiiso/nominal/Tbar_tW"],"(-1)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")
addInput("AntiIsoTTJetsDi",["antiiso/nominal/TTJets_FullLept"],"(-1*top_weight)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")
addInput("AntiIsoTTJetsSemi",["antiiso/nominal/TTJets_SemiLept"],"(-1*top_weight)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")
addInput("AntiIsoDY",["antiiso/nominal/DYJets"],"(-1)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")
addInput("AntiIsoDiBoson",["antiiso/nominal/WW","antiiso/nominal/WZ","antiiso/nominal/ZZ"],"(-1)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")
wjetsFolders=["antiiso/nominal/W1JetsToLNu","antiiso/nominal/W2JetsToLNu2","antiiso/nominal/W3JetsToLNu2","antiiso/nominal/W4JetsToLNu2"]
addInput("AntiIsoWJetsExcl",wjetsFolders,"(-1)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")


##### create systematic variations


#Qscale t-channel
cloneInputs(["tChanLeptons","sChan","tWChan","WJetsExclBF","WJetsExclCF","WJetsExclLF","WJetsExcl","TTJetsDi","TTJetsSemi","TTJetsFull","DY","DiBoson"],
    "__qscale_tch__plus"
)
inputDict["tChanLeptons__qscale_tch__plus"].folderList=["iso/SYST/T_t_ToLeptons_scaleup","iso/SYST/Tbar_t_ToLeptons_scaleup"]

cloneInputs(["tChanLeptons","sChan","tWChan","WJetsExclBF","WJetsExclCF","WJetsExclLF","WJetsExcl","TTJetsDi","TTJetsSemi","TTJetsFull","DY","DiBoson"],
    "__qscale_tch__minus"
)
inputDict["tChanLeptons__qscale_tch__minus"].folderList=["iso/SYST/T_t_ToLeptons_scaledown","iso/SYST/Tbar_t_ToLeptons_scaledown"]




#Qscale ttbar
cloneInputs(["tChanLeptons","sChan","tWChan","WJetsExclBF","WJetsExclCF","WJetsExclLF","WJetsExcl","TTJetsDi","TTJetsSemi","TTJetsFull","DY","DiBoson"],
    "__qscale_ttbar__plus"
)
inputDict["TTJetsSemi__qscale_ttbar__plus"].folderList=["iso/SYST/TTJets_scaleup"]
inputDict["TTJetsDi__qscale_ttbar__plus"].folderList=[]

cloneInputs(["tChanLeptons","sChan","tWChan","WJetsExclBF","WJetsExclCF","WJetsExclLF","WJetsExcl","TTJetsDi","TTJetsSemi","TTJetsFull","DY","DiBoson"],
    "__qscale_ttbar__minus"
)
inputDict["TTJetsSemi__qscale_ttbar__minus"].folderList=["iso/SYST/TTJets_scaledown"]
inputDict["TTJetsDi__qscale_ttbar__minus"].folderList=[]





#Qscale Wjets
cloneInputs(["tChanLeptons","sChan","tWChan","WJetsExclBF","WJetsExclCF","WJetsExclLF","WJetsExcl","TTJetsDi","TTJetsSemi","TTJetsFull","DY","DiBoson"],
    "__qscale_wjets__plus"
)
inputDict["WJetsExcl__qscale_wjets__plus"].folderList=["iso/SYST/W1JetsToLNu_scaleup","iso/SYST/W2JetsToLNu_scaleup","iso/SYST/W3JetsToLNu_scaleup","iso/SYST/W4JetsToLNu_scaleup"]
inputDict["WJetsExclBF__qscale_wjets__plus"].folderList=["iso/SYST/W1JetsToLNu_scaleup","iso/SYST/W2JetsToLNu_scaleup","iso/SYST/W3JetsToLNu_scaleup","iso/SYST/W4JetsToLNu_scaleup"]
inputDict["WJetsExclCF__qscale_wjets__plus"].folderList=["iso/SYST/W1JetsToLNu_scaleup","iso/SYST/W2JetsToLNu_scaleup","iso/SYST/W3JetsToLNu_scaleup","iso/SYST/W4JetsToLNu_scaleup"]
inputDict["WJetsExclLF__qscale_wjets__plus"].folderList=["iso/SYST/W1JetsToLNu_scaleup","iso/SYST/W2JetsToLNu_scaleup","iso/SYST/W3JetsToLNu_scaleup","iso/SYST/W4JetsToLNu_scaleup"]

cloneInputs(["tChanLeptons","sChan","tWChan","WJetsExclBF","WJetsExclCF","WJetsExclLF","WJetsExcl","TTJetsDi","TTJetsSemi","TTJetsFull","DY","DiBoson"],
    "__qscale_wjets__minus"
)
inputDict["WJetsExcl__qscale_wjets__minus"].folderList=["iso/SYST/W1JetsToLNu_scaledown","iso/SYST/W2JetsToLNu_scaledown","iso/SYST/W3JetsToLNu_scaledown","iso/SYST/W4JetsToLNu_scaledown"]
inputDict["WJetsExclBF__qscale_wjets__minus"].folderList=["iso/SYST/W1JetsToLNu_scaledown","iso/SYST/W2JetsToLNu_scaledown","iso/SYST/W3JetsToLNu_scaledown","iso/SYST/W4JetsToLNu_scaledown"]
inputDict["WJetsExclCF__qscale_wjets__minus"].folderList=["iso/SYST/W1JetsToLNu_scaledown","iso/SYST/W2JetsToLNu_scaledown","iso/SYST/W3JetsToLNu_scaledown","iso/SYST/W4JetsToLNu_scaledown"]
inputDict["WJetsExclLF__qscale_wjets__minus"].folderList=["iso/SYST/W1JetsToLNu_scaledown","iso/SYST/W2JetsToLNu_scaledown","iso/SYST/W3JetsToLNu_scaledown","iso/SYST/W4JetsToLNu_scaledown"]




#top mass
cloneInputs(["tChanLeptons","sChan","tWChan","WJetsExclBF","WJetsExclCF","WJetsExclLF","WJetsExcl","TTJetsDi","TTJetsSemi","TTJetsFull","DY","DiBoson"],
    "__top_mass__plus"
)
inputDict["TTJetsSemi__top_mass__plus"].folderList=["iso/SYST/TTJets_mass175_5"]
inputDict["TTJetsDi__top_mass__plus"].folderList=[]
inputDict["tChanLeptons__top_mass__plus"].folderList=["T_t_ToLeptons_mass175_5","Tbar_t_ToLeptons_mass175_5"]
cloneInputs(["tChanLeptons","sChan","tWChan","WJetsExclBF","WJetsExclCF","WJetsExclLF","WJetsExcl","TTJetsDi","TTJetsSemi","TTJetsFull","DY","DiBoson"],
    "__top_mass__minus"
)
inputDict["TTJetsSemi__top_mass__minus"].folderList=["iso/SYST/TTJets_mass169_5"]
inputDict["TTJetsDi__top_mass__minus"].folderList=[]
inputDict["tChanLeptons__top_mass__minus"].folderList=["T_t_ToLeptons_mass169_5","Tbar_t_ToLeptons_mass169_5"]


#wjets shape, hf,lf
#...

#top pt
cloneInputs(["tChanLeptons","sChan","tWChan","WJetsExclBF","WJetsExclCF","WJetsExclLF","WJetsExcl","TTJetsDi","TTJetsSemi","TTJetsFull","DY","DiBoson"],
    "__top_pt__plus"
)
inputDict["TTJetsDi__top_pt__plus"].weight*=Weight("top_weight__up/top_weight")
inputDict["TTJetsSemi__top_pt__plus"].weight*=Weight("top_weight__up/top_weight")
inputDict["TTJetsFull__top_pt__plus"].weight*=Weight("top_weight__up/top_weight")

cloneInputs(["tChanLeptons","sChan","tWChan","WJetsExclBF","WJetsExclCF","WJetsExclLF","WJetsExcl","TTJetsDi","TTJetsSemi","TTJetsFull","DY","DiBoson"],
    "__top_pt__minus"
)
inputDict["TTJetsDi__top_pt__minus"].weight*=Weight("top_weight__down/top_weight")
inputDict["TTJetsSemi__top_pt__minus"].weight*=Weight("top_weight__down/top_weight")
inputDict["TTJetsFull__top_pt__minus"].weight*=Weight("top_weight__down/top_weight")



#wjets matching

#ttbar matching

#PDF
#...

#JES
#...





def findSampleFiles(basedir):
    for inputName in sorted(inputDict.keys()):
        inputDict[inputName].files=[]
        inputDict[inputName].weights=[]
        for folder in inputDict[inputName].folderList:
            path = os.path.join(basedir,folder)
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith(".root") and file.find("output")!=-1:
                         inputDict[inputName].datafiles.append(os.path.join(root,file))
                    if file.endswith(".root.added") and file.find("output")!=-1:
                         inputDict[inputName].weightfiles.append(os.path.join(root,file))
        if len(inputDict[inputName].datafiles)==len(inputDict[inputName].weightfiles):
            print "found ... ",inputName,"...",len(inputDict[inputName].datafiles)," files"
        else:
            print "ERROR"
        inputDict[inputName].datafiles=sorted(inputDict[inputName].datafiles)
        inputDict[inputName].weightfiles=sorted(inputDict[inputName].weightfiles)
        

