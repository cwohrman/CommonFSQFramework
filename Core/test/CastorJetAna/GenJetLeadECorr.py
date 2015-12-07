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

idetamin = 2
idetamax = 7+1
idphimin = 1
idphimax = 5+1

def compareJetPt(x,y):
    if x.pt() < y.pt(): return 1
    if x.pt() > y.pt(): return -1
    if x.pt() == y.pt(): return 0

def compareSpecialListJetPt(x,y):
    return compareJetPt(x[0],y[0])

class GenJetLeadECorr(CommonFSQFramework.Core.ExampleProofReader.ExampleProofReader):
    def init(self):

        self.jetPrePtCutValue = 1.

        self.hist = {}
        self.hist["hNentries"] = ROOT.TH1F("hNentries","hNentries",3,-0.5,2.5)

        emin = 0
        emax = 10000
        nebin = 100

        ptmin = 0
        ptmax = 50
        nptbin = 100

        etamin = -7.3 # -6.6 - 0.7 -> ak7
        etamax = -4.5 # -5.2 + 0.7 -> ak7
        netabin = 28

        self.hist["hdNdPtak5CastorJets"] =  ROOT.TH1F("hdNdPtak5CastorJets","hdNdPtak5CastorJets",nptbin,ptmin,ptmax)
        self.hist["hNTowak5CastorJets"]  =  ROOT.TH1F("hNTowak5CastorJets","hNTowak5CastorJets",7,-0.5,6.5)

        self.hist["hDeltaPhiGenJetHotCasJet"] = ROOT.TH1F("hDeltaPhiGenJetHotCasJet","hDeltaPhiGenJetHotCasJet",50,-pi,pi)
        self.hist["hEGenJetVsECasJet"]        = ROOT.TH2F("hEGenJetVsECasJet","hEGenJetVsECasJet",nebin,emin,emax,nebin,emin,emax)
        self.hist["hPtGenJetVsPtCasJet"]      = ROOT.TH2F("hPtGenJetVsPtCasJet","hPtGenJetVsPtCasJet",nptbin,ptmin,ptmax,nptbin,ptmin,ptmax)

        self.hist["hCountMergedJet"] = ROOT.TH1F("hCountMergedJet","hCountMergedJet",10,0,10)

        self.hist["hPtGenJetVsPtCasJet_EtaPhiCut"]    = ROOT.TH2F("hPtGenJetVsPtCasJet_EtaPhiCut","hPtGenJetVsPtCasJet_EtaPhiCut",nptbin,ptmin,ptmax,nptbin,ptmin,ptmax)
        self.hist["hPtGenJetVsPtCasJet_NoSecJet"]     = ROOT.TH2F("hPtGenJetVsPtCasJet_NoSecJet","hPtGenJetVsPtCasJet_NoSecJet",nptbin,ptmin,ptmax,nptbin,ptmin,ptmax)
        self.hist["hPtGenJetVsPtCasJet_NoPartInCone"] = ROOT.TH2F("hPtGenJetVsPtCasJet_NoPartInCone","hPtGenJetVsPtCasJet_NoPartInCone",nptbin,ptmin,ptmax,nptbin,ptmin,ptmax)

        self.hist["hdNdEMergedCasJet"]     = ROOT.TH1F("hdNdEMergedCasJet","hdNdEMergedCasJet",nebin,emin,emax)
        self.hist["hdNdPtMergedCasJet"]    = ROOT.TH1F("hdNdPtMergedCasJet","hdNdPtMergedCasJet",nptbin,ptmin,ptmax)

        bb = array('d',[])
        nb = 3
        bmin = 250.
        bmax = 2500.
        for i in range(nb+1):
            b = log(bmin) + i*(log(bmax)-log(bmin))/nb
            bb.append(exp(b))

        self.hist["pECasJetGenReco"]          = ROOT.TProfile("pECasJetGenReco","pECasJetGenReco",len(bb)-1,bb)
        self.hist["ptest"]                    = ROOT.TProfile("ptest","ptest",len(bb)-1,bb)

        # # ======================
        # phimin = -pi
        # phimax = pi
        # nphibin = 16
        # # ======================



        # # ======================
        # zmin = -16000
        # zmax = -14000
        # nzbin = 80
        # # ======================


        for h in self.hist:
            self.hist[h].Sumw2()
            self.GetOutputList().Add(self.hist[h])

        # self.SectorBorders = [ 0.,    pi/8.,    pi/4.,  3*pi/8.,  pi/2.,  5*pi/8., 3*pi/4., 7*pi/8., 
        #                        pi, -7*pi/8., -3*pi/4., -5*pi/8., -pi/2., -3*pi/8.,  -pi/4.,  -pi/8. ]
                                
        self.TmpLorVec = ROOT.ROOT.Math.LorentzVector('ROOT::Math::PxPyPzE4D<double>')()
        # self.energy_corr_factor = 1.46
        self.energy_corr_factor = 1.0

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
        return (jet.eta() > -5.7 or jet.eta() < -6.1 or jet.pt() < self.jetPrePtCutValue)

    def jetPreCut_corrE(self, jet):
        return (jet.eta() > -5.7 or jet.eta() < -6.1 or jet.pt() < self.jetPrePtCutValue*self.energy_corr_factor or jet.e() < 250*self.energy_corr_factor)

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


    # find to given recojet a mergable genjet out of list_genjet
    # don't uses genjets which are aleady in merged_genjet
    # 
    # etamin = -5.9 - etacut; etamax = -5.9 + etacut
    # standard is etacut=0.7 => castor witdth in eta
    # phicut between jet.phi() and genjet.phi()
    # when more then one genjet fullfill eta and phi criteria then
    # pt_max_genjet * ptcut > pt_second_max_genjet
    #
    # return the merged genjet
    #        when not merged just None
    def findMergeGenJet(self,recojet,list_genjet,merged_genjet,etacut=0.7,phicut=0.3,ptcut=0.1):
        MergeProposalGenJet = []
        for gjet in list_genjet:
            if gjet.eta() < -5.9-etacut or gjet.eta() > -5.9+etacut: continue
            dphi = self.getDphi(gjet,recojet)
            if abs(dphi) > phicut: continue
            if gjet in merged_genjet: continue
            MergeProposalGenJet.append(gjet)

            if len(MergeProposalGenJet) > 1:
                # sort greater pt first
                MergeProposalGenJet.sort(cmp=compareJetPt)
                if MergeProposalGenJet[0].pt() * ptcut < MergeProposalGenJet[1].pt():
                    return None
                else:
                    return MergeProposalGenJet[0]
            elif len(MergeProposalGenJet) == 1:
                return MergeProposalGenJet[0]
            elif len(MergeProposalGenJet) == 0:
                return None




    def analyze(self):
        weight = 1
        num = 0
        
        self.hist["hNentries"].Fill( 0, weight )

        run  = self.fChain.run
        lumi = self.fChain.lumi
        bx   = self.fChain.bx

        # if run >= 247685: return 0
        if self.isData and bx < 200:
            return 0

        # algo100prescale = self.getPrescaleAlog100(run,lumi)
        # if algo100prescale < 0: return 0

        NCastorRecoJets = self.fChain.ak5CastorJetsP4.size()
       
        CastorMedJetTrg  = self.fChain.trgl1L1GTTech[58] or self.fChain.trgl1L1GTAlgo[100]
        CastorHighJetTrg = self.fChain.trgl1L1GTTech[57] or self.fChain.trgl1L1GTAlgo[101]
        ZeroBiasTrg      = self.fChain.trgZeroBias
        MinBiasTrg       = self.fChain.trgMinBias
        RandomTrg        = self.fChain.trgRandom
        CastorDiJetTrg   = self.fChain.trgCastorDiJet

        if not self.isData:
            CastorMedJetTrg  = self.fChain.trgl1L1GTTech[62]
            CastorHighJetTrg = self.fChain.trgl1L1GTTech[61]
            MinBiasTrg       = True


        CastorRecoJets = []
        for ijet in xrange(0,NCastorRecoJets):
            jet = self.fChain.ak5CastorJetsP4[ijet]
            nTow = self.fChain.ak5CastorJetsnTowers[ijet]
            fem = self.fChain.ak5CastorJetsfem[ijet]
            zDpt = self.fChain.ak5CastorJetsdepth[ijet]

            self.hist["hdNdPtak5CastorJets"].Fill(jet.pt(), weight)
            self.hist["hNTowak5CastorJets"].Fill(nTow, weight)

            if not self.jetPreCut(jet): CastorRecoJets.append([jet, nTow, fem, zDpt])

        CastorRecoJets.sort(cmp=compareSpecialListJetPt)


        MergedGenCastorJet = None
        isIsolated = True
        if len(CastorRecoJets) > 0:
            mindphi = 0.2
            HottestCastorJet = CastorRecoJets[0][0]
            NTowerHotCastorJet = CastorRecoJets[0][1]

            phi_inf, phi_sup = self.phiJetSectorRange(HottestCastorJet,NTowerHotCastorJet)
            # self.hist["htest"].Fill(HottestCastorJet.phi(), phi_inf, weight )
            # self.hist["htest"].Fill(HottestCastorJet.phi(), phi_sup, weight )
            # self.hist["htest2"].Fill(NTowerHotCastorJet, abs(phi_sup-phi_inf))

            # for iphi in xrange(-320,320):
            #     phi = iphi/100.
            #     if self.insideJetSector(phi,HottestCastorJet,NTowerHotCastorJet):
            #         self.hist["htest"].Fill(HottestCastorJet.phi(),phi)

            dphi = 10.0
            for jet in self.fChain.ak5GenJetsp4:
                if self.jetPreCut(jet): continue

                dphi = self.getDphi(HottestCastorJet,jet)

                self.hist["hDeltaPhiGenJetHotCasJet"].Fill( dphi, weight )

                if dphi < mindphi:
                    mindphi = dphi
                    MergedGenCastorJet = jet

            if dphi != 10.0:
                self.hist["hCountMergedJet"].Fill("Eta Cut",1)

            if MergedGenCastorJet:
                self.hist["hCountMergedJet"].Fill("Dphi cut",1)
                self.hist["hPtGenJetVsPtCasJet_EtaPhiCut"].Fill( HottestCastorJet.pt(), MergedGenCastorJet.pt(), weight )
                if self.secondGenJetOverlay(MergedGenCastorJet,HottestCastorJet):
                    isIsolated = False

            if MergedGenCastorJet and isIsolated:
                self.hist["hCountMergedJet"].Fill("no 2.Jet",1)
                self.hist["hPtGenJetVsPtCasJet_NoSecJet"].Fill( HottestCastorJet.pt(), MergedGenCastorJet.pt(), weight )
                if self.particleInRecoNotGenCone(MergedGenCastorJet,HottestCastorJet):
                    isIsolated = False

            if MergedGenCastorJet and isIsolated:
                self.hist["hCountMergedJet"].Fill("no P. in Reco Cone",1)
                self.hist["hPtGenJetVsPtCasJet_NoPartInCone"].Fill( HottestCastorJet.pt(), MergedGenCastorJet.pt(), weight )
                self.hist["ptest"].Fill( HottestCastorJet.e(), MergedGenCastorJet.e()/HottestCastorJet.e(), weight )
                if self.particleInRecoJetSectorNotGenCone(MergedGenCastorJet,HottestCastorJet,NTowerHotCastorJet):
                    isIsolated = False

            if MergedGenCastorJet and isIsolated:
                self.hist["hCountMergedJet"].Fill("no P. in Reco Area",1)
                self.hist["hEGenJetVsECasJet"].Fill( HottestCastorJet.e(), MergedGenCastorJet.e(), weight )
                self.hist["hPtGenJetVsPtCasJet"].Fill( HottestCastorJet.pt(), MergedGenCastorJet.pt(), weight )
                self.hist["pECasJetGenReco"].Fill( HottestCastorJet.e(), MergedGenCastorJet.e()/HottestCastorJet.e(), weight )
                self.hist["hdNdEMergedCasJet"].Fill( HottestCastorJet.e() )
                self.hist["hdNdPtMergedCasJet"].Fill( HottestCastorJet.pt() )

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
            # print " TH1 histogram in output: ", o.GetName()
        
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

    # sampleList.append("MinBias_TuneMBR_13TeV-pythia8_MagnetOff")
    # sampleList.append("MinBias_TuneMBR_13TeV-pythia8")

    # sampleList.append("ReggeGribovPartonMC_13TeV-QGSJetII")
    sampleList.append("ReggeGribovPartonMC_13TeV-EPOS")

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

    # sampleList.append("data_CastorJets_Run2015A")
    # sampleList.append("ReggeGribovPartonMC_castorJet_13TeV-EPOS")

    # maxFilesMC = 1
    maxFilesData = 400
    # nWorkers = 1


    # slaveParams = {}
    # slaveParams["maxEta"] = 2.


    # use printTTree.py <sampleName> to see what trees are avaliable inside the skim file
    GenJetLeadECorr.runAll(treeName="JetCastor",
           # slaveParameters=slaveParams,
           sampleList=sampleList,
           maxFilesMC = maxFilesMC,
           maxFilesData = maxFilesData,
           nWorkers=nWorkers,
           # maxNevents=1000000,
           outFile = "LeadingJetEnergyCorrection.root" )
