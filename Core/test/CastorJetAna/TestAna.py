#!/usr/bin/env python
import CommonFSQFramework.Core.ExampleProofReader

import sys, os, time
sys.path.append(os.path.dirname(__file__))

import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import edm

from array import *

from math import pi
from math import sqrt
from math import log
from math import exp

import numpy as np
import numpy.ma as ma

def compareJetPt(x,y):
    if x.pt() < y.pt(): return 1
    if x.pt() > y.pt(): return -1
    if x.pt() == y.pt(): return 0

def compareSpecialListJetPt(x,y):
    return compareJetPt(x[0],y[0])

class TestAna(CommonFSQFramework.Core.ExampleProofReader.ExampleProofReader):
    def init(self):

        self.hist = {}
        self.hist["hNentries"] = ROOT.TH1F("hNentries","hNentries",3,-0.5,2.5)

        self.hist["bx"] = ROOT.TH1F("bx",";bx",4000,0,4000)
        self.hist["TrgCount"] = ROOT.TH1F("TrgCount","TrgCount",10,0,10)

        self.hist["run_lumi"] = ROOT.TH2F("run_lumi","run_lumi",500,500,1000,1500,0,1500)
        self.hist["run_lumi_TTCnt"] = ROOT.TH2F("run_lumi_TTCnt","run_lumi_TTCnt",500,500,1000,1500,0,1500)
        self.hist["run_lumi_AlgoCnt"] = ROOT.TH2F("run_lumi_AlgoCnt","run_lumi_AlgoCnt",500,500,1000,1500,0,1500)

        for h in self.hist:
            self.hist[h].Sumw2()
            self.GetOutputList().Add(self.hist[h])
                                
        self.TmpLorVec = ROOT.ROOT.Math.LorentzVector('ROOT::Math::PxPyPzE4D<double>')()


    def analyze(self):
        weight = 1
        num = 0
        
        self.hist["hNentries"].Fill( 0, weight )

        run  = self.fChain.run
        lumi = self.fChain.lumi
        bx   = self.fChain.bx

        CastorMedJetTrg  = self.fChain.trgCastorMedJet
        TTCastorMedJet   = self.fChain.trgl1L1GTTech[58]
        AlgoCastorMedJet = self.fChain.trgl1L1GTAlgo[100]

        # CastorHighJetTrg = self.fChain.trgl1L1GTTech[57] or self.fChain.trgl1L1GTAlgo[101]
        # ZeroBiasTrg      = self.fChain.trgZeroBias
        # MinBiasTrg       = self.fChain.trgMinBias
        # RandomTrg        = self.fChain.trgRandom
        # CastorDiJetTrg   = self.fChain.trgCastorDiJet

        self.hist["run_lumi"].Fill(run-247000,lumi)
        if TTCastorMedJet: self.hist["run_lumi_TTCnt"].Fill(run-247000,lumi)
        if AlgoCastorMedJet: self.hist["run_lumi_AlgoCnt"].Fill(run-247000,lumi)

        # # if run >= 247685: return 0
        # if self.isData and bx < 200:
        #     return 0

        # algo100prescale = self.getPrescaleAlog100(run,lumi)
        # if algo100prescale < 0: return 0


        return 1


    def finalize(self):
        print "Finalize:"

        # normFactor = self.getNormalizationFactor()
        # print "  applying norm", normFactor
        # for h in self.hist:
            # self.hist[h].Scale(normFactor)

    def finalizeWhenMerged(self):
        # olist =  self.GetOutputList() # rebuild the histos list
        # histos = {}
        # for o in olist:
        #     if not "TH1" in o.ClassName():
        #         if not "TH2" in o.ClassName():
        #             continue
        #     histos[o.GetName()]=o
        #     # print " TH1 histogram in output: ", o.GetName()        
        pass


if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    ROOT.gSystem.Load("libFWCoreFWLite.so")
    ROOT.AutoLibraryLoader.enable()

    sampleList = None # run through all
    maxFilesMC = None # run through all files found
    maxFilesData = None # same
    nWorkers = None #None # Use all cpu cores

    # debug config:
    # Run printTTree.py alone to get the samples list
    sampleList = []
    # sampleList.append("MinBias_TuneCUETP8M1_13TeV-pythia8")

    # sampleList.append("MinBias_TuneMBR_13TeV-pythia8_MagnetOff")
    # sampleList.append("MinBias_TuneMBR_13TeV-pythia8")

    # sampleList.append("ReggeGribovPartonMC_13TeV-QGSJetII")
    # sampleList.append("ReggeGribovPartonMC_13TeV-EPOS")

    # sampleList.append("ReggeGribovPartonMC_13TeV-EPOS_MagnetOff")
    # sampleList.append("ReggeGribovPartonMC_13TeV-QGSJetII_MagnetOff")

    # sampleList.append("data_ZeroBias1_Run2015A")
    # sampleList.append("data_L1MinimumBiasHF1_Run2015A")

    # sampleList.append("data_SumL1MinimumBiasHF_Run2015A")
    # sampleList.append("data_MelIntCalib_SumL1MinimumBiasHF_Run2015A")
    # sampleList.append("data_SumZeroBias_Run2015A")
    # sampleList.append("data_MelIntCalib_ZeroBias1_Run2015A")
    # sampleList.append("data_MelIntCalib_ZeroBias2_Run2015A")
    # sampleList.append("data_NoLED0to38IC_ZeroBias3_Run2015A")

    sampleList.append("data_CastorJets_Run2015A")
    # sampleList.append("ReggeGribovPartonMC_castorJet_13TeV-EPOS")

    # maxFilesMC = 50
    maxFilesData = 400
    # nWorkers = 1


    # slaveParams = {}
    # slaveParams["maxEta"] = 2.


    # use printTTree.py <sampleName> to see what trees are avaliable inside the skim file
    TestAna.runAll(treeName="JetCastor",
           # slaveParameters=slaveParams,
           sampleList=sampleList,
           maxFilesMC = maxFilesMC,
           maxFilesData = maxFilesData,
           nWorkers=nWorkers,
           outFile = "TEST.root" )
