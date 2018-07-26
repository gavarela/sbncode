#include <algorithm>
#include <cassert>
#include <iostream>
#include <vector>
#include <TH2D.h>
#include <json/json.h>
#include "gallery/ValidHandle.h"
#include "canvas/Utilities/InputTag.h"
#include "nusimdata/SimulationBase/MCFlux.h"
#include "nusimdata/SimulationBase/MCTruth.h"
#include "nusimdata/SimulationBase/MCNeutrino.h"
#include "larsim/EventWeight/Base/MCEventWeight.h"
#include "ExampleSelection.h"
#include "ExampleTools.h"

namespace ana {
  namespace ExampleAnalysis {

ExampleSelection::ExampleSelection() : SelectionBase(), fNuCount(0), fEventCounter(0) {}


void ExampleSelection::Initialize(Json::Value* config) {
  // Make a histogram
  fNuVertexXZHist = new TH2D("nu_vtx_XZ", "",
                             100, -1000, 1000, 100, -1000, 1000);

  // Load configuration parameters
  fMyParam = 0;
  fTruthTag = { "generator" };

  if (config) {
    fMyParam = (*config)["ExampleAnalysis"].get("parameter", 0).asInt();
    fTruthTag = { (*config)["ExampleAnalysis"].get("MCTruthTag", "generator").asString() };
  }

  // Add custom branches
  AddBranch("nucount", &fNuCount);
  AddBranch("myvar", &fMyVar);
  AddBranch("parentPDG", &fParentPDG);

  // Use some library code
  hello();
}


void ExampleSelection::Finalize() {
  // Output our histograms to the ROOT file
  fOutputFile->cd();
  fNuVertexXZHist->Write();
}


bool ExampleSelection::ProcessEvent(gallery::Event& ev) {
  if (fEventCounter % 10 == 0) {
    std::cout << "ExampleSelection: Processing event " << fEventCounter << std::endl;
  }
  fEventCounter++;

  // Grab a data product from the event
  auto const& mctruths = *ev.getValidHandle<std::vector<simb::MCTruth>>(fTruthTag);
  auto const& mcfluxs = *ev.getValidHandle<std::vector<simb::MCFlux>>(fTruthTag);
  assert(mctruths.size() == mcfluxs.size());

  gallery::Handle<std::vector<evwgh::MCEventWeight> > wgh;
  bool hasWeights = ev.getByLabel({"genieeventweight"}, wgh);

  gallery::Handle<std::vector<evwgh::MCEventWeight> > wghf;
  bool hasWeightsf = ev.getByLabel({"fluxeventweight"}, wghf);

  std::vector<gallery::Handle<std::vector<evwgh::MCEventWeight> > > wghs = \
    { wgh, wghf };

  std::cout << "===== " << wgh->size() << std::endl;

  // Print weights
  for (auto const& ws : wghs) {
    for (auto const& w : *ws) {
      for (auto& it : w.fWeight) {
        printf("%50s ", it.first.c_str());
        for (size_t j=0; j<it.second.size(); j++) {
          if (it.second[j] < 1e-2 || it.second[j] > 10) {
            std::cout << "oh no! " << it.second[j] << " ";
          }
          if (j < std::min(10, (int)it.second.size())) {
            printf("%6.3f ", it.second[j]);
          }
        }
        printf("\n");
      }
    }
  }

  // Fill in the custom branches
  fNuCount = mctruths.size();  // Number of neutrinos in this event
  fMyVar = fMyParam;
  
  fParentPDG.clear();  // Clear this for each new event

  // Iterate through the neutrinos
  for (size_t i=0; i<mctruths.size(); i++) {
    auto const& mctruth = mctruths.at(i);
    auto const& mcflux = mcfluxs.at(i);

    // Fill neutrino vertex position histogram
    fNuVertexXZHist->Fill(mctruth.GetNeutrino().Nu().Vx(),
                          mctruth.GetNeutrino().Nu().Vz());

    fParentPDG.push_back(mcflux.fptype);
  }

  return true;
}

  }  // namespace ExampleAnalysis
}  // namespace ana


// This line must be included for all selections!
DECLARE_SBN_PROCESSOR(ana::ExampleAnalysis::ExampleSelection)

