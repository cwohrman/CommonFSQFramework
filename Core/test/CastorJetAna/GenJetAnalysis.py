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

def compareJetPt(x,y):
    if x.pt() < y.pt(): return 1
    if x.pt() > y.pt(): return -1
    if x.pt() == y.pt(): return 0

def compareSpecialListJetPt(x,y):
    return compareJetPt(x[0],y[0])

class GenJetAnalysis(CommonFSQFramework.Core.ExampleProofReader.ExampleProofReader):
    def init(self):

        self.hist = {}
        self.hist["hNentries"] = ROOT.TH1F("hNentries","hNentries",3,-0.5,2.5)

        if not self.isData:
            self.hist["hNak5GenJets"]      =  ROOT.TH1F("hNak5GenJets","hNak5GenJets",100,-0.5, 99.5)
            self.hist["hdNdEak5GenJets"]   =  ROOT.TH1F("hdNdEak5GenJets","hdNdEak5GenJets",50,0,5000)
            self.hist["hdNdPtak5GenJets"]  =  ROOT.TH1F("hdNdPtak5GenJets","hdNdPtak5GenJets",50,0,25)
            self.hist["hdNdEtaak5GenJets"] =  ROOT.TH1F("hdNdEtaak5GenJets","hdNdEtaak5GenJets",60,-6,6)

            self.hist["hDeltaPhiGenJetHotCasJet"] = ROOT.TH1F("hDeltaPhiGenJetHotCasJet","hDeltaPhiGenJetHotCasJet",50,-pi,pi)
            self.hist["hEGenJetVsECasJet"]        = ROOT.TH2F("hEGenJetVsECasJet","hEGenJetVsECasJet",100,0,5000,100,0,5000)
            self.hist["hPtGenJetVsPtCasJet"]      = ROOT.TH2F("hPtGenJetVsPtCasJet","hPtGenJetVsPtCasJet",100,0,20,100,0,20)
            self.hist["pECasJetGenReco"]          = ROOT.TProfile("pECasJetGenReco","pECasJetGenReco",50,0,5000)

            self.hist["hdNdPtHotCasGenJet"]       = ROOT.TH1F("hdNdPtHotCasGenJet","hdNdPtHotCasGenJet",50,0,25)
            self.hist["hdNdPtHotCenGenJet"]       = ROOT.TH1F("hdNdPtHotCenGenJet","hdNdPtHotCenGenJet",50,0,25)
            self.hist["hdNdDeltaPhiCasCenGenJet"] = ROOT.TH1F("hdNdDeltaPhiCasCenGenJet","hdNdDeltaPhiCasCenGenJet",50,-pi,pi)
            self.hist["hdNdDeltaPtCenCasGenJet"]  = ROOT.TH1F("hdNdDeltaPtCenCasGenJet","hdNdDeltaPtCenCasGenJet",40,-1,1)
            self.hist["hdNdDeltaEtaCenCasGenJet"] = ROOT.TH1F("hdNdDeltaEtaCenCasGenJet","hdNdDeltaEtaCenCasGenJet",20,0,10)


        self.hist["hdNdEtaak4CaloJets"]  =  ROOT.TH1F("hdNdEtaak4CaloJets","hdNdEtaak4CaloJets",60,-6,6)

        self.hist["hdNdEak5CastorJets"]  =  ROOT.TH1F("hdNdEak5CastorJets","hdNdEak5CastorJets",50,0,5000)
        self.hist["hdNdPtak5CastorJets"] =  ROOT.TH1F("hdNdPtak5CastorJets","hdNdPtak5CastorJets",50,0,25)
        self.hist["hNTowak5CastorJets"]  =  ROOT.TH1F("hNTowak5CastorJets","hNTowak5CastorJets",7,-0.5,6.5)

        for h in self.hist:
            self.hist[h].Sumw2()
            self.GetOutputList().Add(self.hist[h])

        # self.SectorBorders = [ 0.,    pi/8.,    pi/4.,  3*pi/8.,  pi/2.,  5*pi/8., 3*pi/4., 7*pi/8., 
        #                        pi, -7*pi/8., -3*pi/4., -5*pi/8., -pi/2., -3*pi/8.,  -pi/4.,  -pi/8. ]
                                

    # returns phi in the range of [-pi,pi]
    def movePhiRange(self,phi):
        if phi < -pi: phi = phi+2*pi
        if phi >  pi: phi = phi-2*pi
        return phi

    # get delta phi of two objects in the range of [-pi,pi]
    # both objetcts need a memberfunction 'phi()'
    def getDphi(self,A,B):
        return self.movePhiRange( A.phi() - B.phi() )

    # get distance in R = sqrt( dphi^2 + deta^2 ) of two objects
    # both objects need the memberfunctions 'phi()' and 'eta()'
    def getDcone(self,A,B):
        dphi = self.getDphi(A,B)
        deta = A.eta() - B.eta()
        return sqrt( dphi*dphi + deta*deta )

    # returns true if a second gen jet which is not the merged one
    # overlays with the reco jet
    def secondGenJetOverlay(self,MergedGenCastorJet,HottestCastorJet,radius=0.5):
        for jet in self.fChain.ak5GenJetsp4:
            if jet == MergedGenCastorJet: continue
            dRecoJet = self.getDcone(HottestCastorJet,jet)

            if dRecoJet < radius+radius: return True

        return False

    # returns true if a genparticle in the RecoJet cone
    # but not in the GenJet cone
    def particleInRecoNotGenCone(self,MergedGenCastorJet,HottestCastorJet,radius=0.5):
        for gpart in self.fChain.genParticlesp4:
            if gpart.eta() > -5.2 or gpart.eta() < -6.6: continue

            dRecoJet = self.getDcone(HottestCastorJet,gpart)
            dGenJet = self.getDcone(MergedGenCastorJet,gpart)

            if dRecoJet < radius and dGenJet > radius: return True

        return False

    def jetPreCut(self, jet):
        return (jet.eta() > -5.7 or jet.eta() < -6.1 or jet.pt() < 1 or jet.e() < 250)


    def testFcn(self,HottestCastorJet,nTowers):
        phi = HottestCastorJet.phi()
        if phi < 0: phi = 2*pi + phi

        sec_nbr_inf = int(8.*phi/pi)
        sec_nbr_sup = sec_nbr_inf+1

        if nTower == 1:
            phi_inf = self.movePhiRange(sec_nbr_inf*pi/8.)
            phi_sup = self.movePhiRange(sec_nbr_sup*pi/8.)
            return phi_inf, phi_sup

            if (8.*phi/pi)%sec_nbr_inf < 0.5:
                return 0, 0

        return 0, 0

    def analyze(self):
        weight = 1
        num = 0
        
        self.hist["hNentries"].Fill( 0, weight )

        NCastorRecoJets = self.fChain.ak5CastorJetsP4.size()
        if NCastorRecoJets == 0:
            return 0

        CastorRecoJets = []
        for ijet in xrange(0,NCastorRecoJets):
            jet = self.fChain.ak5CastorJetsP4[ijet]
            nTow = self.fChain.ak5CastorJetsnTowers[ijet]

            self.hist["hdNdEak5CastorJets"].Fill(jet.e(), weight) 
            self.hist["hdNdPtak5CastorJets"].Fill(jet.pt(), weight)
            self.hist["hNTowak5CastorJets"].Fill(nTow, weight)

            if self.jetPreCut(jet): continue
            CastorRecoJets.append([jet,nTow])

        CastorRecoJets.sort(cmp=compareSpecialListJetPt)

        if not self.isData:
            num = self.fChain.ak5GenJetsp4.size()
            self.hist["hNak5GenJets"].Fill(num, weight)

            for jet in self.fChain.ak5GenJetsp4:
                self.hist["hdNdEtaak5GenJets"].Fill(jet.eta(), weight)

                if jet.eta() > -5.7 or jet.eta() < -6.1: continue
                self.hist["hdNdEak5GenJets"].Fill(jet.e(), weight)
                self.hist["hdNdPtak5GenJets"].Fill(jet.pt(), weight)

            MergedGenCastorJet = None
            isIsolated = True
            if len(CastorRecoJets) > 0:
                mindphi = 0.2
                HottestCastorJet = CastorRecoJets[0][0]
                NTowerHotCastorJet = CastorRecoJets[0][1]

                for jet in self.fChain.ak5GenJetsp4:
                    if self.jetPreCut(jet): continue
                    dphi = self.getDphi(HottestCastorJet,jet)

                    self.hist["hDeltaPhiGenJetHotCasJet"].Fill( dphi, weight )

                    if dphi < mindphi:
                        mindphi = dphi
                        MergedGenCastorJet = jet

                if MergedGenCastorJet:
                    if self.secondGenJetOverlay(MergedGenCastorJet,HottestCastorJet):
                        isIsolated = False

                if MergedGenCastorJet and isIsolated:
                    if self.particleInRecoNotGenCone(MergedGenCastorJet,HottestCastorJet):
                        isIsolated = False

                if MergedGenCastorJet and isIsolated:
                    self.hist["hEGenJetVsECasJet"].Fill( HottestCastorJet.e(), MergedGenCastorJet.e(), weight )
                    self.hist["hPtGenJetVsPtCasJet"].Fill( HottestCastorJet.pt(), MergedGenCastorJet.pt(), weight )
                    self.hist["pECasJetGenReco"].Fill( HottestCastorJet.e(), MergedGenCastorJet.e()/HottestCastorJet.e(), weight )

        for jet_eta in self.fChain.PFAK4Caloeta:
            self.hist["hdNdEtaak4CaloJets"].Fill(jet_eta, weight)


        if not self.isData:
            CastorGenJets = []
            CentralGenJets = []
            for jet in self.fChain.ak5GenJetsp4:
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

            dphi = self.movePhiRange( CenJet.phi() - CasJet.phi() )
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
            if not "TH1" in o.ClassName():
                if not "TH2" in o.ClassName():
                    continue
            histos[o.GetName()]=o
            print " TH1 histogram in output: ", o.GetName()

        if not self.isData:
            histos["hNak5GenJets"].Scale( 1./histos["hNentries"].GetBinContent(1) )

            histos["hdNdEak5GenJets"].Scale( 1./histos["hNentries"].GetBinContent(1) )
            histos["hdNdPtak5GenJets"].Scale( 1./histos["hNentries"].GetBinContent(1) )
            histos["hdNdEtaak5GenJets"].Scale( 1./histos["hNentries"].GetBinContent(1) )

            histos["hdNdPtHotCasGenJet"].Scale( 1./histos["hNentries"].GetBinContent(1) )
            histos["hdNdPtHotCenGenJet"].Scale( 1./histos["hNentries"].GetBinContent(1) )
            histos["hdNdDeltaPhiCasCenGenJet"].Scale( 1./histos["hNentries"].GetBinContent(1) )
            histos["hdNdDeltaPtCenCasGenJet"].Scale( 1./histos["hNentries"].GetBinContent(1) )
            histos["hdNdDeltaEtaCenCasGenJet"].Scale( 1./histos["hNentries"].GetBinContent(1) )

        histos["hdNdEtaak4CaloJets"].Scale( 1./histos["hNentries"].GetBinContent(1) )

        histos["hdNdEak5CastorJets"].Scale( 1./histos["hNentries"].GetBinContent(1) )
        histos["hdNdPtak5CastorJets"].Scale( 1./histos["hNentries"].GetBinContent(1) )
        histos["hNTowak5CastorJets"].Scale( 1./histos["hNentries"].GetBinContent(1) )

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
    sampleList = []
    sampleList.append("MinBias_TuneCUETP8M1_13TeV-pythia8")
    # sampleList.append("data_ZeroBias_Run2015A")
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
