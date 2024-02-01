//
// structs used to record MVAResult information into TrkAna tree
// Andy Edmonds (January 2024)
//
#ifndef MVAResultInfo_HH
#define MVAResultInfo_HH
#include "Rtypes.h"
namespace mu2e
{
// general info about the SimParticle which was simulated
  struct MVAResultInfo {
    Float_t result = -1.0; // the result of the MVA
    void reset() { *this = MVAResultInfo(); }
  };
}
#endif
