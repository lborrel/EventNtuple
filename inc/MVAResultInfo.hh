//
// struct to place results from MVA/ML/AI algorithms
//
#ifndef MVAResultInfo_HH
#define MVAResultInfo_HH
//FIXME#include "Offline/RecoDataProducts/inc/MVAResult.hh"
#include "Rtypes.h"
#include <string>
namespace mu2e
{
  struct MVAResultInfo {
    static const int MAX_MVAS = 50;

    MVAResultInfo() {
      n_mvas = 0;
      reset();
    }

    const std::string leafname(std::vector<std::string> labels) {
      std::string leaves = "nmvas/I:";
      for (std::vector<std::string>::const_iterator i_label = labels.begin(); i_label != labels.end(); ++i_label) {
        leaves += *i_label + "/F";
        if (i_label != labels.end()-1) {
          leaves += ":";
        }
      }
      n_mvas = labels.size();
      return leaves;
    }

    const std::vector<std::string> leafnames(std::vector<std::string> labels) {
      std::vector<std::string> leaves;
      for (std::vector<std::string>::const_iterator i_label = labels.begin(); i_label != labels.end(); ++i_label) {
        leaves.push_back(*i_label);
      }
      n_mvas = labels.size();
      return leaves;
    }

    void setMVA(const std::vector<Float_t>& mvas) {
      for (unsigned int i_mva = 0; i_mva < mvas.size(); ++i_mva) {
        _mvas[i_mva] = mvas.at(i_mva);
      }
    }

    void reset() {
      for (auto& i_mva : _mvas) {
        i_mva = -1.0;
      }
    }

    Int_t n_mvas;
    Float_t _mvas[MAX_MVAS];
  };
}
#endif
