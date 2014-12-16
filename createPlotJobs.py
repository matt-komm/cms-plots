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
f.write("requirements   = (CMSFARM =?= TRUE)\n")




for category in [["2j0t",c2j0t],["2j1t",c2j1t],["3j1t",c3j1t],["3j2t",c3j2t]]:
    for var in [
        ["bdt_qcd","BDT--QCD","",EquiBinning(50,-1,1)],
        ["mtw","MTW","GeV",EquiBinning(50,0,200)],
        ["met","MET","GeV",EquiBinning(50,0,200)],
        ["met_phi","#phi(MET)","",EquiBinning(50,-3.2,3.2)],
        ["lepton_pt","pT(l)","GeV",EquiBinning(50,0,200)],
        ["lepton_eta","#eta(l)","",EquiBinning(50,-2.6,2.6)],
        ["lepton_iso","rel. iso","",EquiBinning(50,0,0.12)],
        ["lepton_charge","charge(l)","e",EquiBinning(3,-1.5,1.5)],
        ["lepton_phi","#phi(l)","",EquiBinning(50,-3.2,3.2)],
        ["ljet_pt","pT(ljet)","GeV",EquiBinning(50,0,400)],
        ["ljet_eta","#eta(ljet)","",EquiBinning(50,-5,5)],
        ["ljet_mass","m(ljet)","GeV",EquiBinning(50,0,50)],
        ["ljet_dr","#Delta--R(lj)","",EquiBinning(50,0,7)],
        ["ljet_rms","RMS(lj)","",EquiBinning(50,0,0.12)],
        ["ljet_phi","#phi(lj)","",EquiBinning(50,-3.2,3.2)],
        ["bjet_pt","pT(bjet)","GeV",EquiBinning(50,0,250)],
        ["bjet_eta","#eta(bjet)","",EquiBinning(50,-4,4)],
        ["bjet_mass","m(bjet)","GeV",EquiBinning(50,0,50)],
        ["bjet_dr","#Delta--R(bj)","",EquiBinning(50,0,7)],
        ["bjet_phi","#phi(bj)","",EquiBinning(50,-3.2,3.2)],
        ["cos_theta_whel_lj","cos#theta_{whel}","",EquiBinning(50,-1,1)],
        ["cos_theta_lj","cos#theta_{lj}","",EquiBinning(50,-1,1)],
        ["top_pt","pT(top)","GeV",EquiBinning(50,0,300)],
        ["top_eta","#eta(top)","",EquiBinning(50,-6,6)],
        ["top_mass","m(top)","GeV",EquiBinning(50,100,500)],
        ["top_phi","#phi(top)","",EquiBinning(50,-3.2,3.2)],
        ["w_pt","pT(W)","GeV",EquiBinning(50,0,500)],
        ["w_eta","#eta(W)","",EquiBinning(50,-5,5)],
        ["w_phi","#phi(W)","",EquiBinning(50,-3.2,3.2)],
        ["C","C","",EquiBinning(50,0,1)],
        ["D","D","",EquiBinning(50,0,1)],
        ["isotropy","isotropy","",EquiBinning(50,0,1)],
        ["thrust","thrust","",EquiBinning(50,0.4,1)],
        ["aplanarity","aplanarity","",EquiBinning(50,0,0.5)],
        ["circularity","circularity","",EquiBinning(50,0,1.0)],
        ["sphericity","sphericity","",EquiBinning(50,0,1.0)],
        ["hadronic_pt","pT(HFS)","GeV",EquiBinning(50,0,400)],
        ["hadronic_eta","#eta(HFS)","",EquiBinning(50,-6.5,6.5)],
        ["hadronic_mass","m(HFS)","GeV",EquiBinning(50,0,1500)],
        ["hadronic_phi","#phi(HFS)","",EquiBinning(50,-3.2,3.2)],
        ["shat_pt","pT(#hat{s})","GeV",EquiBinning(50,0,150)],
        ["shat_eta","#eta(#hat{s})","",EquiBinning(50,-8,8)],
        ["shat_mass","m(#hat{s})","GeV",EquiBinning(50,0,1500)],
        ["shat_phi","#phi(#hat{s})","",EquiBinning(50,-3.2,3.2)]
    ]:
        pass
