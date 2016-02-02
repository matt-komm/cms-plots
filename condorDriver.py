from Canvas import *
from Histogram import *
from Stack import *
from Axis import *
from InfoText import *
from Position import *
from Weight import *
from SystematicBand import *
from Box import *
import InputBuilder
import SampleBuilder
import StackBuilder


import os, sys, random

import ROOT
ROOT.gSystem.Load("libpowerlib.so")

ROOT.gROOT.SetBatch(True)
ROOT.gROOT.SetStyle("Plain")




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
    
    
sampleDict={
    "tchan":{
        "histStyle":HistogramStyle.createFilled(newColor(1.0,0.0,0.0)),
        "legend":LegendEntry("#it{t}-channel",drawOptions="F"),
        "scale":"beta_signal",
        "hists":["tchan"]
    },
    "tWschan":{
        "histStyle":HistogramStyle.createFilled(newColor(0.5,0.0,0.0)),
        "legend":LegendEntry("#it{s}-ch./tW",drawOptions="F"),
        "scale":"ttjets",
        "hists":["twchan","schan"]
    },
    "ttjets":{
        "histStyle":HistogramStyle.createFilled(newColor(1.0,0.65,0.0)),
        "legend":LegendEntry("tt#lower[-0.87]{#kern[-0.88]{-}}",drawOptions="F"),
        "scale":"ttjets",
        "hists":["ttjets"]
    },
    "wjets":{
        "histStyle":HistogramStyle.createFilled(newColor(0.0,0.5,0.0)),
        "legend":LegendEntry("W/Z/diboson",addtitle="",drawOptions="F"),
        "scale":"wzjets",
        "hists":["wjets_heavy","wjets_charm","wjets_light","dyjets","diboson"]
    },
    "qcd":{
        "histStyle":HistogramStyle.createFilled(newColor(0.65,0.65,0.65)),
        "legend":LegendEntry("Multijet",drawOptions="F"),
        "scale":"qcd",
        "hists":["qcd"]
    },
    
    "data":{
        "histStyle":HistogramStyle.createMarkers(newColor(0.0,0.0,0.0)),
        "legend":LegendEntry("Data",drawOptions="P"),
        "hists":["DATA"]
    },
}

sysNames=[
['stat', "statistical"],

#fitting
['fiterror', "ML-fit uncertainty"],
['diboson', "Di Boson fraction"],
['dyjets', "Drell-Yan fraction"],
['schan', "s-channel fraction"],
['twchan', "tW fraction"],
['qcd_antiiso', "QCD shape"],
['qcd_yield', "QCD yield"],

#detector
['btag_bc', "b tagging"],
['btag_l', "mistagging"],
['jer', "JER"],
['jes', "JES"],
['met', "unclustered \\MET"],
['pu', "pileup"],
['lepton_id', "lepton ID"],
['lepton_iso', "lepton isolation"],
['lepton_trigger', "trigger efficiency"],

#add reweighting
['top_weight', "top \\pT reweighting"],
['wjets_pt_weight', "\\wjets W \\pT reweighting"],
['wjets_flavour_heavy', "\\wjets heavy flavor fraction"],
['wjets_flavour_light', "\\wjets light flavor fraction"],
['wjets_shape', "\\wjets shape reweighting"],

#theory
['generator', "generator model"],
['mass', "top quark mass"],
#['tchan_scale', "$Q^{2}$ scale t-channel"],
['tchan_qscale_me_weight', "$Q^{2}$ scale t-channel"],
['ttjets_scale', "\\ttbar $Q^{2}$ scale"],
#['ttjets_qscale_me_weight', "\\ttbar $Q^{2}$ scale"],
['ttjets_matching', "\\ttbar matching"],
['wzjets_scale', "\\wjets $Q^{2}$ scale"],
#['wzjets_qscale_me_weight', "\\wjets $Q^{2}$ scale"],
['wzjets_matching', "\\wjets matching"],
['pdf', "PDF"],

['mcstat', "limited MC"],
]

def readFile(fName):
    fUp = open(fName)
    result={}
    for line in fUp:
        split = line.replace("\n","").replace("\r","").split(" ")
        result[split[0]]={"mean":float(split[1]),"error":float(split[2])}
    return result


