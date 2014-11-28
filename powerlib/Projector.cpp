#include "Projector.hpp"
#include "TMath.h"
#include "TDirectory.h"
#include "TFile.h"
#include <math.h>

ClassImp(Projector)

Projector::Projector()
{
}

Projector::Projector(TH1* hist, TTree* tree, const char* varExp, const char* cutExp):
    _hist(hist),
    _tree(tree),
    _varFct("varFct",varExp,_tree),
    _cutFct("cutFct",cutExp,_tree)
    
{
    //_projectFct=(std::bind(&Projector::Project,this));
}

ProjectFct Projector::getProjectFct()
{
    return _projectFct;
}

void Projector::Print(long i) 
{
    _tree->GetEntry(i);
    std::cout << _varFct.EvalInstance() <<" "<<_cutFct.EvalInstance()<< std::endl;
}

void Projector::Project()
{   
    long last = _tree->GetEntries();
    /*
    if (max>=0)
    {
        last=std::min(max,last);
    }
    */
    for (long ientry = 0; ientry < last; ++ientry)
    {
        _tree->GetEntry(ientry);

        double var = _varFct.EvalInstance();
        double weight = _cutFct.EvalInstance();
        if (!std::isnan(var) && !std::isnan(weight) && !std::isinf(var) && !std::isinf(weight))
        {
            _hist->Fill(var,weight);
        }
    }
}
