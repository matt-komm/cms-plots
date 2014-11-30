#ifndef __PROJECTIONGROUP_H__
#define __PROJECTIONGROUP_H__

#include <vector>
#include <utility>
#include <algorithm>
#include <iostream>
#include <functional>
#include <cstdlib>

#ifndef __CINT__
#include <thread>
#include <mutex>
#endif

#include "Projector.hpp"
#include "TROOT.h"
#include "TSystem.h"
#include "TH1.h"

#ifndef __CINT__
static std::mutex _mutex;
#endif

class ProjectionGroup
{
    public:
        struct Status
        {
            enum {PENDING,STARTED,RUNNING,DONE} value;
            Status():
                value(PENDING)
            {
            }
            
        };
    protected:
        std::vector<std::pair<Status*,Projector*>> _projectors;
        TH1* _hist;
    public:
        typedef void* function_t( void* ) ;
    
        ProjectionGroup()
        {
        }
        ProjectionGroup(TH1* hist);
        void Add(Projector* projector)
        {
            _projectors.push_back(std::make_pair(new Status(),projector));
        }
        
        int getNextItem()
        {
            #ifndef __CINT__
            _mutex.lock();
            #endif
            int next = -1;
            for (unsigned int i = 0; i < _projectors.size(); ++i)
            {
                if (_projectors[i].first->value==Status::PENDING)
                {
                    next=i;
                    _projectors[i].first->value=Status::STARTED;
                    break;
                }
            }
            std::cout<<std::this_thread::get_id()<<", next: "<<next<<std::endl;
            #ifndef __CINT__
            _mutex.unlock();
            #endif
            
            return next;
        }
        
        void ProjectThreaded()
        {
            #ifndef __CINT__
            int next = getNextItem();
            while (next>=0)
            {
                _mutex.lock();
                _projectors[next].first->value=Status::RUNNING;
                _mutex.unlock();
                _projectors[next].second->Project();
                _mutex.lock();
                _projectors[next].first->value=Status::DONE;
                _hist->Add(_projectors[next].second->getHist());
                _mutex.unlock();
                
                 next = getNextItem();
                
            }
            #endif
        }
        
        void Project(unsigned int nthreads)
        {
            #ifndef __CINT__
            std::function<void()> fct = std::bind(&ProjectionGroup::ProjectThreaded,this);
            //fct();
            /*
            for (unsigned int i = 0; i < _projectors.size(); ++i)
            {
                std::cout<<i<<"/"<<_projectors.size()<<"\r";
                std::cout.flush();
                _projectors[i].second->Project();
                *?
            }
            std::cout<<std::endl;
            */
            std::vector<std::thread*> threads;

            
            for (unsigned int ithread = 0; ithread<std::min(nthreads, (unsigned int)_projectors.size()); ++ithread)
            {
                
                
                std::thread* t = new std::thread(fct);
                
                threads.push_back(t);
                
            }
            for (unsigned int ithread = 0; ithread<threads.size(); ++ithread)
            {
                threads[ithread]->join();
            }
            
            #endif
        }
        /*
        Class(const Class& c);
        Class(Class&& c);
        Class& operator=(const Class& c);
        Class& operator=(Class&& c);
        ~Class();
        */
};

#endif

