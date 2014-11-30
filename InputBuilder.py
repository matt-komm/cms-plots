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
addInput("tChan",["iso/nominal/T_t","iso/nominal/Tbar_t"])
addInput("tChanLeptons",["iso/nominal/T_t_ToLeptons","iso/nominal/Tbar_t_ToLeptons"])

#other top
addInput("sChan",["iso/nominal/T_s","iso/nominal/Tbar_s"])
addInput("tWChan",["iso/nominal/T_tW","iso/nominal/Tbar_tW"])
addInput("TTJetsDi",["iso/nominal/TTJets_FullLept"])
addInput("TTJetsSemi",["iso/nominal/TTJets_SemiLept"])
addInput("TTJetsFull",["iso/nominal/TTJets_MassiveBinDECAY"])

#EWK
addInput("DY",["iso/nominal/DYJets"])
addInput("DiBoson",["iso/nominal/WW","iso/nominal/WZ","iso/nominal/ZZ"])

wjetsFolders=["iso/nominal/W1JetsToLNu","iso/nominal/W2JetsToLNu2","iso/nominal/W3JetsToLNu2","iso/nominal/W4JetsToLNu2"]
addInput("WJetsExclBF",wjetsFolders,"(abs(ljet_id)==5 || abs(bjet_id)==5 || abs(sjet1_id)==5 || abs(sjet2_id)==5)")
addInput("WJetsExclCF",wjetsFolders,"((abs(ljet_id)!=5 && abs(bjet_id)!=5 && abs(sjet1_id)!=5 && abs(sjet2_id)!=5) && (abs(ljet_id)==4 || abs(bjet_id)==4 || abs(sjet1_id)==4 || abs(sjet2_id)==4))")
addInput("WJetsExclLF",wjetsFolders,"(abs(ljet_id)!=5 && abs(bjet_id)!=5 && abs(sjet1_id)!=5 && abs(sjet2_id)!=5 && abs(ljet_id)!=4 && abs(bjet_id)!=4 && abs(sjet1_id)!=4 && abs(sjet2_id)!=4)")
addInput("WJetsExcl",wjetsFolders)

#data
addInput("SingleMu",["iso/data/SingleMu"])
addInput("SingleEle",["iso/data/SingleEle"])

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

