#ifndef __PROJECTOR_H__
#define __PROJECTOR_H__

#include <iostream>
#include <functional>

#include "TObject.h"
#include "TTree.h"
#include "TTreeFormula.h"
#include "TH1.h"
#include "TThread.h"

typedef TThread::VoidRtnFunc_t ProjectFct;

class Projector
{
    public:
        
    private:
        TH1* _hist;
        TTree* _tree;
        TTreeFormula _varFct;
        TTreeFormula _cutFct;
        ProjectFct _projectFct;
    public:
    
        Projector();
        Projector(TH1* hist, TTree* tree, const char* varExp, const char* cutExp);
        void Print(long i=0);
        void Project();
        ProjectFct getProjectFct();
        
        inline const TH1* getHist() const
        {
            return _hist;
        }
        
        


    ClassDef(Projector, 1)
};

#endif

