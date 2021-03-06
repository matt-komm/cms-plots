#include "Projector.hpp"
#include "TMath.h"
#include "TDirectory.h"
#include "TFile.h"
#include <math.h>

ClassImp(Projector)

Projector::Projector()
{
}

Projector::Projector(TH1* hist, const char* filename, const char* treename, const char* varExp, const char* cutExp):
    _hist(hist),
    _varExp(varExp),
    _cutExp(cutExp)
{
    /*
    char buf[50];
    sprintf(buf,"hist_%s_%i",treename,rand());
    _hist = (TH1*)hist->Clone(buf);
    */
    
    _filenames.push_back(filename);
    _treenames.push_back(treename);
    //std::cout<<filename<<" "<<treename<<std::endl;
}

void Projector::addFriend(const char* filename, const char* treename)
{
    _filenames.push_back(filename);
    _treenames.push_back(treename);
    //std::cout<<filename<<" "<<treename<<std::endl;
}

void Projector::Project(long maxentries)
{   
    TFile* mainFile = new TFile(_filenames[0].c_str());
    TTree* tree = (TTree*)(mainFile->Get(_treenames[0].c_str()));
    
    if (!tree)
    {
        std::cout<<"Tree '"<<_treenames[0].c_str()<<"' not found in file '"<<_filenames[0].c_str()<<std::endl;
        return;
    }
    for (unsigned int i = 1; i < _filenames.size(); ++i)
    {
        tree->AddFriend(_treenames[i].c_str(),_filenames[i].c_str());
    }
    
    tree->GetEntry(0);
    char varFctName[50];
    char cutFctName[50];
    sprintf(varFctName,"varFct_%s_%i",_treenames[0].c_str(),rand());
    sprintf(cutFctName,"cutFct_%s_%i",_treenames[0].c_str(),rand());
    TTreeFormula varFct(varFctName,_varExp.c_str(),tree);
    TTreeFormula cutFct(cutFctName,_cutExp.c_str(),tree);
    if (maxentries==0)
    {
        maxentries=tree->GetEntries();
    }
    for (long ientry = 0; ientry < std::min((Long64_t)maxentries,tree->GetEntries()); ++ientry)
    {
        tree->GetEntry(ientry);
        
        double var = varFct.EvalInstance();
        double weight = cutFct.EvalInstance();
        if (!std::isnan(var) && !std::isnan(weight) && !std::isinf(var) && !std::isinf(weight))
        {
            _hist->Fill(var,weight);
        }
    }
    mainFile->Close();  
}   
