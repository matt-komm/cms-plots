import os
from Weight import *

class InputSource:
    def __init__(self,folderList,weightStr="1"):
        self.folderList=folderList
        self.weight=Weight(weightStr)
        self.datafiles=[]
        self.weightfiles=[]
        

inputDict = {}

def addInput(name,folderList,weightStr="1"):
    inputDict[name]=InputSource(folderList,str(weightStr))

#signal    
addInput("tChan",["iso/nominal/T_t","iso/nominal/Tbar_t"],
    "pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight")
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


def findSampleFiles(basedir):
    for inputName in inputDict.keys():
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

