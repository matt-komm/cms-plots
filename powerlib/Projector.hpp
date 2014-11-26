#ifndef __PROJECTOR_H__
#define __PROJECTOR_H__

#include <iostream>
#include "TObject.h"
#include "TTree.h"
#include "TTreeFormula.h"
#include "TH1.h"


class Projector: 
    public TObject 
{
    private:
        TH1* _hist;
        TTree* _tree;
        TTreeFormula _varFct;
        TTreeFormula _cutFct;
    public:
        Projector();
        Projector(TH1* hist, TTree* tree, const char* varExp, const char* cutExp);
        void Print(long i=0);
        void Project(long max=0);


    ClassDef(Projector, 1)
};

#endif

