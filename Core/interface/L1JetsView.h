#ifndef L1JetsView_h
#define L1JetsView_h

#include "CommonFSQFramework/Core/interface/EventViewBase.h"

class L1JetsView: public EventViewBase{
    public:
       L1JetsView(const edm::ParameterSet& ps, TTree * tree, edm::ConsumesCollector && iC);

    private:
      virtual void fillSpecific(const edm::Event&, const edm::EventSetup&);
      std::vector<edm::InputTag > m_todo;



};
#endif
