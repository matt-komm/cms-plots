from Canvas import *
from Histogram import *
from Stack import *
from Axis import *
from InfoText import *
from Position import *
from Weight import *
import InputBuilder
import SampleBuilder
import StackBuilder

import os, sys, random

import ROOT
ROOT.gSystem.Load("libpowerlib.so")

ROOT.gROOT.SetBatch(True)
ROOT.gROOT.SetStyle("Plain")

InputBuilder.findSampleFiles("/nfs/user/mkomm/stpol_step3/Oct28_reproc_v8")

#InputBuilder.findSampleFiles("/home/mkomm/Analysis/STpol/Oct28_reproc_v6")

globalPosition.makeLegendOutside()

def getChi2(mcHist,dataHist):
    bins=[]
    for ibin in range(dataHist.GetNbinsX()):
        if dataHist.GetBinContent(ibin+1)>0.0000000001:
            bins.append(ibin+1)
    newHistMC=ROOT.TH1F("newHistMC"+str(random.random()),"",len(bins),0,len(bins))
    newHistMC.Sumw2()
    newHistData=ROOT.TH1F("newHistData"+str(random.random()),"",len(bins),0,len(bins))
    newHistData.Sumw2()
    for i,ibin in enumerate(bins):
        newHistMC.SetBinContent(i+1,mcHist.GetBinContent(ibin))
        newHistMC.SetBinError(i+1,mcHist.GetBinError(ibin))
        
        newHistData.SetBinContent(i+1,dataHist.GetBinContent(ibin))
        newHistData.SetBinError(i+1,dataHist.GetBinError(ibin))
    
    return newHistMC.Chi2Test(newHistData,"WW")

def getKS(mcHist,dataHist):
    bins=[]
    for ibin in range(dataHist.GetNbinsX()):
        if dataHist.GetBinContent(ibin+1)>0.0000000001:
            bins.append(ibin+1)
    newHistMC=ROOT.TH1F("newHistMC"+str(random.random()),"",len(bins),0,len(bins))
    newHistMC.Sumw2()
    newHistData=ROOT.TH1F("newHistData"+str(random.random()),"",len(bins),0,len(bins))
    newHistData.Sumw2()
    for i,ibin in enumerate(bins):
        newHistMC.SetBinContent(i+1,mcHist.GetBinContent(ibin))
        newHistMC.SetBinError(i+1,mcHist.GetBinError(ibin))
        
        newHistData.SetBinContent(i+1,dataHist.GetBinContent(ibin))
        newHistData.SetBinError(i+1,dataHist.GetBinError(ibin))
    
    return newHistMC.KolmogorovTest(newHistData)

def makePlotMConly(name,mcstack,var,varName,unit,lumiText,weightMC,binning):
    cv=CanvasResiduen(widthCM=8.5,margins=globalPosition.canvas,resRange=[0.6,1.4])
    cv.setCoordinateStyle(CoordinateStyle(xtitle=varName,unit=unit,ytitle="Events",unitBinning=binning))
    legend=Legend(position=globalPosition.legend)
    cv.addDrawable(legend)
    cv.addDrawable(InfoText.createCMSText(orientation=InfoText.SIDEWAYS,position=globalPosition.cmstext))
    cv.addDrawable(InfoText.createLumiText(lumi=lumiText,position=globalPosition.lumi))

    stackSet_MC = StackBuilder.stackDict[mcstack]
    stackPlot_MC = Stack()
    for sample in stackSet_MC.getSamples():
        sampleHist=Histogram1D.createEmpty(binning)
        sampleHist.setStyle(sample.histStyle)
        legendEntry=sample.legendEntry
        legendEntry.rootObj=sampleHist.getRootHistogram()
        legend.addEntry(legendEntry)
        for inputSet in sample.getInputs():
            for i in range(len(inputSet.datafiles)):
                #sys.stdout.write('%i/%i\r' % (i+1,len(inputSet.datafiles)))
                #sys.stdout.flush()
                print inputSet.datafiles[i]
                print (stackSet_MC.weight*sample.weight*inputSet.weight*weightMC).get()
                p = ROOT.Projector(sampleHist.getRootHistogram(), inputSet.datafiles[i], "dataframe", var, (stackSet_MC.weight*sample.weight*inputSet.weight*weightMC).get())
                p.addFriend(inputSet.weightfiles[i],"dataframe")
                p.Project()
                #break
            print   
        sampleHist.removeNegativeEntries()
        stackPlot_MC.addHistogram(sampleHist)
    cv.addDrawable(stackPlot_MC)
    cv.draw()
    cv.save(name+".pdf")
    cv.save(name+".png")

