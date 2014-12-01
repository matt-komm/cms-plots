#!/usr/bin/python

from optparse import OptionParser
from driver import *

#makePlot("mu_2j1t_top_pt","MC_mu_single","data_mu","top_pt","pT(top)","GeV","#mu+jets, 2j1t, 16.9",c2j1t+qcd+lumiMu,c2j1t+qcd,EquiBinning(50,0,250))
if __name__=="__main__":
    parser = OptionParser()
    parser.add_option("--name", dest="name", default="")
    parser.add_option("--stackMC", dest="stackMC", default="")
    parser.add_option("--stackData", dest="stackData", default="")
    parser.add_option("--var", dest="var", default="")
    parser.add_option("--varName", dest="varName", default="")
    parser.add_option("--unit", dest="unit", default="")
    parser.add_option("--text", dest="text", default="")
    parser.add_option("--weightMC", dest="weightMC", default="")
    parser.add_option("--weightData", dest="weightData", default="")
    parser.add_option("--binning", dest="binning", default="")
    (options, args) = parser.parse_args()
    
    print "name: ",options.name
    print "stackMC: ",options.stackMC
    print "stackData: ",options.stackData
    print "variable: ",options.var
    print "variable title: ",options.varName
    print "variable unit: ",options.unit
    print "text: ",options.text
    print "weight MC: ",options.weightMC
    print "weight data: ",options.weightData
    print "binning: ",options.binning
    
    makePlot(options.name,options.stackMC,options.stackData,
    options.var,options.varName,options.unit,options.text,Weight(options.weightMC),Weight(options.weightData),EquiBinning(*eval(options.binning)))
    
    
