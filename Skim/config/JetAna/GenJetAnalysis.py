#!/usr/bin/env python
import CommonFSQFramework.Core.ExampleProofReader

import sys, os, time
sys.path.append(os.path.dirname(__file__))

import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import edm

from array import *

from math import pi

def compareJetPt(x,y):
    if x.pt() < y.pt(): return 1
    if x.pt() > y.pt(): return -1
    if x.pt() == y.pt(): return 0

class GenJetAnalysis(CommonFSQFramework.Core.ExampleProofReader.ExampleProofReader):
    def init(self):

        self.hist = {}
        self.hist["hNentries"] = ROOT.TH1F("hNentries","hNentries",3,-0.5,2.5)

        self.hist["hNak4GenJets"] =  ROOT.TH1F("hNak4GenJets","hNak4GenJets",100,-0.5, 99.5)

        self.hist["hdNdEak4GenJets"] =  ROOT.TH1F("hdNdEak4GenJets","hdNdEak4GenJets",50,0,5000)
        self.hist["hdNdPtak4GenJets"] =  ROOT.TH1F("hdNdPtak4GenJets","hdNdPtak4GenJets",50,0,25)

        self.hist["hdNdEtaak4GenJets"] =  ROOT.TH1F("hdNdEtaak4GenJets","hdNdEtaak4GenJets",60,-6,6)
        self.hist["hdNdEtaak4CaloJets"] =  ROOT.TH1F("hdNdEtaak4CaloJets","hdNdEtaak4CaloJets",60,-6,6)

        self.hist["hdNdEak5CastorJets"] =  ROOT.TH1F("hdNdEak5CastorJets","hdNdEak5CastorJets",50,0,5000)
        self.hist["hdNdPtak5CastorJets"] =  ROOT.TH1F("hdNdPtak5CastorJets","hdNdPtak5CastorJets",50,0,25)

        self.hist["hdNdPtHotCasGenJet"]       = ROOT.TH1F("hdNdPtHotCasGenJet","hdNdPtHotCasGenJet",50,0,25)
        self.hist["hdNdPtHotCenGenJet"]       = ROOT.TH1F("hdNdPtHotCenGenJet","hdNdPtHotCenGenJet",50,0,25)
        self.hist["hdNdDeltaPhiCasCenGenJet"] = ROOT.TH1F("hdNdDeltaPhiCasCenGenJet","hdNdDeltaPhiCasCenGenJet",50,-pi,pi)
        self.hist["hdNdDeltaPtCenCasGenJet"]  = ROOT.TH1F("hdNdDeltaPtCenCasGenJet","hdNdDeltaPtCenCasGenJet",40,-1,1)
        self.hist["hdNdDeltaEtaCenCasGenJet"] = ROOT.TH1F("hdNdDeltaEtaCenCasGenJet","hdNdDeltaEtaCenCasGenJet",20,0,10)

        self.hist["hDeltaPhiGenJetHotCasJet"] = ROOT.TH1F("hDeltaPhiGenJetHotCasJet","hDeltaPhiGenJetHotCasJet",50,-pi,pi)

        self.hist["hEGenJetVsECasJet"] = ROOT.TH2F("hEGenJetVsECasJet","hEGenJetVsECasJet",50,0,5000,50,0,5000)

        self.hist["pECasJetGenReco"] = ROOT.TProfile("pECasJetGenReco","pECasJetGenReco",50,0,5000)

        for h in self.hist:
            self.hist[h].Sumw2()
            self.GetOutputList().Add(self.hist[h])

    def analyze(self):
        weight = 1
        num = 0
        
        self.hist["hNentries"].Fill( 0, weight )

        num = self.fChain.ak4GenJetsp4.size()
        self.hist["hNak4GenJets"].Fill(num, weight)

        for jet in self.fChain.ak4GenJetsp4:
            self.hist["hdNdEtaak4GenJets"].Fill(jet.eta(), weight)

            if jet.eta() > -5.2 or jet.eta() < -6.4: continue
            self.hist["hdNdEak4GenJets"].Fill(jet.e(), weight)
            self.hist["hdNdPtak4GenJets"].Fill(jet.pt(), weight)

        for jet_eta in self.fChain.PFAK4Caloeta:
            self.hist["hdNdEtaak4CaloJets"].Fill(jet_eta, weight)

        CastorRecoJets = []
        for jet in self.fChain.ak5CastorJetsP4:
            if jet.eta() > -5.2 or jet.eta() < -6.4: continue
            self.hist["hdNdEak5CastorJets"].Fill(jet.e(), weight)
            self.hist["hdNdPtak5CastorJets"].Fill(jet.pt(), weight)

            if jet.eta() > -5.4 or jet.eta() < -6.2 or jet.e() < 500: continue
            CastorRecoJets.append(jet)

        CastorRecoJets.sort(cmp=compareJetPt)
        if len(CastorRecoJets) > 0:
            MergedGenCastorJet = None
            mindphi = 4.0
            for jet in self.fChain.ak4GenJetsp4:
                if jet.eta() > -5.4 or jet.eta() < -6.2: continue
                dphi = CastorRecoJets[0].phi() - jet.phi()
                if dphi < -pi: dphi = dphi+2*pi
                if dphi >  pi: dphi = dphi-2*pi

                self.hist["hDeltaPhiGenJetHotCasJet"].Fill( dphi, weight )

                if dphi < mindphi and dphi < pi/8.:
                    mindphi = dphi
                    MergedGenCastorJet = jet

            if MergedGenCastorJet:
                self.hist["hEGenJetVsECasJet"].Fill( CastorRecoJets[0].e(), MergedGenCastorJet.e(), weight )
                self.hist["pECasJetGenReco"].Fill( MergedGenCastorJet.e(), MergedGenCastorJet.e()/CastorRecoJets[0].e(), weight )


        CastorGenJets = []
        CentralGenJets = []
        for jet in self.fChain.ak4GenJetsp4:
            if jet.eta() > -5   and jet.eta() <  5  : CentralGenJets.append(jet)
            if jet.eta() > -6.4 and jet.eta() < -5.2: CastorGenJets.append(jet)

        CastorGenJets.sort(cmp=compareJetPt)
        CentralGenJets.sort(cmp=compareJetPt)

        nCasJet = len(CastorGenJets)
        nCenJet = len(CentralGenJets)

        if nCenJet > 1:
            if CentralGenJets[0].pt() < CentralGenJets[1].pt():
                raise Exception("Jet sort incorrect!!!")

        if nCasJet > 0: self.hist["hNentries"].Fill( 1, weight )

        if nCasJet > 0: self.hist["hdNdPtHotCasGenJet"].Fill( CastorGenJets[0].pt(), weight )
        if nCenJet > 0: self.hist["hdNdPtHotCenGenJet"].Fill( CentralGenJets[0].pt(), weight )

        if nCasJet == 0 or nCenJet == 0: return 1

        CasJet = CastorGenJets[0]
        CenJet = CentralGenJets[0]

        ptcut = 5
        if CasJet.pt() < ptcut or CenJet.pt() < ptcut: return 1

        dphi = CenJet.phi() - CasJet.phi()
        if dphi < -pi: dphi = dphi+2*pi
        if dphi >  pi: dphi = dphi-2*pi
        self.hist["hdNdDeltaPhiCasCenGenJet"].Fill( dphi, weight )

        if abs(dphi) < 2.7: return 1

        pcut = 0.2 * (CenJet.pt()+CasJet.pt())/2
        if nCasJet > 1:
            if CastorGenJets[1].pt() > pcut: return 1
        if nCenJet > 1:
            if CentralGenJets[1].pt() > pcut: return 1

        self.hist["hNentries"].Fill( 2, weight )

        dpt = (CenJet.pt()-CasJet.pt())/(CenJet.pt()+CasJet.pt())
        self.hist["hdNdDeltaPtCenCasGenJet"].Fill( dpt, weight )

        deta = CenJet.eta()-CasJet.eta()
        self.hist["hdNdDeltaEtaCenCasGenJet"].Fill( deta, weight )


        
        return 1

    def finalize(self):
        print "Finalize:"

        # normFactor = self.getNormalizationFactor()
        # print "  applying norm", normFactor
        # for h in self.hist:
            # self.hist[h].Scale(normFactor)

    def finalizeWhenMerged(self):
        olist =  self.GetOutputList() # rebuild the histos list
        histos = {}
        for o in olist:
            if not "TH1" in o.ClassName(): continue
            histos[o.GetName()]=o
            print " TH1 histogram in output: ", o.GetName()

        histos["hNak4GenJets"].Scale( 1./histos["hNentries"].GetBinContent(1) )

        histos["hdNdEak4GenJets"].Scale( 1./histos["hNentries"].GetBinContent(1) )
        histos["hdNdPtak4GenJets"].Scale( 1./histos["hNentries"].GetBinContent(1) )

        histos["hdNdEtaak4GenJets"].Scale( 1./histos["hNentries"].GetBinContent(1) )
        histos["hdNdEtaak4CaloJets"].Scale( 1./histos["hNentries"].GetBinContent(1) )

        histos["hdNdEak5CastorJets"].Scale( 1./histos["hNentries"].GetBinContent(1) )
        histos["hdNdPtak5CastorJets"].Scale( 1./histos["hNentries"].GetBinContent(1) )

        histos["hdNdPtHotCasGenJet"].Scale( 1./histos["hNentries"].GetBinContent(1) )
        histos["hdNdPtHotCenGenJet"].Scale( 1./histos["hNentries"].GetBinContent(1) )
        histos["hdNdDeltaPhiCasCenGenJet"].Scale( 1./histos["hNentries"].GetBinContent(1) )
        histos["hdNdDeltaPtCenCasGenJet"].Scale( 1./histos["hNentries"].GetBinContent(1) )
        histos["hdNdDeltaEtaCenCasGenJet"].Scale( 1./histos["hNentries"].GetBinContent(1) )

        # you can save further histograms to the output file by calling:
        #self.GetOutputList().Add(myNewHisto)
        
        pass


if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    ROOT.gSystem.Load("libFWCoreFWLite.so")
    ROOT.AutoLibraryLoader.enable()

    sampleList = None # run through all
    maxFilesMC = None # run through all files found
    maxFilesData = None # same
    nWorkers = None # Use all cpu cores

    # debug config:
    # Run printTTree.py alone to get the samples list
    # sampleList = []
    # sampleList.append("MinBias_TuneMonash13_13TeV-pythia8_MagnetOff")
    # maxFilesMC = 1
    # maxFilesData = 1
    # nWorkers = 1


    # slaveParams = {}
    # slaveParams["maxEta"] = 2.


    # use printTTree.py <sampleName> to see what trees are avaliable inside the skim file
    GenJetAnalysis.runAll(treeName="JetCastor",
           # slaveParameters=slaveParams,
           sampleList=sampleList,
           maxFilesMC = maxFilesMC,
           maxFilesData = maxFilesData,
           nWorkers=nWorkers,
           outFile = "plotsGenJetAnalysis.root" )
