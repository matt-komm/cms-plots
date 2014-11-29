#ifndef __PROJECTOR_H__
#define __PROJECTOR_H__

#include <iostream>
#include <functional>
#include <vector>
#include <string>

#include "TObject.h"
#include "TTree.h"
#include "TTreeFormula.h"
#include "TH1.h"
#include "TThread.h"
#include "TFile.h"
#include "TMemFile.h"



class Projector
{
    public:
        
    private:
        TH1* _hist;
        std::vector<std::string> _filenames;
        std::vector<std::string> _treenames;
        std::string _varExp;
        std::string _cutExp;
        
    public:
    
        Projector();
        Projector(TH1* hist, const char* filename, const char* treename, const char* varExp, const char* cutExp);
        
        void addFriend(const char* filename, const char* treename);
        void Project();
        
        inline const TH1* getHist() const
        {
            return _hist;
        }
        
        


    ClassDef(Projector, 1)
};

#endif