'''
        for qcd in [["qcdnone",Weight("1")],["qcdmtw",qcdMuMTW],["qcdbdt",Weight("(bdt_qcd>0.4)")]]:
            args="Arguments = \"'--mode=plot' '--name=mu_"+category[0]+"_"+var[0]+"_"+qcd[0]+"' '--stackMC=MC_mu_single' '--stackData=data_mu' '--var="+var[0]+"' '--varName="+var[1]+"' '--unit="+var[2]+"' '--text=#mu+jets,--"+category[0]+",--16.9' '--weightMC="+(category[1]*qcd[1]*lumiMu).get()+"' '--weightData="+(category[1]*qcd[1]).get()+"' '--binning="+str(var[3]).replace(" ","")+"'\"\n"
            #args=args.replace("'","\\\"")#.replace("(","\\\\(").replace(")","\\\\)")
            f.write(args)
            f.write("Queue\n")
            
        for qcd in [["qcdnone",Weight("1")],["qcdmet",qcdEleMET],["qcdbdt",Weight("(bdt_qcd>0.55)")]]:
            args="Arguments = \"'--mode=plot' '--name=ele_"+category[0]+"_"+var[0]+"_"+qcd[0]+"' '--stackMC=MC_ele_single' '--stackData=data_ele' '--var="+var[0]+"' '--varName="+var[1]+"' '--unit="+var[2]+"' '--text=e+jets,--"+category[0]+",--18.9' '--weightMC="+(category[1]*qcd[1]*lumiEle).get()+"' '--weightData="+(category[1]*qcd[1]).get()+"' '--binning="+str(var[3]).replace(" ","")+"'\"\n"
            #args=args.replace("'","\\\"")#.replace("(","\\\\(").replace(")","\\\\)")
            f.write(args)
            f.write("Queue\n")
'''
            
for category in [["2j0t",c2j0t],["3j1t",c3j1t],["3j2t",c3j2t]]:
    for var in [
        ["bdt_sig_bg","BDT--t-chan.","",EquiBinning(50,-1,1)],
        
    ]:
        for qcd in [["qcdnone",Weight("1")],["qcdmtw",qcdMuMTW],["qcdbdt",Weight("(bdt_qcd>0.4)")]]:
            args="Arguments = \"'--mode=plot' '--name=mu_"+category[0]+"_"+var[0]+"_"+qcd[0]+"' '--stackMC=MC_mu_single' '--stackData=data_mu' '--var="+var[0]+"' '--varName="+var[1]+"' '--unit="+var[2]+"' '--text=#mu+jets,--"+category[0]+",--16.9' '--weightMC="+(category[1]*qcd[1]*lumiMu).get()+"' '--weightData="+(category[1]*qcd[1]).get()+"' '--binning="+str(var[3]).replace(" ","")+"'\"\n" 
            #args=args.replace("'","\\\"")#.replace("(","\\\\(").replace(")","\\\\)")
            f.write(args)
            f.write("Queue\n")
            
            Nbins=6
            for cosBin in range(Nbins):
                start=-1.0+cosBin*2.0/Nbins
                end=start+2.0/Nbins
                cutWeight=Weight("(cos_theta_lq>"+str(start)+")*(cos_theta_lq<"+str(end)+")")
                args="Arguments = \"'--mode=plot' '--name=mu_"+category[0]+"_"+var[0]+"_"+qcd[0]+"_cosBin"+str(cosBin)+"' '--stackMC=MC_mu_single' '--stackData=data_mu' '--var="+var[0]+"' '--varName="+var[1]+"' '--unit="+var[2]+"' '--text=#mu+jets,--"+category[0]+",--16.9' '--weightMC="+(category[1]*qcd[1]*lumiMu*cutWeight).get()+"' '--weightData="+(category[1]*qcd[1]*cutWeight).get()+"' '--binning="+str(var[3]).replace(" ","")+"'\"\n" 
                #args=args.replace("'","\\\"")#.replace("(","\\\\(").replace(")","\\\\)")
                f.write(args)
                f.write("Queue\n")

        for qcd in [["qcdnone",Weight("1")],["qcdmet",qcdEleMET],["qcdbdt",Weight("(bdt_qcd>0.55)")]]:
            args="Arguments = \"'--mode=plot' '--name=ele_"+category[0]+"_"+var[0]+"_"+qcd[0]+"' '--stackMC=MC_ele_single' '--stackData=data_ele' '--var="+var[0]+"' '--varName="+var[1]+"' '--unit="+var[2]+"' '--text=e+jets,--"+category[0]+",--18.9' '--weightMC="+(category[1]*qcd[1]*lumiEle).get()+"' '--weightData="+(category[1]*qcd[1]).get()+"' '--binning="+str(var[3]).replace(" ","")+"'\"\n"
            #args=args.replace("'","\\\"")#.replace("(","\\\\(").replace(")","\\\\)")
            f.write(args)
            f.write("Queue\n")
            
            Nbins=6
            for cosBin in range(Nbins):
                start=-1.0+cosBin*2.0/Nbins
                end=start+2.0/Nbins
                cutWeight=Weight("(cos_theta_lq>"+str(start)+")*(cos_theta_lq<"+str(end)+")")
                args="Arguments = \"'--mode=plot' '--name=ele_"+category[0]+"_"+var[0]+"_"+qcd[0]+"_cosBin"+str(cosBin)+"' '--stackMC=MC_ele_single' '--stackData=data_ele' '--var="+var[0]+"' '--varName="+var[1]+"' '--unit="+var[2]+"' '--text=e+jets,--"+category[0]+",--18.9' '--weightMC="+(category[1]*qcd[1]*lumiEle*cutWeight).get()+"' '--weightData="+(category[1]*qcd[1]*cutWeight).get()+"' '--binning="+str(var[3]).replace(" ","")+"'\"\n"
                #args=args.replace("'","\\\"")#.replace("(","\\\\(").replace(")","\\\\)")
                f.write(args)
                f.write("Queue\n")
            