def makePlot(name,mcstack,datastack,var,varName,unit,lumiText,weightMC,weightData,binning,addText=""):
    cv=CanvasResiduen(widthCM=8.5,margins=globalPosition.canvas,resRange=[0.6,1.4])
    cv.setCoordinateStyle(CoordinateStyle(xtitle=varName,unit=unit,ytitle="Events",unitBinning=binning))
    legend=Legend(position=globalPosition.legend)
    cv.addDrawable(legend)
    cv.addDrawable(InfoText.createCMSText(orientation=InfoText.SIDEWAYS,position=globalPosition.cmstext))
    cv.addDrawable(InfoText.createLumiText(lumi=lumiText,position=globalPosition.lumi))

    stackSet_MC = StackBuilder.stackDict[mcstack]
    stackPlot_MC = Stack()
    for sample in stackSet_MC.getSamples():
        sampleHist=Histogram1D.createEmpty(binning)
        sampleHist.setStyle(sample.histStyle)
        legendEntry=sample.legendEntry
        legendEntry.rootObj=sampleHist.getRootHistogram()
        legend.addEntry(legendEntry)
        for inputSet in sample.getInputs():
            for i in range(len(inputSet.datafiles)):
                #sys.stdout.write('%i/%i\r' % (i+1,len(inputSet.datafiles)))
                #sys.stdout.flush()
                print inputSet.datafiles[i]
                p = ROOT.Projector(sampleHist.getRootHistogram(), inputSet.datafiles[i], "dataframe", var, (stackSet_MC.weight*sample.weight*inputSet.weight*weightMC).get())
                p.addFriend(inputSet.weightfiles[i],"dataframe")
                p.Project()
                #break
            print  
        sampleHist.removeNegativeEntries() 
        stackPlot_MC.addHistogram(sampleHist)
    cv.addDrawable(stackPlot_MC)

    stackSet_data = StackBuilder.stackDict[datastack]
    stackPlot_data = Stack()
    for sample in stackSet_data.getSamples():
        sampleHist=Histogram1D.createEmpty(binning)
        sampleHist.setStyle(sample.histStyle)
        legendEntry=sample.legendEntry
        legendEntry.rootObj=sampleHist.getRootHistogram()
        legend.addEntry(legendEntry)
        for inputSet in sample.getInputs():
            for i in range(len(inputSet.datafiles)):
                #sys.stdout.write('%i/%i\r' % (i+1,len(inputSet.datafiles)))
                #sys.stdout.flush()
                print inputSet.datafiles[i]
                #print (stackSet_data.weight+sample.weight+inputSet.weight+weightData).get()
                p = ROOT.Projector(sampleHist.getRootHistogram(), inputSet.datafiles[i], "dataframe", var, (stackSet_data.weight*sample.weight*inputSet.weight*weightData).get())
                p.addFriend(inputSet.weightfiles[i],"dataframe")
                p.Project()
                #break
            print   
        sampleHist.removeNegativeEntries()
        stackPlot_data.addHistogram(sampleHist)
    cv.addDrawable(stackPlot_data)
    if addText!="":
        cv.addDrawable(InfoText.createTestInfo(
            chi2=getChi2(stackPlot_MC.getSum().getRootHistogram(),stackPlot_data.getSum().getRootHistogram())*100.0,
            ks=getKS(stackPlot_MC.getSum().getRootHistogram(),stackPlot_data.getSum().getRootHistogram())*100.0,
         
            position=BoundingBox(BoundingBox.PERCENTS,0.53,0.91,0.75,0.91),
            orientation=InfoText.SIDEWAYS
        ))
    
        cv.addDrawable(InfoText([TextItem(addText,63,7.5)],
            position=BoundingBox(BoundingBox.PERCENTS,0.53,0.87,0.75,0.87),
            orientation=InfoText.SIDEWAYS
        ))
    else:
        cv.addDrawable(InfoText.createTestInfo(
            chi2=getChi2(stackPlot_MC.getSum().getRootHistogram(),stackPlot_data.getSum().getRootHistogram())*100.0,
            ks=getKS(stackPlot_MC.getSum().getRootHistogram(),stackPlot_data.getSum().getRootHistogram())*100.0,
            
            position=BoundingBox(BoundingBox.PERCENTS,0.53,0.895,0.75,0.895),
            orientation=InfoText.SIDEWAYS
        ))
    dataResHist=stackPlot_data.getSum()
    dataResHist.divideHistogram(stackPlot_MC.getSum())
    dataResHist.setStyle(HistogramStyle.createMarkers())
    cv.addResiduen(dataResHist)

    cv.draw()
    #cv.wait()    
    cv.save(name+".pdf")
    cv.save(name+".png")
    
