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

import os, sys



f = open("plots.condor","w")
f.write("Universe   = vanilla\n")
f.write("Executable = run.sh\n")
f.write("Log        = /dev/null\n")
f.write("Output     = log/log$(Process).out\n")
f.write("Error      = log/log$(Process).error\n")
f.write("should_transfer_files = NO\n")
f.write("when_to_transfer_output = NEVER\n")




for category in [["2j0t",c2j0t],["2j1t",c2j1t],["3j1t",c3j1t],["3j2t",c3j2t]]:
    for var in [
        ["bdt_qcd","BDT QCD","",EquiBinning(50,0.4,1)],
        ["mtw","MTW","GeV",EquiBinning(50,0,200)],
        ["met","MET","GeV",EquiBinning(50,0,200)],
        ["met_phi","#phi(MET)","",EquiBinning(50,-3.2,3.2)],
        ["lepton_pt","pT(l)","GeV",EquiBinning(50,0,200)],
        ["lepton_eta","#eta(l)","",EquiBinning(50,-2.5,2.5)],
        ["lepton_iso","rel. iso","",EquiBinning(50,0,0.15)],
        ["ljet_pt","pT(ljet)","GeV",EquiBinning(50,0,250)],
        ["ljet_eta","#eta(ljet)","",EquiBinning(50,-5,5)],
        ["ljet_mass","#eta(bjet)","GeV",EquiBinning(50,0,200)],
        ["ljet_dr","#DeltaR","",EquiBinning(50,0,7)],
        ["bjet_pt","pT(bjet)","GeV",EquiBinning(50,0,250)],
        ["bjet_eta","#eta(bjet)","",EquiBinning(50,-5,5)],
        ["bjet_mass","#eta(bjet)","GeV",EquiBinning(50,0,200)],
        ["cos_theta_whel_lj","cos#theta_{whel}","",EquiBinning(50,-1,1)],
        ["cos_theta_lj","cos#theta_{lj}","",EquiBinning(50,-1,1)],
        ["top_pt","pT(top)","GeV",EquiBinning(50,0,250)],
        ["top_eta","#eta(top)","",EquiBinning(50,-6,6)],
        ["top_mass","m(top)","GeV",EquiBinning(50,0,250)],
        ["w_pt","pT(W)","GeV",EquiBinning(50,0,250)],
        ["w_eta","#eta(W)","",EquiBinning(50,-6,6)],
        ["w_phi","#phi(W)","",EquiBinning(50,-3.2,3.2)]
    ]:
        args="Arguments = \"--name=mu_"+category[0]+"_"+var[0]+" --stackMC=MC_mu_single --stackData=data_mu --var="+var[0]+" --varName='"+var[1]+"' --unit='"+var[2]+"' --text='#mu+jets, "+category[0]+", 16.9' --weightMC='"+(category[1]+qcd+lumiMu).get()+"' --weightData='"+(category[1]+qcd).get()+"' --binning='"+str(var[3]).replace(" ","")+"'\"\n"
        #args=args.replace("'","\\\"")#.replace("(","\\\\(").replace(")","\\\\)")
        f.write(args)
        f.write("Queue\n")
        
        
        args="Arguments = \"--name=ele_"+category[0]+"_"+var[0]+" --stackMC=MC_ele_single --stackData=data_ele --var="+var[0]+" --varName='"+var[1]+"' --unit='"+var[2]+"' --text='#e+jets, "+category[0]+", 18.9' --weightMC='"+(category[1]+qcd+lumiEle).get()+"' --weightData='"+(category[1]+qcd).get()+"' --binning='"+str(var[3]).replace(" ","")+"'\"\n"
        #args=args.replace("'","\\\"")#.replace("(","\\\\(").replace(")","\\\\)")
        f.write(args)
        f.write("Queue\n")

f.close()
            
'''
    parser.add_option("--stackMC", dest="stackMC")
    parser.add_option("--stackData", dest="stackData")
    parser.add_option("--var", dest="var")
    parser.add_option("--varName", dest="varName")
    parser.add_option("--unit", dest="unit")
    parser.add_option("--text", dest="text")
    parser.add_option("--weight", dest="weight")
    parser.add_option("--binning", dest="binning")
    
    
        print category[0],var[0]
        makePlot("mu_"+category[0]+"_"+var[0],"MC_mu_single","data_mu",var[0],var[1],var[2],"#mu+jets, "+category[0]+", 16.9",category[1]+qcd+lumiMu,category[1]+qcd,var[3])
        makePlot("ele_"+category[0]+"_"+var[0],"MC_ele_single","data_ele",var[0],var[1],var[2],"e+jets, "+category[0]+", 18.9",category[1]+qcd+lumiEle,category[1]+qcd,var[3])
'''