for category in [["2j1t",c2j1t]]:
    for var in [
        ["bdt_sig_bg","BDT--t-chan.","",EquiBinning(50,-1,1)],
    ]:
        for qcd in [["qcdnone",Weight("1")],["qcdmtw",qcdMuMTW],["qcdbdt",Weight("(bdt_qcd>0.4)")]]:
            args="Arguments = \"'--mode=plot' '--name=mu_"+category[0]+"_"+var[0]+"_"+qcd[0]+"' '--stackMC=MC_mu_single' '--stackData=data_mu' '--var="+var[0]+"' '--varName="+var[1]+"' '--unit="+var[2]+"' '--text=#mu+jets,--"+category[0]+",--16.9' '--weightMC="+(category[1]*qcd[1]*lumiMu).get()+"' '--weightData="+(category[1]*qcd[1]*Weight("("+var[0]+"<0.0)")).get()+"' '--binning="+str(var[3]).replace(" ","")+"'\"\n"
            #args=args.replace("'","\\\"")#.replace("(","\\\\(").replace(")","\\\\)")
            f.write(args) 
            f.write("Queue\n")
            
            Nbins=6
            for cosBin in range(Nbins):
                start=-1.0+cosBin*2.0/Nbins
                end=start+2.0/Nbins
                cutWeight=Weight("(cos_theta_lq>"+str(start)+")*(cos_theta_lq<"+str(end)+")")
                args="Arguments = \"'--mode=plot' '--name=mu_"+category[0]+"_"+var[0]+"_"+qcd[0]+"_cosBin"+str(cosBin)+"' '--stackMC=MC_mu_single' '--stackData=data_mu' '--var="+var[0]+"' '--varName="+var[1]+"' '--unit="+var[2]+"' '--text=#mu+jets,--"+category[0]+",--16.9' '--weightMC="+(category[1]*qcd[1]*lumiMu*cutWeight).get()+"' '--weightData="+(category[1]*qcd[1]*cutWeight).get()+"' '--binning="+str(var[3]).replace(" ","")+"'\"\n" 
                #args=args.replace("'","\\\"")#.replace("(","\\\\(").replace(")","\\\\)")
                f.write(args)
                f.write("Queue\n")
                
        for qcd in [["qcdnone",Weight("1")],["qcdmet",qcdEleMET],["qcdbdt",Weight("(bdt_qcd>0.55)")]]:
            args="Arguments = \"'--mode=plot' '--name=ele_"+category[0]+"_"+var[0]+"_"+qcd[0]+"' '--stackMC=MC_ele_single' '--stackData=data_ele' '--var="+var[0]+"' '--varName="+var[1]+"' '--unit="+var[2]+"' '--text=e+jets,--"+category[0]+",--18.9' '--weightMC="+(category[1]*qcd[1]*lumiEle).get()+"' '--weightData="+(category[1]*qcd[1]*Weight("("+var[0]+"<0.0)")).get()+"' '--binning="+str(var[3]).replace(" ","")+"'\"\n"
            #args=args.replace("'","\\\"")#.replace("(","\\\\(").replace(")","\\\\)")
            f.write(args)
            f.write("Queue\n")
            
            Nbins=6
            for cosBin in range(Nbins):
                start=-1.0+cosBin*2.0/Nbins
                end=start+2.0/Nbins
                cutWeight=Weight("(cos_theta_lq>"+str(start)+")*(cos_theta_lq<"+str(end)+")")
                args="Arguments = \"'--mode=plot' '--name=ele_"+category[0]+"_"+var[0]+"_"+qcd[0]+"_cosBin"+str(cosBin)+"' '--stackMC=MC_ele_single' '--stackData=data_ele' '--var="+var[0]+"' '--varName="+var[1]+"' '--unit="+var[2]+"' '--text=e+jets,--"+category[0]+",--18.9' '--weightMC="+(category[1]*qcd[1]*lumiEle*cutWeight).get()+"' '--weightData="+(category[1]*qcd[1]*cutWeight).get()+"' '--binning="+str(var[3]).replace(" ","")+"'\"\n"
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