fitDict={}
fitDict["nominal"]=readFile(os.path.join("/home/mkomm/Analysis/STpol/paper_plots/bdt_Jun22_final","nominal","mu.txt"))
for sysName in sysNames:
    name = sysName[0]
    if name in ["stat","fiterror","mcstat","generator"]:
        continue
    else:
        fitDict[name]={}
        fileNameUp = os.path.join("/home/mkomm/Analysis/STpol/paper_plots/bdt_Jun22_final",name+"__up","mu.txt")
        fitUp = readFile(fileNameUp)
        fitDict[name]["up"]=fitUp
        fileNameDown = os.path.join("/home/mkomm/Analysis/STpol/paper_plots/bdt_Jun22_final",name+"__down","mu.txt")
        fitDown = readFile(fileNameUp)
        fitDict[name]["down"]=fitDown
        
def normalize(output):
    s=0.0
    for i in range(len(output)):
        if output[i]<0.0:
            output[i]=0.0
        s+=output[i]
    for i in range(len(output)):
        output[i]=output[i]/s
        
def diceGaus(output,hist,covHist):
    N=hist.GetNbinsX()
    mean=numpy.zeros(N)
    cov=numpy.zeros((N,N))
    for i in range(N):
        for j in range(N):
            cov[i][j]=covHist.GetBinContent(i+1,j+1)
    diced=numpy.random.multivariate_normal(mean,cov)
    for i in range(N):
        output[i]+=diced[i]
        
def calculateTestQuantity(dataDist, mcDist):
    chi2=0.0
    for ibin in range(len(dataDist)):
        data = dataDist[ibin]
        mc = mcDist[ibin]
        if (data+mc)>0:
            chi2+=(data-mc)**2/(data+mc)
    return chi2

    
def calculateChi2(data,nominalMC,covariance):
    
    chi2 = 0.0
    '''
    for i in range(data.GetNbinsX()):
        covariance[i][i]+=data.GetBinError(i+1)**2
        #print i,math.sqrt(covariance[i][i]),data.GetBinError(i+1)
    '''
    invcov = numpy.linalg.inv(covariance)
    for i in range(data.GetNbinsX()):
        for j in range(data.GetNbinsX()):
            chi2+=(data.GetBinContent(i+1)-nominalMC.GetBinContent(i+1))*(data.GetBinContent(j+1)-nominalMC.GetBinContent(j+1))*invcov[i][j]
            #print i,j,(data.GetBinContent(i+1)-nominalMC.GetBinContent(i+1)),(data.GetBinContent(j+1)-nominalMC.GetBinContent(j+1)),invcov[i][j]
    print "chi2=",chi2
    return ROOT.TMath.Gamma(data.GetNbinsX()/2,chi2/2)
    
    '''
    p = 1.0
    for i in range(data.GetNbinsX()):
        nsigma = math.fabs(data.GetBinContent(i+1)-nominalMC.GetBinContent(i+1))/math.sqrt(covariance[i,i]+data.GetBinError(i+1)**2)
        pval=1-ROOT.TMath.Erf(nsigma/math.sqrt(2))
        p*=pval
        print "%02i: d=%4.0f+-%2.1f m=%6.1f+-%3.1f | %3.1f / %3.1f = %1.2f => p=%4.3f" % (i,data.GetBinContent(i+1),data.GetBinError(i+1),nominalMC.GetBinContent(i+1),math.sqrt(covariance[i,i]),(data.GetBinContent(i+1)-nominalMC.GetBinContent(i+1)),math.sqrt(math.sqrt(covariance[i,i])**2+data.GetBinError(i+1)**2),nsigma,pval)
        
    return p
    '''
            
