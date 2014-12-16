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



f = open("hists.condor","w")
f.write("Universe   = vanilla\n")
f.write("Executable = run.sh\n")
f.write("Log        = /dev/null\n")
f.write("Output     = log/log$(Process).out\n")
f.write("Error      = log/log$(Process).error\n")
f.write("should_transfer_files = NO\n")
f.write("when_to_transfer_output = NEVER\n")
f.write("requirements   = (CMSFARM =?= TRUE)\n")



            
for category in [["2j0t",c2j0t],["3j1t",c3j1t],["3j2t",c3j2t]]:
    for var in [
        ["bdt_sig_bg","BDT--t-chan.","",EquiBinning(50,-1,1)],
        
    ]:
        for qcd in [["qcdnone",Weight("1")],["qcdmtw",qcdMuMTW],["qcdbdt",Weight("(bdt_qcd>0.4)")]]:
            args="Arguments = \"'--mode=hist' '--name=mu_"+category[0]+"' '--stackMC=MC_mu_single' '--stackData=data_mu' '--var="+var[0]+"' '--varName="+var[1]+"' '--unit="+var[2]+"' '--text=#mu+jets,--"+category[0]+",--16.9' '--weightMC="+(category[1]*qcd[1]*lumiMu).get()+"' '--weightData="+(category[1]*qcd[1]).get()+"' '--binning="+str(var[3]).replace(" ","")+"'\"\n" 
            #args=args.replace("'","\\\"")#.replace("(","\\\\(").replace(")","\\\\)")
            f.write(args)
            f.write("Queue\n")

        for qcd in [["qcdnone",Weight("1")],["qcdmet",qcdEleMET],["qcdbdt",Weight("(bdt_qcd>0.55)")]]:
            args="Arguments = \"'--mode=hist' '--name=ele_"+category[0]+"' '--stackMC=MC_ele_single' '--stackData=data_ele' '--var="+var[0]+"' '--varName="+var[1]+"' '--unit="+var[2]+"' '--text=e+jets,--"+category[0]+",--18.9' '--weightMC="+(category[1]*qcd[1]*lumiEle).get()+"' '--weightData="+(category[1]*qcd[1]).get()+"' '--binning="+str(var[3]).replace(" ","")+"'\"\n"
            #args=args.replace("'","\\\"")#.replace("(","\\\\(").replace(")","\\\\)")
            f.write(args)
            f.write("Queue\n")

for category in [["2j1t",c2j1t*Weight("(bdt_sig_bg<0.0)")]]:
    for var in [
        ["bdt_sig_bg","BDT--t-chan.","",EquiBinning(50,-1,1)],
    ]:
        for qcd in [["qcdnone",Weight("1")],["qcdmtw",qcdMuMTW],["qcdbdt",Weight("(bdt_qcd>0.4)")]]:
            args="Arguments = \"'--mode=hist' '--name=mu_"+category[0]+"' '--stackMC=MC_mu_single' '--stackData=data_mu' '--var="+var[0]+"' '--varName="+var[1]+"' '--unit="+var[2]+"' '--text=#mu+jets,--"+category[0]+",--16.9' '--weightMC="+(category[1]*qcd[1]*lumiMu).get()+"' '--weightData="+(category[1]*qcd[1]).get()+"' '--binning="+str(var[3]).replace(" ","")+"'\"\n"
            #args=args.replace("'","\\\"")#.replace("(","\\\\(").replace(")","\\\\)")
            f.write(args) 
            f.write("Queue\n")
        for qcd in [["qcdnone",Weight("1")],["qcdmet",qcdEleMET],["qcdbdt",Weight("(bdt_qcd>0.55)")]]:
            args="Arguments = \"'--mode=hist' '--name=ele_"+category[0]+"' '--stackMC=MC_ele_single' '--stackData=data_ele' '--var="+var[0]+"' '--varName="+var[1]+"' '--unit="+var[2]+"' '--text=e+jets,--"+category[0]+",--18.9' '--weightMC="+(category[1]*qcd[1]*lumiEle).get()+"' '--weightData="+(category[1]*qcd[1]).get()+"' '--binning="+str(var[3]).replace(" ","")+"'\"\n"
            #args=args.replace("'","\\\"")#.replace("(","\\\\(").replace(")","\\\\)")
            f.write(args)
            f.write("Queue\n")
f.close()
            


