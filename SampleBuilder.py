import ROOT

import InputBuilder
from Histogram import *
from Style import *
from Weight import *

class SampleSource:
    def __init__(self,inputList,histStyle,legendEntry, weightStr="1"):
        self.inputList=inputList
        self.histStyle=histStyle
        self.legendEntry=legendEntry
        self.weight=Weight(weightStr)
        
        
    def getInputs(self):
        inputs=[];
        for inputName in self.inputList:
            inputs.append(InputBuilder.inputDict[inputName])
        return inputs

sampleDict={}

def addSample(name,inputList,histStyle,legendEntry, weightStr="1"):
    sampleDict[name]=SampleSource(inputList,histStyle,legendEntry,str(weightStr))
    
#--------- 4 components --------------------
addSample("signal",
    ["tChanLeptons"],
    HistogramStyle.createFilled(newColor(236/255.0,208/255.0,120/255.0)),
    LegendEntry(title="SM signal",drawOptions="F",priority=0),
)

addSample("otherTop",
    ["sChan","tWChan","TTJetsDi","TTJetsSemi"],
    HistogramStyle.createFilled(newColor(192/255.0,41/255.0,66/255.0)),
    LegendEntry(title="other top",drawOptions="F",priority=0),
)

addSample(
    "noTop",
    ["DY","DiBoson","WJetsExcl"],
    HistogramStyle.createFilled(newColor(83/255.0,119/255.0,122/255.0)),
    LegendEntry(title="EWK",drawOptions="F",priority=0)
)



addSample(
    "QCDMu",
    ["AntiIsoSingleMu","AntiIsotChanLeptons","AntiIsosChan",
    "AntiIsotWChan","AntiIsoTTJetsDi","AntiIsoTTJetsSemi",
    "AntiIsoDY","AntiIsoDiBoson","AntiIsoWJetsExcl"],
    HistogramStyle.createFilled(newColor(0.65,0.65,0.65)),
    LegendEntry(title="QCD",drawOptions="F",priority=0),
    ((c2j0t*qcd_sf["mu"]["2j0t"])+(c2j1t*qcd_sf["mu"]["2j1t"])+(c3j1t*qcd_sf["mu"]["3j1t"])+(c3j2t*qcd_sf["mu"]["3j2t"])).get()
)

addSample(
    "QCDEle",
    ["AntiIsoSingleEle","AntiIsotChanLeptons","AntiIsosChan",
    "AntiIsotWChan","AntiIsoTTJetsDi","AntiIsoTTJetsSemi",
    "AntiIsoDY","AntiIsoDiBoson","AntiIsoWJetsExcl"],
    HistogramStyle.createFilled(newColor(0.65,0.65,0.65)),
    LegendEntry(title="QCD",drawOptions="F",priority=0),
    ((c2j0t*qcd_sf["ele"]["2j0t"])+(c2j1t*qcd_sf["ele"]["2j1t"])+(c3j1t*qcd_sf["ele"]["3j1t"])+(c3j2t*qcd_sf["ele"]["3j2t"])).get()
)

#--------- more components --------------------

addSample("tChan",
    ["tChanLeptons"],
    HistogramStyle.createFilled(newColor(1.0,0.0,0.7)),
    LegendEntry(title="t-ch.",drawOptions="F",priority=0),
)

addSample("otherST",
    ["sChan","tWChan"],
    HistogramStyle.createFilled(newColor(0.55,0.0,0.25)),
    LegendEntry(title="s+tW",drawOptions="F",priority=0),
)

addSample("ttbar",
    ["TTJetsDi","TTJetsSemi"],
    HistogramStyle.createFilled(newColor(1.0,0.65,0.0)),
    LegendEntry(title="tt-pair",drawOptions="F",priority=0),
)

addSample("ttbarSemi",
    ["TTJetsSemi"],
    HistogramStyle.createFilled(newColor(1.0,0.65,0.0)),
    LegendEntry(title="tt-pair",drawOptions="F",priority=0),
)

addSample(
    "WJetsExclBF",
    ["WJetsExclBF"],
    HistogramStyle.createFilled(newColor(0.0,0.5,0.0)),
    LegendEntry(title="W+bX",drawOptions="F",priority=0),
    "1.3"
)

addSample(
    "WJetsExclCF",
    ["WJetsExclCF"],
    HistogramStyle.createFilled(newColor(0.0,0.75,0.35)),
    LegendEntry(title="W+cX",drawOptions="F",priority=0),
    "1.3"
)

addSample(
    "WJetsExclLF",
    ["WJetsExclLF"],
    HistogramStyle.createFilled(newColor(0.0,1.0,0.45)),
    LegendEntry(title="W+LF",drawOptions="F",priority=0)
)

addSample(
    "other",
    ["DY","DiBoson"],
    HistogramStyle.createFilled(newColor(0.1,0.5,1.0)),
    LegendEntry(title="DY+VV",drawOptions="F",priority=0)
)




#--------- data --------------------
addSample(
    "SingleMu",
    ["SingleMu"],
    HistogramStyle.createMarkers(),
    LegendEntry(title="data",drawOptions="PE",priority=10)
)

addSample(
    "SingleEle",
    ["SingleEle"],
    HistogramStyle.createMarkers(),
    LegendEntry(title="data",drawOptions="PE",priority=10)
)
