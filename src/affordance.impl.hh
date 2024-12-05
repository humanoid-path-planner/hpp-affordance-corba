// Copyright (C) 2009, 2010 by Florent Lamiraux, Thomas Moulard, JRL.
//
// This file is part of the hpp-affordance-corba.
//
// This software is provided "as is" without warranty of any kind,
// either expressed or implied, including but not limited to the
// implied warranties of fitness for a particular purpose.
//
// See the COPYING file for more information.

#ifndef HPP_AFFORDANCE_CORBA_IMPL_HH
#define HPP_AFFORDANCE_CORBA_IMPL_HH
#include <coal/BVH/BVH_model.h>
#include <omniORB4/CORBA.h>

#include "affordance-idl.hh"
#include "hpp/corbaserver/affordance/fwd.hh"
#include "hpp/corbaserver/affordance/server.hh"
#include "hpp/corbaserver/problem-solver-map.hh"
#include "hpp/core/problem-solver.hh"

namespace hpp {
namespace affordanceCorba {
namespace impl {
class Afford : public virtual POA_hpp::corbaserver::affordance::Afford {
 public:
  Afford();

  void setServer(Server* server) { server_ = server; }

  Afford(const core::ProblemSolverPtr_t& problemSolver);

  void resetAffordanceConfig();

  affordance::OperationBases_t createOperations();

  void setAffordanceConfig(const char* affType, const hpp::doubleSeq& conf);

  hpp::doubleSeq* getAffordanceConfig(const char* affType);

  void setMargin(const char* affType, CORBA::Double margin);

  void setNeighbouringTriangleMargin(const char* affType,
                                     CORBA::Double nbTriMargin);

  void setMinimumArea(const char* affType, CORBA::Double minArea);

  bool checkModel(const char* obstacleName);

  void affordanceAnalysis(
      const char* obstacleName, const affordance::OperationBases_t& operations,
      std::vector<double> reduceSizes = std::vector<double>());

  void analyseObject(const char* obstacleName,
                     const hpp::doubleSeq& reduceSizesCorba);

  void analyseAll(const hpp::doubleSeq& reduceSizesCorba);

  void deleteAffordancesByType(const char* affordance,
                               const char* obstacleName);

  void deleteAffordances(const char* obstacleName);

  void addAffObjects(const affordance::OperationBases_t& ops,
                     const std::vector<affordance::CollisionObjects_t>& affObjs,
                     const char* obstacleName);

  hpp::doubleSeqSeqSeqSeq* getAffordancePoints(const char* affordance);

  hpp::Names_t* getAffRefObstacles(const char* affordance);

  hpp::Names_t* getAffordanceTypes();

  hpp::Names_t* getAffordanceConfigTypes();

 private:
  Server* server_;
  core::ProblemSolverPtr_t problemSolver() { return server_->problemSolver(); }
};  // class Afford
}  // namespace impl
}  // namespace affordanceCorba
}  // namespace hpp

#endif  // HPP_AFFORDANCE_CORBA_IMPL_HH