def makeHists(name,sysVariation,mcstack,datastack,var,weightMC,weightData,binning):
    outFile = ROOT.TFile(name+".root","RECREATE")
    
    #theta naming
    #<observable>__<process>__<uncertainty>__(plus,minus) 
    #<observable>_DATA
    
    fakeData=Histogram1D.createEmpty(binning)
    fakeData.getRootHistogram().SetDirectory(outFile)
    fakeData.getRootHistogram().SetName(var+"_"+name+"__FakeDATA")
    stackSet_MC = StackBuilder.stackDict[mcstack]
    for sample in stackSet_MC.getSamples():
        sampleHist=Histogram1D.createEmpty(binning)
        sampleHist.getRootHistogram().SetDirectory(outFile)
        if (sysVariation!=""):
            sampleHist.getRootHistogram().SetName(var+"_"+name+"__"+sample.name)
        else:
            sampleHist.getRootHistogram().SetName(var+"_"+name+"__"+sample.name+"__"+sysVariation)
        for inputSet in sample.getInputs():
            for i in range(len(inputSet.datafiles)):
                #sys.stdout.write('%i/%i\r' % (i+1,len(inputSet.datafiles)))
                #sys.stdout.flush()
                print inputSet.datafiles[i]
                #print (stackSet_MC.weight+sample.weight+inputSet.weight+weightMC).get()
                p = ROOT.Projector(sampleHist.getRootHistogram(), inputSet.datafiles[i], "dataframe", var, (stackSet_MC.weight*sample.weight*inputSet.weight*weightMC).get())
                p.addFriend(inputSet.weightfiles[i],"dataframe")
                p.Project()
                #break
            print
        sampleHist.removeNegativeEntries()
        fakeData.addHistogram(sampleHist)
        
        outFile.cd()
        #sampleHist.Write()
        
        

    stackSet_data = StackBuilder.stackDict[datastack]
    for sample in stackSet_data.getSamples():
        sampleHist=Histogram1D.createEmpty(binning)
        sampleHist.getRootHistogram().SetDirectory(outFile)
        sampleHist.getRootHistogram().SetName(var+"_"+name+"__DATA")
        for inputSet in sample.getInputs():
            for i in range(len(inputSet.datafiles)):
                #sys.stdout.write('%i/%i\r' % (i+1,len(inputSet.datafiles)))
                #sys.stdout.flush()
                print inputSet.datafiles[i]
                #print (stackSet_data.weight+sample.weight+inputSet.weight+weightData).get()
                p = ROOT.Projector(sampleHist.getRootHistogram(), inputSet.datafiles[i], "dataframe", var, (stackSet_data.weight*sample.weight*inputSet.weight*weightData).get())
                p.addFriend(inputSet.weightfiles[i],"dataframe")
                p.Project()
                #break
            print
        sampleHist.removeNegativeEntries()
        outFile.cd()
        #sampleHist.Write()
    outFile.Write()
    outFile.Close()   
        
#makeHists("mu_2j1t","nominal","MC_mu_fit","data_mu","bdt_sig_bg",c2j1t*lumiMu*Weight("(bdt_qcd>0.4)"),c2j1t*Weight("(bdt_qcd>0.4)"),EquiBinning(25,-1,0))
#makeHists("mu_3j1t","nominal","MC_mu_fit","data_mu","bdt_sig_bg",c3j1t*lumiMu*Weight("(bdt_qcd>0.4)"),c3j1t*Weight("(bdt_qcd>0.4)"),EquiBinning(50,-1,1))
#makeHists("mu_3j2t","nominal","MC_mu_fit","data_mu","bdt_sig_bg",c3j2t*lumiMu*Weight("(bdt_qcd>0.4)"),c3j2t*Weight("(bdt_qcd>0.4)"),EquiBinning(50,-1,1))

#makeHists("ele_2j1t","nominal","MC_ele_fit","data_ele","bdt_sig_bg",c2j1t*lumiEle*Weight("(bdt_qcd>0.55)"),c2j1t*Weight("(bdt_qcd>0.55)"),EquiBinning(25,-1,0))
#makeHists("ele_3j1t","nominal","MC_ele_fit","data_ele","bdt_sig_bg",c3j1t*lumiEle*Weight("(bdt_qcd>0.55)"),c3j1t*Weight("(bdt_qcd>0.55)"),EquiBinning(50,-1,1))
#makeHists("ele_3j2t","nominal","MC_ele_fit","data_ele","bdt_sig_bg",c3j2t*lumiEle*Weight("(bdt_qcd>0.55)"),c3j2t*Weight("(bdt_qcd>0.55)"),EquiBinning(50,-1,1))

#makePlot("mu_2j1t_bdt_sig_bg","MC_mu_fit","data_mu","bdt_sig_bg","signal BDT","","#mu+jets, 2j1t, 10^{-3}",c2j1t*lumiMu*Weight("(bdt_qcd>0.4)"),c2j1t*Weight("(bdt_qcd>0.4)"),EquiBinning(1,-0.05,0),"cos#theta#in[0.6,0.7]")

#makePlotMConly("ttonly_ljet_rms","ttonly","ljet_rms","RMS ljet","","#mu+jets, 2j1t, 10^{-3}",c2j1t,EquiBinning(50,0.01))

