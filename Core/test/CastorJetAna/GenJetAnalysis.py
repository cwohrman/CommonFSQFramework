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

        self.hist["bx"] = ROOT.TH1F("bx",";bx",4000,0,4000)
        self.hist["bx_MB"] = ROOT.TH1F("bx_MB","bx_MB",4000,0,4000)
        self.hist["bx_MedJet"] = ROOT.TH1F("bx_MedJet","bx_MedJet",4000,0,4000)

        self.hist["TrgCount"] = ROOT.TH1F("TrgCount","TrgCount",10,0,10)

        if not self.isData:
            self.hist["hNak5GenJets"]      =  ROOT.TH1F("hNak5GenJets","hNak5GenJets",100,-0.5, 99.5)
            self.hist["hdNdEak5GenJets"]   =  ROOT.TH1F("hdNdEak5GenJets","hdNdEak5GenJets",50,0,5000)
            self.hist["hdNdPtak5GenJets"]  =  ROOT.TH1F("hdNdPtak5GenJets","hdNdPtak5GenJets",50,0,25)
            self.hist["hdNdEtaak5GenJets"] =  ROOT.TH1F("hdNdEtaak5GenJets","hdNdEtaak5GenJets",60,-6,6)

            self.hist["hDeltaPhiGenJetHotCasJet"] = ROOT.TH1F("hDeltaPhiGenJetHotCasJet","hDeltaPhiGenJetHotCasJet",50,-pi,pi)
            self.hist["hEGenJetVsECasJet"]        = ROOT.TH2F("hEGenJetVsECasJet","hEGenJetVsECasJet",100,0,5000,100,0,5000)
            self.hist["hPtGenJetVsPtCasJet"]      = ROOT.TH2F("hPtGenJetVsPtCasJet","hPtGenJetVsPtCasJet",100,0,20,100,0,20)

            bb = array('d',[])
            nb = 3
            bmin = 250.
            bmax = 2500.
            for i in range(nb+1):
                b = log(bmin) + i*(log(bmax)-log(bmin))/nb
                bb.append(exp(b))

            self.hist["pECasJetGenReco"]          = ROOT.TProfile("pECasJetGenReco","pECasJetGenReco",len(bb)-1,bb)
            self.hist["ptest"]                    = ROOT.TProfile("ptest","ptest",len(bb)-1,bb)

            self.hist["hdNdPtHotCasGenJet"]       = ROOT.TH1F("hdNdPtHotCasGenJet","hdNdPtHotCasGenJet",50,0,25)
            self.hist["hdNdPtHotCenGenJet"]       = ROOT.TH1F("hdNdPtHotCenGenJet","hdNdPtHotCenGenJet",50,0,25)
            self.hist["hdNdDeltaPhiCasCenGenJet"] = ROOT.TH1F("hdNdDeltaPhiCasCenGenJet","hdNdDeltaPhiCasCenGenJet",50,-pi,pi)
            self.hist["hdNdDeltaPtCenCasGenJet"]  = ROOT.TH1F("hdNdDeltaPtCenCasGenJet","hdNdDeltaPtCenCasGenJet",40,-1,1)
            self.hist["hdNdDeltaEtaCenCasGenJet"] = ROOT.TH1F("hdNdDeltaEtaCenCasGenJet","hdNdDeltaEtaCenCasGenJet",20,0,10)


        self.hist["hdNdEtaak4CaloJets"]  =  ROOT.TH1F("hdNdEtaak4CaloJets","hdNdEtaak4CaloJets",60,-6,6)

        self.hist["hdNdEak5CastorJets"]  =  ROOT.TH1F("hdNdEak5CastorJets","hdNdEak5CastorJets",50,0,5000)
        self.hist["hdNdPtak5CastorJets"] =  ROOT.TH1F("hdNdPtak5CastorJets","hdNdPtak5CastorJets",50,0,25)
        self.hist["hNTowak5CastorJets"]  =  ROOT.TH1F("hNTowak5CastorJets","hNTowak5CastorJets",7,-0.5,6.5)

        self.hist["hdNdEak5CastorJetsHOT"]             =  ROOT.TH1F("hdNdEak5CastorJetsHOT","hdNdEak5CastorJetsHOT",30,0,7500)
        self.hist["hdNdEak5CastorJetsHOT_TrgMedJet"]   =  ROOT.TH1F("hdNdEak5CastorJetsHOT_TrgMedJet","hdNdEak5CastorJetsHOT_TrgMedJet",30,0,7500)
        self.hist["hdNdEak5CastorJetsHOT_TrgHighJet"]  =  ROOT.TH1F("hdNdEak5CastorJetsHOT_TrgHighJet","hdNdEak5CastorJetsHOT_TrgHighJet",30,0,7500)
        self.hist["hdNdEak5CastorJetsHOT_TrgZeroBias"] =  ROOT.TH1F("hdNdEak5CastorJetsHOT_TrgZeroBias","hdNdEak5CastorJetsHOT_TrgZeroBias",30,0,7500)
        self.hist["hdNdEak5CastorJetsHOT_TrgMinBias"]  =  ROOT.TH1F("hdNdEak5CastorJetsHOT_TrgMinBias","hdNdEak5CastorJetsHOT_TrgMinBias",30,0,7500)
        self.hist["hdNdEak5CastorJetsHOT_TrgRandom"]   =  ROOT.TH1F("hdNdEak5CastorJetsHOT_TrgRandom","hdNdEak5CastorJetsHOT_TrgRandom",30,0,7500)
        self.hist["hdNdPtak5CastorJetsHOT"]             =  ROOT.TH1F("hdNdPtak5CastorJetsHOT","hdNdPtak5CastorJetsHOT",25,0,25)
        self.hist["hdNdPtak5CastorJetsHOT_TrgMedJet"]   =  ROOT.TH1F("hdNdPtak5CastorJetsHOT_TrgMedJet","hdNdPtak5CastorJetsHOT_TrgMedJet",25,0,25)
        self.hist["hdNdPtak5CastorJetsHOT_TrgHighJet"]  =  ROOT.TH1F("hdNdPtak5CastorJetsHOT_TrgHighJet","hdNdPtak5CastorJetsHOT_TrgHighJet",25,0,25)
        self.hist["hdNdPtak5CastorJetsHOT_TrgZeroBias"] =  ROOT.TH1F("hdNdPtak5CastorJetsHOT_TrgZeroBias","hdNdPtak5CastorJetsHOT_TrgZeroBias",25,0,25)
        self.hist["hdNdPtak5CastorJetsHOT_TrgMinBias"]  =  ROOT.TH1F("hdNdPtak5CastorJetsHOT_TrgMinBias","hdNdPtak5CastorJetsHOT_TrgMinBias",25,0,25)
        self.hist["hdNdPtak5CastorJetsHOT_TrgRandom"]   =  ROOT.TH1F("hdNdPtak5CastorJetsHOT_TrgRandom","hdNdPtak5CastorJetsHOT_TrgRandom",25,0,25)


        self.hist["hEvsFem_ak5CastorJetsHOT_TrgMedJet"]  = ROOT.TH2F("hEvsFem_ak5CastorJetsHOT_TrgMedJet","hEvsFem_ak5CastorJetsHOT_TrgMedJet",30,0,7500,10,0,1)
        self.hist["hEvsFem_ak5CastorJetsHOT_TrgHighJet"] = ROOT.TH2F("hEvsFem_ak5CastorJetsHOT_TrgHighJet","hEvsFem_ak5CastorJetsHOT_TrgHighJet",30,0,7500,10,0,1)

        self.hist["htest"] = ROOT.TH2F("htest","htest",100,-pi,pi,100,-pi,3*pi)
        self.hist["htest2"] = ROOT.TH2F("htest2","htest2",100,0,10,100,0,2*pi)



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


    def phiJetSectorRange(self,HottestCastorJet,nTowers):
        phi = HottestCastorJet.phi()
        if phi < 0: phi = 2*pi + phi

        sec_nbr_inf = int(8.*phi/pi)
        sec_nbr_sup = sec_nbr_inf+1

        closer_border = int(16.*phi/pi)%2

        if nTowers == 2:
            if closer_border == 0:
                sec_nbr_inf -= 1
            else:
                sec_nbr_sup += 1

        if nTowers == 3:
            sec_nbr_inf -= 1
            sec_nbr_sup += 1

        if nTowers == 4:
            if closer_border == 0:
                sec_nbr_inf -= 2
                sec_nbr_sup += 1
            else:
                sec_nbr_inf -= 1
                sec_nbr_sup += 2

        sec_nbr_inf = (sec_nbr_inf+16)%16
        sec_nbr_sup = (sec_nbr_sup+16)%16

        phi_inf = self.movePhiRange( sec_nbr_inf*pi/8. )
        phi_sup = self.movePhiRange( sec_nbr_sup*pi/8. )

        phi_inf =  self.movePhiRange( sec_nbr_inf*pi/8. )
        phi_sup =  self.movePhiRange( sec_nbr_sup*pi/8. )

        return phi_inf, phi_sup

    def insideJetSector(self,phi_part,HottestCastorJet,nTowers):
        phi_inf, phi_sup = self.phiJetSectorRange(HottestCastorJet,nTowers)

        if phi_part > phi_inf and phi_part < phi_sup:
            return True
        if phi_inf > 0 and phi_sup < 0:
            if phi_part > phi_inf or phi_part < phi_sup:
                return True

        return False

    def particleInRecoJetSectorNotGenCone(self,MergedGenCastorJet,HottestCastorJet,nTowers,radius=0.5):
        for gpart in self.fChain.genParticlesp4:
            if gpart.eta() > -5.2 or gpart.eta() < -6.6: continue

            dGenJet = self.getDcone(MergedGenCastorJet,gpart)
            if dGenJet < radius: continue

            if self.insideJetSector(gpart.phi(),HottestCastorJet,nTowers):
                return True

        return False


    def getPrescaleAlog100(self, run, lumi):
        if run < 247612: return 10
        if run == 247612:
            if lumi < 34: return 10
            return 100
        if run < 247642: return 10
        if run == 247642:
            if lumi < 11: return -1 # means unknown don't use events
            return 100
        if run < 247644: return 100
        if run == 247644:
            if lumi < 46: return 100
            return 10
        if run < 247685: return 10
        if run < 247702: return 11
        if run == 247702:
            if lumi < 72: return 11
            if lumi < 124: return 5
            return 2
        if run < 247705: return 11
        if run == 247705:
            if lumi < 25: return 11
            return 2
        if run < 247920: return 11
        if run == 247920:
            if lumi < 115: return 11
            return 1
        if run < 247934: return 11
        if run == 247934:
            if lumi < 48: return 11
            return 1

        return 11


    def analyze(self):
        weight = 1
        num = 0
        
        self.hist["hNentries"].Fill( 0, weight )

        run  = self.fChain.run
        lumi = self.fChain.lumi
        bx   = self.fChain.bx

        # if run >= 247685: return 0
        if bx < 200: return 0

        algo100prescale = self.getPrescaleAlog100(run,lumi)
        if algo100prescale < 0: return 0

        NCastorRecoJets = self.fChain.ak5CastorJetsP4.size()
        if NCastorRecoJets == 0:
            return 0

        CastorMedJetTrg  = self.fChain.trgl1L1GTTech[58] or self.fChain.trgl1L1GTAlgo[100]
        CastorHighJetTrg = self.fChain.trgl1L1GTTech[57] or self.fChain.trgl1L1GTAlgo[101]
        ZeroBiasTrg      = self.fChain.trgZeroBias
        MinBiasTrg       = self.fChain.trgMinBias
        RandomTrg        = self.fChain.trgRandom

        self.hist["TrgCount"].Fill("all",1)
        if CastorMedJetTrg:  self.hist["TrgCount"].Fill("MedJet",1)
        if CastorHighJetTrg: self.hist["TrgCount"].Fill("HighJet",1)
        if ZeroBiasTrg:      self.hist["TrgCount"].Fill("ZeroBias",1)
        if MinBiasTrg:       self.hist["TrgCount"].Fill("MinBias",1)
        if RandomTrg:        self.hist["TrgCount"].Fill("RndTrg",1)
        if self.fChain.trgCastorMedJet: self.hist["TrgCount"].Fill("MedJet_HLT",1)
        if self.fChain.trgCastorHighJet: self.hist["TrgCount"].Fill("HighJet_HLT",1)

        CastorRecoJets = []
        for ijet in xrange(0,NCastorRecoJets):
            jet = self.fChain.ak5CastorJetsP4[ijet]
            nTow = self.fChain.ak5CastorJetsnTowers[ijet]
            fem = self.fChain.ak5CastorJetsfem[ijet]

            self.hist["hdNdEak5CastorJets"].Fill(jet.e(), weight) 
            self.hist["hdNdPtak5CastorJets"].Fill(jet.pt(), weight)
            self.hist["hNTowak5CastorJets"].Fill(nTow, weight)

            # if self.jetPreCut(jet): continue
            CastorRecoJets.append([jet,nTow, fem])

        CastorRecoJets.sort(cmp=compareSpecialListJetPt)

        trgpsc_weight = 1
        if CastorMedJetTrg: trgpsc_weight = algo100prescale

        if len(CastorRecoJets) > 0:
            jet = CastorRecoJets[0][0]
            nTow = CastorRecoJets[0][1]
            fem = CastorRecoJets[0][2]

            fem_thr = 0.8

            # if nTow == 2:
            # if MinBiasTrg:
            if CastorMedJetTrg:
                if fem < fem_thr: self.hist["hdNdEak5CastorJetsHOT"].Fill(jet.e(), weight)
                self.hist["hdNdPtak5CastorJetsHOT"].Fill(jet.pt(), weight)
                self.hist["bx"].Fill( bx, weight )
            # if CastorMedJetTrg and MinBiasTrg: 
            if CastorMedJetTrg:
                if fem < fem_thr: self.hist["hdNdEak5CastorJetsHOT_TrgMedJet"].Fill(jet.e(), weight)
                self.hist["hdNdPtak5CastorJetsHOT_TrgMedJet"].Fill(jet.pt(), weight)
                self.hist["hEvsFem_ak5CastorJetsHOT_TrgMedJet"].Fill(jet.e(), fem, weight)
                self.hist["bx_MedJet"].Fill( bx, weight )
            # if CastorHighJetTrg and MinBiasTrg:
            if CastorHighJetTrg and CastorMedJetTrg:
                if fem < fem_thr: self.hist["hdNdEak5CastorJetsHOT_TrgHighJet"].Fill(jet.e(), weight)
                self.hist["hdNdPtak5CastorJetsHOT_TrgHighJet"].Fill(jet.pt(), weight)
                self.hist["hEvsFem_ak5CastorJetsHOT_TrgHighJet"].Fill(jet.e(), fem, weight)
            if ZeroBiasTrg: 
                self.hist["hdNdEak5CastorJetsHOT_TrgZeroBias"].Fill(jet.e(), weight)
                self.hist["hdNdPtak5CastorJetsHOT_TrgZeroBias"].Fill(jet.pt(), weight)
            if MinBiasTrg: 
                self.hist["hdNdEak5CastorJetsHOT_TrgMinBias"].Fill(jet.e(), weight)
                self.hist["hdNdPtak5CastorJetsHOT_TrgMinBias"].Fill(jet.pt(), weight)
                self.hist["bx_MB"].Fill( bx, weight )
            if RandomTrg: 
                self.hist["hdNdEak5CastorJetsHOT_TrgRandom"].Fill(jet.e(), weight)
                self.hist["hdNdPtak5CastorJetsHOT_TrgRandom"].Fill(jet.pt(), weight)

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
                # NTowerHotCastorJet = 4

                phi_inf, phi_sup = self.phiJetSectorRange(HottestCastorJet,NTowerHotCastorJet)
                # self.hist["htest"].Fill(HottestCastorJet.phi(), phi_inf, weight )
                # self.hist["htest"].Fill(HottestCastorJet.phi(), phi_sup, weight )
                # self.hist["htest2"].Fill(NTowerHotCastorJet, abs(phi_sup-phi_inf))

                # for iphi in xrange(-320,320):
                #     phi = iphi/100.
                #     if self.insideJetSector(phi,HottestCastorJet,NTowerHotCastorJet):
                #         self.hist["htest"].Fill(HottestCastorJet.phi(),phi)

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
                    self.hist["ptest"].Fill( HottestCastorJet.e(), MergedGenCastorJet.e()/HottestCastorJet.e(), weight )

                if MergedGenCastorJet and isIsolated:
                    if self.particleInRecoJetSectorNotGenCone(MergedGenCastorJet,HottestCastorJet,NTowerHotCastorJet):
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
    # sampleList.append("MinBias_TuneCUETP8M1_13TeV-pythia8")
    # sampleList.append("data_ZeroBias_Run2015A")
    # sampleList.append("data_L1MinimumBiasHF1_Run2015A")
    # sampleList.append("data_SumL1MinimumBiasHF_Run2015A")
    sampleList.append("data_CastorJets_Run2015A")
    # maxFilesMC = 1
    maxFilesData = 400
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
