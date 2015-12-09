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

idetafix = 7
idphifix = 5

def compareJetPt(x,y):
    if x.pt() < y.pt(): return 1
    if x.pt() > y.pt(): return -1
    if x.pt() == y.pt(): return 0

def compareSpecialListJetPt(x,y):
    return compareJetPt(x[0],y[0])

class GenRecoJetAnalysis(CommonFSQFramework.Core.ExampleProofReader.ExampleProofReader):
    def init(self):

        self.hist = {}
        self.hist["hNentries"] = ROOT.TH1F("hNentries","hNentries",3,-0.5,2.5)

        emin = 0
        emax = 10000
        nebin = 100

        ptmin = 0
        ptmax = 50
        nptbin = 100

        ptmin = 1
        ptmax = 20
        nptbin = 11
        ptbinarr = np.array([1,1.5,2,2.5,3,4,5,6,8,10,13,20],dtype=float)
        # ptbinarr.resize(nptbin+1)
        # for i in xrange(0,nptbin+1):
        #     b = log(ptmin) + i*(log(ptmax)-log(ptmin))/nptbin
        #     ptbinarr[i] = exp(b)

        etamin = -7.3 # -6.6 - 0.7 -> ak7
        etamax = -4.5 # -5.2 + 0.7 -> ak7
        netabin = 28


        self.hist["hAll_RecoJetPt"] = ROOT.TH1F("hAll_RecoJetPt","hAll_RecoJetPt",nptbin,ptbinarr)
        self.hist["hSplit1_RecoJetPt"] = ROOT.TH1F("hSplit1_RecoJetPt","hSplit1_RecoJetPt",nptbin,ptbinarr)
        self.hist["hSplit2_RecoJetPt"] = ROOT.TH1F("hSplit2_RecoJetPt","hSplit2_RecoJetPt",nptbin,ptbinarr)

        ##################################################################################################
        ##################################################################################################            
        if not self.isData:
            self.hist["hAll_GenJetPt"] = ROOT.TH1F("hAll_GenJetPt","hAll_GenJetPt",nptbin,ptbinarr)
            self.hist["hSplit1_GenJetPt"] = ROOT.TH1F("hSplit1_GenJetPt","hSplit1_GenJetPt",nptbin,ptbinarr)
            self.hist["hSplit2_GenJetPt"] = ROOT.TH1F("hSplit2_GenJetPt","hSplit2_GenJetPt",nptbin,ptbinarr)

            self.hist["hAll_PtVsPt_GenRecoJet"] = ROOT.TH2F("hAll_PtVsPt_GenRecoJet","hAll_PtVsPt_GenRecoJet",nptbin,ptbinarr,nptbin,ptbinarr)
            self.hist["hAll_Count"] = ROOT.TH1F("hAll_Count","hAll_Count",10,0,10)
            self.hist["hAll_RecoJetPt_Fake"] = ROOT.TH1F("hAll_RecoJetPt_Fake","hAll_RecoJetPt_Fake",nptbin,ptbinarr)
            self.hist["hAll_RecoJetPt_RatFake"] = ROOT.TH1F("hAll_RecoJetPt_RatFake","hAll_RecoJetPt_RatFake",nptbin,ptbinarr)
            self.hist["hAll_GenJetPt_Misses"] = ROOT.TH1F("hAll_GenJetPt_Misses","hAll_GenJetPt_Misses",nptbin,ptbinarr)
            self.hist["hAll_GenJetPt_RatMis"] = ROOT.TH1F("hAll_GenJetPt_RatMis","hAll_GenJetPt_RatMis",nptbin,ptbinarr)
            self.hist["hAll_RecoJetPt_Merged"] = ROOT.TH1F("hAll_RecoJetPt_Merged","hAll_RecoJetPt_Merged",nptbin,ptbinarr)
            self.hist["hAll_GenJetPt_Merged"] = ROOT.TH1F("hAll_GenJetPt_Merged","hAll_GenJetPt_Merged",nptbin,ptbinarr)


            self.hist["hSplit1_PtVsPt_GenRecoJet"] = ROOT.TH2F("hSplit1_PtVsPt_GenRecoJet","hSplit1_PtVsPt_GenRecoJet",nptbin,ptbinarr,nptbin,ptbinarr)
            self.hist["hSplit1_Count"] = ROOT.TH1F("hSplit1_Count","hSplit1_Count",10,0,10)
            self.hist["hSplit1_RecoJetPt_Fake"] = ROOT.TH1F("hSplit1_RecoJetPt_Fake","hSplit1_RecoJetPt_Fake",nptbin,ptbinarr)
            self.hist["hSplit1_RecoJetPt_RatFake"] = ROOT.TH1F("hSplit1_RecoJetPt_RatFake","hSplit1_RecoJetPt_RatFake",nptbin,ptbinarr)
            self.hist["hSplit1_GenJetPt_Misses"] = ROOT.TH1F("hSplit1_GenJetPt_Misses","hSplit1_GenJetPt_Misses",nptbin,ptbinarr)
            self.hist["hSplit1_GenJetPt_RatMis"] = ROOT.TH1F("hSplit1_GenJetPt_RatMis","hSplit1_GenJetPt_RatMis",nptbin,ptbinarr)
            self.hist["hSplit1_RecoJetPt_Merged"] = ROOT.TH1F("hSplit1_RecoJetPt_Merged","hSplit1_RecoJetPt_Merged",nptbin,ptbinarr)
            self.hist["hSplit1_GenJetPt_Merged"] = ROOT.TH1F("hSplit1_GenJetPt_Merged","hSplit1_GenJetPt_Merged",nptbin,ptbinarr)

            self.hist["hSplit2_PtVsPt_GenRecoJet"] = ROOT.TH2F("hSplit2_PtVsPt_GenRecoJet","hSplit2_PtVsPt_GenRecoJet",nptbin,ptbinarr,nptbin,ptbinarr)
            self.hist["hSplit2_Count"] = ROOT.TH1F("hSplit2_Count","hSplit2_Count",10,0,10)
            self.hist["hSplit2_RecoJetPt_Fake"] = ROOT.TH1F("hSplit2_RecoJetPt_Fake","hSplit2_RecoJetPt_Fake",nptbin,ptbinarr)
            self.hist["hSplit2_RecoJetPt_RatFake"] = ROOT.TH1F("hSplit2_RecoJetPt_RatFake","hSplit2_RecoJetPt_RatFake",nptbin,ptbinarr)
            self.hist["hSplit2_GenJetPt_Misses"] = ROOT.TH1F("hSplit2_GenJetPt_Misses","hSplit2_GenJetPt_Misses",nptbin,ptbinarr)
            self.hist["hSplit2_GenJetPt_RatMis"] = ROOT.TH1F("hSplit2_GenJetPt_RatMis","hSplit2_GenJetPt_RatMis",nptbin,ptbinarr)
            self.hist["hSplit2_RecoJetPt_Merged"] = ROOT.TH1F("hSplit2_RecoJetPt_Merged","hSplit2_RecoJetPt_Merged",nptbin,ptbinarr)
            self.hist["hSplit2_GenJetPt_Merged"] = ROOT.TH1F("hSplit2_GenJetPt_Merged","hSplit2_GenJetPt_Merged",nptbin,ptbinarr)
        ##################################################################################################
        ##################################################################################################




        ##################################################################################################
        # Special: for checking uncertanty in Energy skale
        self.castor_energy_uncertanty = 0.22
        self.hist["hScaleLow_RecoJetPt"] = ROOT.TH1F("hScaleLow_RecoJetPt","hScaleLow_RecoJetPt",nptbin,ptbinarr)
        self.hist["hScaleUp_RecoJetPt"] = ROOT.TH1F("hScaleUp_RecoJetPt","hScaleUp_RecoJetPt",nptbin,ptbinarr)

        self.hist["hSplit1_ScaleLow_RecoJetPt"] = ROOT.TH1F("hSplit1_ScaleLow_RecoJetPt","hSplit1_ScaleLow_RecoJetPt",nptbin,ptbinarr)
        self.hist["hSplit1_ScaleUp_RecoJetPt"] = ROOT.TH1F("hSplit1_ScaleUp_RecoJetPt","hSplit1_ScaleUp_RecoJetPt",nptbin,ptbinarr)
        self.hist["hSplit2_ScaleLow_RecoJetPt"] = ROOT.TH1F("hSplit2_ScaleLow_RecoJetPt","hSplit2_ScaleLow_RecoJetPt",nptbin,ptbinarr)
        self.hist["hSplit2_ScaleUp_RecoJetPt"] = ROOT.TH1F("hSplit2_ScaleUp_RecoJetPt","hSplit2_ScaleUp_RecoJetPt",nptbin,ptbinarr)
        ##################################################################################################

        #     bb = array('d',[])
        #     nb = 3
        #     bmin = 250.
        #     bmax = 2500.
        #     for i in range(nb+1):
        #         b = log(bmin) + i*(log(bmax)-log(bmin))/nb
        #         bb.append(exp(b))


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
        self.energy_corr_factor = 1.399
        # self.energy_corr_factor = 1.0

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
        return (jet.eta() > -5.7 or jet.eta() < -6.1 or jet.pt() < self.jetPrePtCutValue or jet.e() < 250)

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

        evt  = self.fChain.event
        run  = self.fChain.run
        lumi = self.fChain.lumi
        bx   = self.fChain.bx


        # if run >= 247685: return 0
        if self.isData and bx < 200:
            return 0

        # algo100prescale = self.getPrescaleAlog100(run,lumi)
        # if algo100prescale < 0: return 0
        

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

        # use only events with Bptx AND
        if self.isData:
            if not self.fChain.trgl1L1GTTech[0] or not ZeroBiasTrg:
                return 0


        SplitHistName = "hSplit1_"
        if evt%2 == 1:
            self.hist["hNentries"].Fill( 1, weight )
            SplitHistName = "hSplit2_"


        #############################################################
        # Reco Jet LOOP
        #############################################################
        NCastorRecoJets = self.fChain.ak5CastorJetsP4.size()
        CastorRecoJets = []
        for ijet in xrange(0,NCastorRecoJets):
            jet = self.fChain.ak5CastorJetsP4[ijet]
            CastorRecoJets.append(jet)

            #########################################################
            self.hist["hAll_RecoJetPt"].Fill( jet.pt() * self.energy_corr_factor )
            self.hist[SplitHistName+"RecoJetPt"].Fill( jet.pt() * self.energy_corr_factor )
            #########################################################

            #########################################################
            self.hist["hScaleLow_RecoJetPt"].Fill( jet.pt() * self.energy_corr_factor * (1-self.castor_energy_uncertanty) )
            self.hist["hScaleUp_RecoJetPt"].Fill( jet.pt() * self.energy_corr_factor * (1+self.castor_energy_uncertanty) )

            self.hist[SplitHistName+"ScaleLow_RecoJetPt"].Fill( jet.pt() * self.energy_corr_factor * (1-self.castor_energy_uncertanty) )
            self.hist[SplitHistName+"ScaleUp_RecoJetPt"].Fill( jet.pt() * self.energy_corr_factor * (1+self.castor_energy_uncertanty) )
            #########################################################

        #############################################################
        # Reco Jet LOOP
        #############################################################
        CastorRecoJets.sort(cmp=compareJetPt)




        if not self.isData:
            CastorHadronLevelGenJets = []
            for gjet in self.fChain.ak5GenJetsp4:
                if gjet.eta() < -6.6 or gjet.eta() > -5.2: continue
                CastorHadronLevelGenJets.append(gjet)

                self.hist["hAll_GenJetPt"].Fill(gjet.pt())
                self.hist[SplitHistName+"GenJetPt"].Fill(gjet.pt())
            CastorHadronLevelGenJets.sort(cmp=compareJetPt)


            ###################################################################
            # Do Merging
            ###################################################################
            etacut = float(idetafix)/10.
            phicut = float(idphifix)/10.

            MergedGenJet = []
            MergedRecoJet = []
            for jet in CastorRecoJets:
                merged_jet = self.findMergeGenJet(jet,CastorHadronLevelGenJets,MergedGenJet,etacut,phicut)
                if not merged_jet is None:
                    self.hist["hAll_PtVsPt_GenRecoJet"].Fill(jet.pt()*self.energy_corr_factor,merged_jet.pt())
                    self.hist[SplitHistName+"PtVsPt_GenRecoJet"].Fill(jet.pt()*self.energy_corr_factor,merged_jet.pt())
                    MergedGenJet.append(merged_jet)
                    MergedRecoJet.append(jet)

            if len(MergedGenJet) != len(MergedRecoJet):
                raise Exception("Number of merged Gen and Reco Jets is not the same !!!")

            for jet in CastorRecoJets:
                self.hist["hAll_Count"].Fill("All Reco",1)
                self.hist[SplitHistName+"Count"].Fill("All Reco",1)
                if jet in MergedRecoJet:
                    self.hist["hAll_Count"].Fill("Merged Reco",1)
                    self.hist["hAll_RecoJetPt_Merged"].Fill(jet.pt()*self.energy_corr_factor)
                    self.hist[SplitHistName+"Count"].Fill("Merged Reco",1)
                    self.hist[SplitHistName+"RecoJetPt_Merged"].Fill(jet.pt()*self.energy_corr_factor)
                else:
                    self.hist["hAll_Count"].Fill("Fake",1)
                    self.hist["hAll_RecoJetPt_Fake"].Fill(jet.pt()*self.energy_corr_factor)
                    self.hist["hAll_RecoJetPt_RatFake"].Fill(jet.pt()*self.energy_corr_factor)
                    self.hist[SplitHistName+"Count"].Fill("Fake",1)
                    self.hist[SplitHistName+"RecoJetPt_Fake"].Fill(jet.pt()*self.energy_corr_factor)
                    self.hist[SplitHistName+"RecoJetPt_RatFake"].Fill(jet.pt()*self.energy_corr_factor)
                        
            for gjet in CastorHadronLevelGenJets:
                self.hist["hAll_Count"].Fill("All Gen",1)
                if gjet in MergedGenJet:
                    self.hist["hAll_Count"].Fill("Merged Gen",1)
                    self.hist["hAll_GenJetPt_Merged"].Fill(gjet.pt())
                    self.hist[SplitHistName+"Count"].Fill("Merged Gen",1)
                    self.hist[SplitHistName+"GenJetPt_Merged"].Fill(gjet.pt())
                else:
                    self.hist["hAll_Count"].Fill("Misses",1)
                    self.hist["hAll_GenJetPt_Misses"].Fill(gjet.pt())
                    self.hist["hAll_GenJetPt_RatMis"].Fill(gjet.pt())
                    self.hist[SplitHistName+"Count"].Fill("Misses",1)
                    self.hist[SplitHistName+"GenJetPt_Misses"].Fill(gjet.pt())
                    self.hist[SplitHistName+"GenJetPt_RatMis"].Fill(gjet.pt())
            ###################################################################
            # finish if not self.isData
            ###################################################################

        # finish analyze function
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

        if not self.isData:
            histos["hAll_RecoJetPt_RatFake"].Divide(histos["hAll_RecoJetPt"])
            histos["hAll_GenJetPt_RatMis"].Divide(histos["hAll_GenJetPt"])

            histos["hSplit1_RecoJetPt_RatFake"].Divide(histos["hSplit1_RecoJetPt"])
            histos["hSplit1_GenJetPt_RatMis"].Divide(histos["hSplit1_GenJetPt"])

            histos["hSplit2_RecoJetPt_RatFake"].Divide(histos["hSplit2_RecoJetPt"])
            histos["hSplit2_GenJetPt_RatMis"].Divide(histos["hSplit2_GenJetPt"])
        
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
    # sampleList.append("MinBias_TuneZ2star_13TeV-pythia6")

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
    sampleList.append("data_SumZeroBias_Run2015A")
    # sampleList.append("data_MelIntCalib_ZeroBias1_Run2015A")
    # sampleList.append("data_MelIntCalib_ZeroBias2_Run2015A")
    # sampleList.append("data_NoLED0to38IC_ZeroBias3_Run2015A")

    # sampleList.append("data_CastorJets_Run2015A")
    # sampleList.append("ReggeGribovPartonMC_castorJet_13TeV-EPOS")

    # maxFilesMC = 1
    # maxFilesData = 1
    # nWorkers = 1


    # slaveParams = {}
    # slaveParams["maxEta"] = 2.


    # use printTTree.py <sampleName> to see what trees are avaliable inside the skim file
    GenRecoJetAnalysis.runAll(treeName="JetCastor",
           # slaveParameters=slaveParams,
           sampleList=sampleList,
           maxFilesMC = maxFilesMC,
           maxFilesData = maxFilesData,
           nWorkers=nWorkers,
           # maxNevents=900000,
           outFile = "GenRecoJetAnalysis_TEST.root" )