def diceShape(output,nominalHist,upHist,downHist,d=None):
    if d==None:
        d = ROOT.gRandom.Gaus(0.0,1.0)
    for i in range(nominalHist.GetNbinsX()):
        
        up=upHist.GetBinContent(i+1)
        nom=nominalHist.GetBinContent(i+1)
        down=downHist.GetBinContent(i+1)
        #print i,down/downHist.Integral()*3
        #symmetrize if only one-sided
        '''
        if (up<nom and down<nom) or (up>nom and down>nom):
            diff=max(math.fabs(up-nom),math.fabs(down-nom))
            up=nom+diff
            down=nom-diff
        '''
        
        #symmetrize always
        
        diff=max(math.fabs(up-nom),math.fabs(down-nom))
        #print nom,down,diff,nom-diff
        up=nom+diff
        down=nom-diff
        
        #d=-1.0
        
        if d>1:
            output[i]+= (up-nom)*math.fabs(d)
        elif d<-1:
            output[i]+= (down-nom)*math.fabs(d)
        else:
            output[i]+= d/2.0*(up-down)+(d*d-math.fabs(d*d*d)/2.0)*(up+down-2.0*nom)
        

def makePlotFromHists(outName,rootFileName,prefix,varName,unit,lumiText,addText="",rebin=1,normalize=False, dataSubtracted=False):
    if not dataSubtracted:
        resRange=[0.6,1.4]
    else:
        resRange=[0.15,1.85]
    cv=CanvasResiduen(widthCM=9.0,margins=globalPosition.canvas,resRange=resRange)
    
    
    legend=Legend(position=globalPosition.legend)
    #legend.textsize=9
    stackPlot_MC = Stack()
    histBackgroundSum = None
    histSignalSum = None
    
    rootFile = ROOT.TFile(rootFileName)
    #for sampleName in ["tchan","tWschan","wjets","ttjets","other","qcd"]:
    for sampleName in ["qcd","wjets","ttjets","tWschan","tchan"]:
        sampleHist=None
        for i,histName in enumerate(sampleDict[sampleName]["hists"]):
            #print sampleName,i
            nominalName=prefix+"__"+histName
            hist = rootFile.Get(nominalName)
            hist.Rebin(rebin)
            
            if i==0:    
                sampleHist=Histogram1D.createFromRootHist(hist)
                sampleHist.setStyle(sampleDict[sampleName]["histStyle"])
            else:
                tempHist=Histogram1D.createFromRootHist(hist)
                sampleHist.addHistogram(tempHist)
        sampleHist.scale(fitDict["nominal"][sampleDict[sampleName]["scale"]]["mean"])
        legendEntry=sampleDict[sampleName]["legend"]
        legendEntry.rootObj=sampleHist.getRootHistogram()
        legend.addEntry(legendEntry)
        sampleHist.removeNegativeEntries() 
        stackPlot_MC.addHistogram(sampleHist) 
        
        
        if sampleName!="tchan":
            if histBackgroundSum==None:
                histBackgroundSum=Histogram1D.createFromRootHist(sampleHist._rootHistogram)
            else:
                histBackgroundSum._rootHistogram.Add(sampleHist._rootHistogram)
        else:
            if histSignalSum==None:
                histSignalSum=Histogram1D.createFromRootHist(sampleHist._rootHistogram)
                histSignalSum.setStyle(sampleDict[sampleName]["histStyle"])
            else:
                histSignalSum._rootHistogram.Add(sampleHist._rootHistogram)
            
         
    
    stackPlot_DATA = Stack()
    rootFile = ROOT.TFile(rootFileName)
    for sampleName in ["data"]:
        sampleHist=None
        for i,histName in enumerate(sampleDict[sampleName]["hists"]):
            #print sampleName,i
            nominalName=prefix+"__"+histName
            hist = rootFile.Get(nominalName)
            hist.Rebin(rebin)
            if i==0:
                sampleHist=Histogram1D.createFromRootHist(hist)
                sampleHist.setStyle(sampleDict[sampleName]["histStyle"])
            else:
                tempHist=Histogram1D.createFromRootHist(hist)
                sampleHist.addHistogram(tempHist)
        legendEntry=sampleDict[sampleName]["legend"]
        legendEntry.rootObj=sampleHist.getRootHistogram()
        legend.addEntry(legendEntry)
        
        sampleHist.removeNegativeEntries() 
        stackPlot_DATA.addHistogram(sampleHist)
        
    ########################################################
    histSumDATA=stackPlot_DATA.getSum()
    
    if not dataSubtracted:
        cv.addDrawable(stackPlot_MC)
        histSumMC=stackPlot_MC.getSum()
    
    else:
        cv.addDrawable(histSignalSum)
        histSumMC=histSignalSum
        histSumDATA.addHistogram(histBackgroundSum,-1.0)
    
    cv.addDrawable(histSumDATA)
    
    #######################################################
    
    
    print "data = ",histSumDATA.getRootHistogram().Integral()
    
    if normalize:
        norm = histSumDATA.getRootHistogram().Integral()/histSumMC.getRootHistogram().Integral()
        for hist in stackPlot_MC._histograms:
            hist.scale(norm)
        histSumMC.scale(norm)

    
    cv.addDrawable(InfoText([TextItem(addText,63,8)],
        position=BoundingBox(BoundingBox.PERCENTS,0.67,0.915,0.67,0.915),
        orientation=InfoText.SIDEWAYS,
        alignment=33
    ))
    
    
    cv.setCoordinateStyle(CoordinateStyle(xtitle=varName,unit=unit,ytitle="Events",unitBinning=sampleHist.getBinning()))
    

    cv.addDrawable(InfoText.createCMSText(orientation=InfoText.SIDEWAYS,position=globalPosition.cmstext))
    cv.addDrawable(InfoText.createLumiText(lumi=lumiText,position=globalPosition.lumi))

    #cv.addDrawable(InfoText.createCMSText(orientation=InfoText.SIDEWAYS,position=globalPosition.cmstext))
    
    sysHists={}
    for sysName in sysNames:
        name = sysName[0]
        if name in ["stat","fiterror","mcstat","generator"]:
            #sysHists[name]={'shape':False}
            pass
        else:
            sysHists[name]={'shape':True}
            #print name
            sysHistUp=None
            sysHistDown=None
            #for sampleName in ["tchan","tWschan","wjets","ttjets","other","qcd"]:
            for sampleName in ["qcd","ttjets","wjets","tWschan","tchan"]:
                for i,histName in enumerate(sampleDict[sampleName]["hists"]):
                    #print sampleName,i
                    sysNameUp=prefix+"__"+histName+"__"+name+"__up"
                    histUp = rootFile.Get(sysNameUp)
                    
                    sysNameDown=prefix+"__"+histName+"__"+name+"__down"
                    histDown = rootFile.Get(sysNameDown)
                    
                    if histUp and histDown:
                        #print sysNameUp
                        if sysHistUp==None:
                            sysHistUp=Histogram1D.createFromRootHist(histUp)
                            sysHistUp.scale(fitDict[name]["up"][sampleDict[sampleName]["scale"]]["mean"])
                            
                            sysHistDown=Histogram1D.createFromRootHist(histDown)
                            sysHistDown.scale(fitDict[name]["down"][sampleDict[sampleName]["scale"]]["mean"])
                        else:
                            tempHist=Histogram1D.createFromRootHist(histUp)
                            tempHist.scale(fitDict[name]["up"][sampleDict[sampleName]["scale"]]["mean"])
                            sysHistUp.addHistogram(tempHist)
                            
                            tempHist=Histogram1D.createFromRootHist(histDown)
                            tempHist.scale(fitDict[name]["down"][sampleDict[sampleName]["scale"]]["mean"])
                            sysHistDown.addHistogram(tempHist)

                    else:
                        nominalName=prefix+"__"+histName
                        #print nominalName
                        histUp = rootFile.Get(nominalName)
                        histDown = rootFile.Get(nominalName)
                        if sysHistUp==None:
                            sysHistUp=Histogram1D.createFromRootHist(histUp)
                            sysHistUp.scale(fitDict["nominal"][sampleDict[sampleName]["scale"]]["mean"])
                            
                            sysHistDown=Histogram1D.createFromRootHist(histDown)
                            sysHistDown.scale(fitDict["nominal"][sampleDict[sampleName]["scale"]]["mean"])
                        else:
                            tempHist=Histogram1D.createFromRootHist(histUp)
                            tempHist.scale(fitDict["nominal"][sampleDict[sampleName]["scale"]]["mean"])
                            sysHistUp.addHistogram(tempHist)
                            
                            tempHist=Histogram1D.createFromRootHist(histDown)
                            tempHist.scale(fitDict["nominal"][sampleDict[sampleName]["scale"]]["mean"])
                            sysHistDown.addHistogram(tempHist)
            sysHistUp.rebin(rebin)
            sysHistDown.rebin(rebin)
            
            ###################################################
            
            if dataSubtracted:
                sysHistUp.addHistogram(histBackgroundSum,-1.0)
                sysHistDown.addHistogram(histBackgroundSum,-1.0)
            
            ###################################################
            
            sysHistUp.getRootHistogram().Scale(histSumMC.getRootHistogram().Integral()/sysHistUp.getRootHistogram().Integral())
            sysHistDown.getRootHistogram().Scale(histSumMC.getRootHistogram().Integral()/sysHistDown.getRootHistogram().Integral())
            sysHists[name]["up"]=sysHistUp
            sysHists[name]["down"]=sysHistDown
            
            
            
            
            
            
            
            
            #print name, ": %5.4f  %5.4f" %(sysHistDown.getRootHistogram().Integral()/histSumMC.getRootHistogram().Integral(),sysHistUp.getRootHistogram().Integral()/histSumMC.getRootHistogram().Integral())
            
            
    '''
    sysHists["jes"]["down"].divideHistogram(stackPlot_MC.getSum())
    sysHists["jes"]["down"].setStyle(HistogramStyle.createLine(2))
    
    sysHists["jes"]["up"].divideHistogram(stackPlot_MC.getSum())
    sysHists["jes"]["up"].setStyle(HistogramStyle.createLine(3))
            
    cv.addResiduen(sysHists["jes"]["down"])
    cv.addResiduen(sysHists["jes"]["up"])
    '''   
    
    nominalTQ = calculateTestQuantity(histSumDATA.getRootHistogram(),histSumMC.getRootHistogram())
    print nominalTQ
    
    tqHist = ROOT.TH1F("tqHist",";log(TQ_{i}/TQ_{nominal}));toys",100,-1,3)
    ntqClose=0
    
    NTOYS=15000
    sysBandDist=numpy.zeros((NTOYS,histSumMC.getRootHistogram().GetNbinsX()))
    
    
    for toy in range(NTOYS):
        if toy%500==0:
            print "process dist... ",100.0*toy/NTOYS,"%"
        for ibin in range(histSumMC.getRootHistogram().GetNbinsX()):
            sysBandDist[toy][ibin]=histSumMC.getRootHistogram().GetBinContent(ibin+1)
        for sysName in sysHists.keys():
            sysDict = sysHists[sysName]
            if sysDict["shape"]:
                diceShape(sysBandDist[toy],histSumMC.getRootHistogram(),sysDict["up"].getRootHistogram(),sysDict["down"].getRootHistogram())
            else:
                pass
                
        dataToys=numpy.zeros(histSumDATA.getRootHistogram().GetNbinsX())
        for ibin in range(histSumDATA.getRootHistogram().GetNbinsX()):
            dataToys[ibin]=ROOT.gRandom.Poisson(histSumDATA.getRootHistogram().GetBinContent(ibin+1))

        '''
        tqToy = calculateTestQuantity(dataToys,sysBandDist[toy])
        if tqToy<nominalTQ:
            ntqClose+=1
        tqHist.Fill(math.log(tqToy/nominalTQ))
        '''
        
        #normalize(sysBandDist[toy])
        #sysBandDist[toy]*=histSumDATA.getRootHistogram().Integral()
        
     
    print "p=",1.0*(NTOYS-ntqClose)/NTOYS
    #cvTQ = ROOT.TCanvas("cvtq","",800,600)
    #tqHist.Draw()
    #cvTQ.WaitPrimitive()
    
    
    '''
    covariance=numpy.zeros((histSumMC.getRootHistogram().GetNbinsX(),histSumMC.getRootHistogram().GetNbinsX()))
    pcov = 0
    for ibin in range(histSumMC.getRootHistogram().GetNbinsX()):
        for jbin in range(ibin,histSumMC.getRootHistogram().GetNbinsX()):
            if ibin!=jbin:
                continue
            for itoy in range(NTOYS):
                for jtoy in range(itoy+1,NTOYS):
                    if pcov%200000==0:
                        print "process cov... ",100.0*pcov/(histSumMC.getRootHistogram().GetNbinsX()*NTOYS)**2*4,"%"
                    pcov+=1
                    covariance[ibin][jbin]+=(sysBandDist[itoy][ibin]-sysBandDist[jtoy][ibin])*(sysBandDist[itoy][jbin]-sysBandDist[jtoy][jbin])
            covariance[ibin][jbin]/=NTOYS**2
            covariance[jbin][ibin]=covariance[ibin][jbin]
    #print covariance
    pvalue = calculateChi2(histSumDATA.getRootHistogram(),histSumMC.getRootHistogram(),covariance)
    print "pvalue=",pvalue
    print "sigma=",ROOT.TMath.ErfInverse(1-pvalue)*math.sqrt(2)
    '''
    
    downSys,mean,upSys=numpy.percentile(sysBandDist, [15.866,50.0,84.134],0)
    '''
    pullCv = ROOT.TCanvas("pullCv","",800,600)
    pullHist = ROOT.TH1F("pullHist",";#delta data/#sigma;",50,-2,2)
    for ibin in range(len(mean)):
        d=histSumDATA.getRootHistogram().GetBinContent(ibin+1)-histSumMC.getRootHistogram().GetBinContent(ibin+1)
        err=math.sqrt(histSumDATA.getRootHistogram().GetBinError(ibin+1)**2+(0.5*(upSys[ibin]-downSys[ibin]))**2)
        pullHist.Fill(d/err)
    pullHist.Draw()
    pullCv.Update()
    pullCv.WaitPrimitive()
    '''
    
    for ibin in range(histSumMC.getRootHistogram().GetNbinsX()):
        if mean[ibin]<0.1 or math.isnan(downSys[ibin]) or math.isnan(upSys[ibin]):
            continue
        #print ibin,"%5.4f: %5.4f, %5.4f (%5.4f)" % (mean[ibin],downSys[ibin]/mean[ibin],upSys[ibin]/mean[ibin],math.sqrt(covariance[ibin][ibin])/mean[ibin])
        w = histSumMC.getRootHistogram().GetBinWidth(ibin+1)
        c = histSumMC.getRootHistogram().GetBinCenter(ibin+1)
        u = min(resRange[1]-0.005,upSys[ibin]/mean[ibin])
        d = max(resRange[0]+0.005,downSys[ibin]/mean[ibin])
        
        box = Box(c-0.5*w,d,c+0.5*w,u)
        cv.addResiduen(box)
        
    legendEntry=LegendEntry("",drawOptions="",priority=-1)
    legendEntry.rootObj=""
    legend.addEntry(legendEntry)
    
    legendEntry=LegendEntry("Total syst.",drawOptions="F",priority=-2)
    legendEntry.rootObj=box._rootBoxF
    legend.addEntry(legendEntry)
    
    
    cv.addDrawable(legend)

    dataResHist=Histogram1D.createFromRootHist(histSumDATA.getRootHistogram())
    dataResHist.divideHistogram(histSumMC)
    dataResHist.setStyle(HistogramStyle.createMarkers())
    cv.addResiduen(dataResHist)
    

    cv.draw()
       
    cv.save(outName+".pdf")
    cv.save(outName+".png")
    cv.save(outName+".C")
    cv.wait() 
    
makePlotFromHists(
    "mu_2j1t_cos_theta",
    "/home/mkomm/Analysis/STpol/paper_plots/Jul11_plots/merged/0.45000/mu/cos_theta_lj.root",
    "2j1t_cos_theta_lj",
    "cos#kern[0.1]{#theta}#scale[0.7]{#lower[0.28]{#mu}}#kern[-1.1]{*}",
    "",
    "2#kern[-0.5]{ }jets 1#kern[-0.5]{ }tag, 19.7",
    "BDT#scale[0.7]{#lower[0.2]{W/tt#lower[-0.87]{#kern[-1]{-}}}} > 0.45",
    rebin=2
)
    
makePlotFromHists(
    "mu_2j1t_cos_theta_bgsub",
    "/home/mkomm/Analysis/STpol/paper_plots/Jul11_plots/merged/0.45000/mu/cos_theta_lj.root",
    "2j1t_cos_theta_lj",
    "cos#kern[0.1]{#theta}#scale[0.7]{#lower[0.28]{#mu}}#kern[-1.1]{*}",
    "",
    "2#kern[-0.5]{ }jets 1#kern[-0.5]{ }tag, 19.7",
    "BDT#scale[0.7]{#lower[0.2]{W/tt#lower[-0.87]{#kern[-1]{-}}}} > 0.45",
    rebin=2,
    dataSubtracted=True
)
'''
makePlotFromHists(
    "mu_2j1t_abseta",
    "/home/mkomm/Analysis/STpol/paper_plots/Jul11_plots/merged/preselection/2j_1t/mu/abs_ljet_eta.root",
    "2j1t_abs_ljet_eta",
    "|#eta#scale[0.7]{#lower[0.2]{#kern[-0.5]{ }j#lower[0.2]{#scale[1.2]{'}}}}|",
    "",
    "2#kern[-0.5]{ }jets 1#kern[-0.5]{ }tag, 19.7",
    "",
    rebin=1
)
'''
'''
makePlotFromHists(
    "mu_2j1t_topmass",
    "/home/mkomm/Analysis/STpol/paper_plots/Jul11_plots/merged/preselection/2j_1t/mu/top_mass.root",
    "2j1t_top_mass",
    "m#scale[0.7]{#lower[0.2]{b#mu#nu}} / GeV",
    "",
    "2#kern[-0.5]{ }jets 1#kern[-0.5]{ }tag, 19.7",
    "",
    rebin=1
)

    
makePlotFromHists(
    "mu_2j1t_bdt_sig_bg",
    "/home/mkomm/Analysis/STpol/paper_plots/Jul11_plots/merged/preselection/2j_1t/mu/bdt_sig_bg.root",
    "2j1t_bdt_sig_bg",
    "#lower[-0.18]{BDT#scale[0.7]{#lower[0.2]{W/tt#lower[-0.87]{#kern[-1]{-}}}}}",
    "",
    "2#kern[-0.5]{ }jets 1#kern[-0.5]{ }tag, 19.7",
    "",
    rebin=1
)
    
makePlotFromHists(
    "mu_2j1t_met",
    "/home/mkomm/Analysis/STpol/paper_plots/Jul11_plots/merged/preqcd/2j_1t/mu/met.root",
    "2j1t_met",
    "#lower[-0.1]{E#scale[0.7]{#lower[0.28]{T}}#kern[-2.35]{#scale[1.3]{#lower[0.1]{/}}}}",
    "",
    "2#kern[-0.5]{ }jets 1#kern[-0.5]{ }tag, 19.7",
    "",
    rebin=1
)

makePlotFromHists(
    "mu_3j2t_met",
    "/home/mkomm/Analysis/STpol/paper_plots/Jul11_plots/merged/preqcd/3j_2t/mu/met.root",
    "3j2t_met",
    "#lower[-0.1]{E#scale[0.7]{#lower[0.28]{T}}#kern[-2.35]{#scale[1.3]{#lower[0.1]{/}}}}",
    "",
    "3#kern[-0.5]{ }jets 2#kern[-0.5]{ }tag, 19.7",
    "",
    rebin=1
)

makePlotFromHists(
    "mu_2j1t_mtw",
    "/home/mkomm/Analysis/STpol/paper_plots/Jul11_plots/merged/preqcd/2j_1t/mu/mtw.root",
    "2j1t_mtw",
    "M#scale[0.7]{#lower[0.28]{T}}(W)",
    "",
    "2#kern[-0.5]{ }jets 1#kern[-0.5]{ }tag, 19.7",
    "",
    rebin=1
)

makePlotFromHists(
    "mu_3j2t_mtw",
    "/home/mkomm/Analysis/STpol/paper_plots/Jul11_plots/merged/preqcd/3j_2t/mu/mtw.root",
    "3j2t_mtw",
    "M#scale[0.7]{#lower[0.28]{T}}(W)",
    "",
    "3#kern[-0.5]{ }jets 2#kern[-0.5]{ }tag, 19.7",
    "",
    rebin=1
)


makePlotFromHists(
    "mu_2j1t_bdt_qcd",
    "/home/mkomm/Analysis/STpol/paper_plots/Jul11_plots/merged/preqcd/2j_1t/mu/bdt_qcd.root",
    "2j1t_bdt_qcd",
    "BDT#scale[0.7]{#lower[0.28]{multijet}}",
    "",
    "2#kern[-0.5]{ }jets 1#kern[-0.5]{ }tag, 19.7",
    "",
    rebin=1
)

makePlotFromHists(
    "mu_3j2t_bdt_qcd",
    "/home/mkomm/Analysis/STpol/paper_plots/Jul11_plots/merged/preqcd/3j_2t/mu/bdt_qcd.root",
    "3j2t_bdt_qcd",
    "BDT#scale[0.7]{#lower[0.28]{multijet}}",
    "",
    "3#kern[-0.5]{ }jets 2#kern[-0.5]{ }tags, 19.7",
    "",
    rebin=1
)



makePlotFromHists(
    "mu_2j0t_bdt_sig_bg",
    "/home/mkomm/Analysis/STpol/paper_plots/Jul11_plots/merged/preselection/2j_0t/mu/bdt_sig_bg.root",
    "2j0t_bdt_sig_bg",
    "#lower[-0.18]{BDT#scale[0.7]{#lower[0.2]{W/tt#lower[-0.87]{#kern[-1]{-}}}}}",
    "",
    "2#kern[-0.5]{ }jets 0#kern[-0.5]{ }tags, 19.7",
    "",
    rebin=1,
    normalize=True
)

makePlotFromHists(
    "mu_2j1t_bdt_sig_bg",
    "/home/mkomm/Analysis/STpol/paper_plots/Jul11_plots/merged/preselection/2j_1t/mu/bdt_sig_bg.root",
    "2j1t_bdt_sig_bg",
    "#lower[-0.18]{BDT#scale[0.7]{#lower[0.2]{W/tt#lower[-0.87]{#kern[-1]{-}}}}}",
    "",
    "2#kern[-0.5]{ }jets 1#kern[-0.5]{ }tag, 19.7",
    "",
    rebin=1
)

makePlotFromHists(
    "mu_3j2t_cos_theta",
    "/home/mkomm/Analysis/STpol/paper_plots/Jul11_plots/merged/preselection/3j_2t/mu/cos_theta_lj.root",
    "3j2t_cos_theta_lj",
    "cos#kern[0.1]{#theta}#scale[0.7]{#lower[0.28]{#mu}}#kern[-1.1]{*}",
    "",
    "3#kern[-0.5]{ }jets 2#kern[-0.5]{ }tags, 19.7",
    "",
    rebin=2
)
makePlotFromHists(
    "mu_3j2t_bdt_sig_bg",
    "/home/mkomm/Analysis/STpol/paper_plots/Jul11_plots/merged/preselection/3j_2t/mu/bdt_sig_bg.root",
    "3j2t_bdt_sig_bg",
    "#lower[-0.18]{BDT#scale[0.7]{#lower[0.2]{W/tt#lower[-0.87]{#kern[-1]{-}}}}}",
    "",
    "3#kern[-0.5]{ }jets 2#kern[-0.5]{ }tags, 19.7",
    "",
    rebin=1
)



makePlotFromHists(
    "mu_2j1t_cos_theta_CR",
    "/home/mkomm/Analysis/STpol/paper_plots/Jul11_plots/merged/reverseBDT/0.00000/2j_1t/mu/cos_theta_lj.root",
    "2j1t_cos_theta_lj",
    "cos#kern[0.1]{#theta}#scale[0.7]{#lower[0.28]{#mu}}#kern[-1.1]{*}",
    "",
    "2#kern[-0.5]{ }jets 1#kern[-0.5]{ }tag, 19.7",
    "BDT#scale[0.7]{#lower[0.2]{W/tt#lower[-0.87]{#kern[-1]{-}}}} < 0",
    rebin=2
)

makePlotFromHists(
    "mu_2j0t_cos_theta_CR",
    "/home/mkomm/Analysis/STpol/paper_plots/Jul11_plots/merged/preselection/2j_0t/mu/cos_theta_lj.root",
    "2j0t_cos_theta_lj",
    "cos#kern[0.1]{#theta}#scale[0.7]{#lower[0.28]{#mu}}#kern[-1.1]{*}",
    "",
    "2#kern[-0.5]{ }jets 0#kern[-0.5]{ }tags, 19.7",
    "",
    rebin=2,
    normalize=True
)

'''

