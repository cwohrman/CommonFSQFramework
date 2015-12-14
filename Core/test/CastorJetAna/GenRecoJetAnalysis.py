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

doReWeight = False

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
        self.hist["hRunNbr"] = ROOT.TH1F("hRunNbr","hRunNbr minus 247000",2000,0,2000)

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



        ###################################################
        for h in self.hist:
            self.hist[h].Sumw2()
            self.GetOutputList().Add(self.hist[h])


        
        ###################################################
        self.energy_corr_factor = 1.399
        # self.energy_corr_factor = 1.0



        ###################################################
        self.MCtoDATA_JetPtBinWeigth = {}
        self.MCtoDATA_JetPtBinWeigth["MinBias_TuneCUETP8M1_13TeV-pythia8"] = [ 1.01, 0.90, 0.83, 0.79, 0.78, 0.80, 0.86, 0.92, 0.94, 1.06, 1.08]
        self.MCtoDATA_JetPtBinWeigth["MinBias_TuneZ2star_13TeV-pythia6"] = [ 0.77, 0.66, 0.60, 0.57, 0.55, 0.55, 0.57, 0.59, 0.62, 0.72, 0.95]
        self.MCtoDATA_JetPtBinWeigth["MinBias_TuneZ2star_13TeV-pythia6_MagnetOff"] = [ 0.77, 0.66, 0.60, 0.56, 0.55, 0.56, 0.58, 0.59, 0.61, 0.74, 0.82]
        self.MCtoDATA_JetPtBinWeigth["MinBias_TuneMonash13_13TeV-pythia8_MagnetOff"] = [ 1.08, 0.99, 0.94, 0.91, 0.92, 0.95, 0.99, 1.07, 1.13, 1.25, 1.26]
        self.MCtoDATA_JetPtBinWeigth["MinBias_TuneMBR_13TeV-pythia8"] = [ 0.76, 0.67, 0.62, 0.61, 0.62, 0.67, 0.72, 0.78, 0.84, 0.98, 1.28]
        self.MCtoDATA_JetPtBinWeigth["MinBias_TuneMBR_13TeV-pythia8_MagnetOff"] = [ 0.76, 0.66, 0.62, 0.62, 0.62, 0.67, 0.74, 0.78, 0.86, 1.02, 1.15]
        self.MCtoDATA_JetPtBinWeigth["ReggeGribovPartonMC_13TeV-QGSJetII"] = [ 1.22, 1.20, 1.08, 0.94, 0.75, 0.58, 0.51, 0.46, 0.44, 0.43, 0.41]
        self.MCtoDATA_JetPtBinWeigth["ReggeGribovPartonMC_13TeV-QGSJetII_MagnetOff"] = [ 1.22, 1.19, 1.08, 0.93, 0.74, 0.59, 0.51, 0.47, 0.44, 0.43, 0.40]
        self.MCtoDATA_JetPtBinWeigth["ReggeGribovPartonMC_13TeV-EPOS"] = [ 1.11, 1.09, 1.05, 1.00, 0.92, 0.79, 0.69, 0.52, 0.36, 0.29, 0.28]
        self.MCtoDATA_JetPtBinWeigth["ReggeGribovPartonMC_13TeV-EPOS_MagnetOff"] = [ 1.11, 1.09, 1.05, 1.01, 0.91, 0.79, 0.68, 0.54, 0.37, 0.30, 0.23]

        ####################################################
        # collect with Njets mean weighted bins
        self.MCtoDATA_SecndWeigth = {}
        self.MCtoDATA_SecndWeigth["MinBias_TuneCUETP8M1_13TeV-pythia8"] = [ 1.03, 0.91, 0.88, 0.86, 0.88, 0.92, 0.99, 1.04, 1.01, 1.12, 1.08]
        self.MCtoDATA_SecndWeigth["MinBias_TuneZ2star_13TeV-pythia6"] = [ 0.85, 0.79, 0.78, 0.77, 0.78, 0.81, 0.85, 0.86, 0.88, 1.00, 1.21]
        self.MCtoDATA_SecndWeigth["MinBias_TuneZ2star_13TeV-pythia6_MagnetOff"] = [ 0.85, 0.79, 0.77, 0.76, 0.78, 0.82, 0.85, 0.86, 0.86, 1.04, 1.06]
        self.MCtoDATA_SecndWeigth["MinBias_TuneMonash13_13TeV-pythia8_MagnetOff"] = [ 1.07, 0.95, 0.93, 0.93, 0.95, 1.00, 1.03, 1.09, 1.11, 1.20, 1.14]
        self.MCtoDATA_SecndWeigth["MinBias_TuneMBR_13TeV-pythia8"] = [ 0.85, 0.80, 0.80, 0.81, 0.86, 0.92, 0.97, 1.00, 1.02, 1.13, 1.35]
        self.MCtoDATA_SecndWeigth["MinBias_TuneMBR_13TeV-pythia8_MagnetOff"] = [ 0.85, 0.80, 0.81, 0.82, 0.85, 0.91, 1.00, 1.00, 1.03, 1.17, 1.17]
        self.MCtoDATA_SecndWeigth["ReggeGribovPartonMC_13TeV-QGSJetII"] = [ 1.17, 1.06, 0.97, 0.86, 0.73, 0.66, 0.65, 0.72, 0.80, 0.82, 0.84]
        self.MCtoDATA_SecndWeigth["ReggeGribovPartonMC_13TeV-QGSJetII_MagnetOff"] = [ 1.17, 1.06, 0.97, 0.86, 0.73, 0.68, 0.66, 0.72, 0.78, 0.82, 0.86]
        self.MCtoDATA_SecndWeigth["ReggeGribovPartonMC_13TeV-EPOS"] = [ 1.08, 1.03, 1.00, 0.95, 0.90, 0.81, 0.73, 0.60, 0.50, 0.50, 0.66]
        self.MCtoDATA_SecndWeigth["ReggeGribovPartonMC_13TeV-EPOS_MagnetOff"] = [ 1.08, 1.03, 1.00, 0.97, 0.89, 0.81, 0.72, 0.62, 0.51, 0.48, 0.54]

        ####################################################
        # collect with Njets mean weighted bins
        self.MCtoDATA_ThirdWeigth = {}
        self.MCtoDATA_ThirdWeigth["MinBias_TuneCUETP8M1_13TeV-pythia8"] = [ 1.04, 0.90, 0.92, 0.92, 0.95, 1.00, 1.07, 1.08, 1.00, 1.11, 1.05]
        self.MCtoDATA_ThirdWeigth["MinBias_TuneZ2star_13TeV-pythia6"] = [ 0.89, 0.87, 0.89, 0.89, 0.91, 0.95, 0.98, 0.97, 0.97, 1.09, 1.23]
        self.MCtoDATA_ThirdWeigth["MinBias_TuneMonash13_13TeV-pythia8_MagnetOff"] = [ 1.06, 0.92, 0.95, 0.96, 0.99, 1.03, 1.05, 1.09, 1.07, 1.14, 1.05]
        self.MCtoDATA_ThirdWeigth["MinBias_TuneMBR_13TeV-pythia8"] = [ 0.90, 0.89, 0.91, 0.93, 0.98, 1.02, 1.05, 1.05, 1.03, 1.13, 1.28]
        self.MCtoDATA_ThirdWeigth["ReggeGribovPartonMC_13TeV-QGSJetII"] = [ 1.14, 0.97, 0.92, 0.84, 0.76, 0.81, 0.86, 1.03, 1.11, 1.07, 1.03]
        self.MCtoDATA_ThirdWeigth["ReggeGribovPartonMC_13TeV-EPOS"] = [ 1.07, 0.99, 0.98, 0.94, 0.91, 0.84, 0.78, 0.69, 0.69, 0.82, 1.20]
        self.MCtoDATA_ThirdWeigth["MinBias_TuneZ2star_13TeV-pythia6_MagnetOff"] = [ 0.89, 0.87, 0.88, 0.88, 0.92, 0.96, 0.98, 0.96, 0.94, 1.13, 1.08]
        self.MCtoDATA_ThirdWeigth["MinBias_TuneMBR_13TeV-pythia8_MagnetOff"] = [ 0.90, 0.89, 0.92, 0.94, 0.96, 1.01, 1.08, 1.04, 1.03, 1.16, 1.10]
        self.MCtoDATA_ThirdWeigth["ReggeGribovPartonMC_13TeV-QGSJetII_MagnetOff"] = [ 1.14, 0.97, 0.92, 0.84, 0.76, 0.83, 0.87, 1.01, 1.07, 1.08, 1.07]
        self.MCtoDATA_ThirdWeigth["ReggeGribovPartonMC_13TeV-EPOS_MagnetOff"] = [ 1.07, 0.99, 0.98, 0.96, 0.90, 0.85, 0.78, 0.72, 0.69, 0.76, 1.01]

        
        ####################################################
        # collect with pt weighted weights
        # self.MCtoDATA_SecndWeigth = {}
        # self.MCtoDATA_SecndWeigth["MinBias_TuneCUETP8M1_13TeV-pythia8"] = [ 1.03, 0.91, 0.88, 0.87, 0.89, 0.94, 1.02, 1.07, 1.02, 1.12, 1.06]
        # self.MCtoDATA_SecndWeigth["MinBias_TuneZ2star_13TeV-pythia6"] = [ 0.85, 0.80, 0.78, 0.77, 0.79, 0.83, 0.87, 0.90, 0.91, 1.03, 1.21]
        # self.MCtoDATA_SecndWeigth["MinBias_TuneZ2star_13TeV-pythia6_MagnetOff"] = [ 0.85, 0.80, 0.78, 0.77, 0.80, 0.84, 0.88, 0.89, 0.89, 1.07, 1.06]
        # self.MCtoDATA_SecndWeigth["MinBias_TuneMonash13_13TeV-pythia8_MagnetOff"] = [ 1.07, 0.96, 0.94, 0.93, 0.96, 1.01, 1.05, 1.10, 1.10, 1.18, 1.09]
        # self.MCtoDATA_SecndWeigth["MinBias_TuneMBR_13TeV-pythia8"] = [ 0.85, 0.81, 0.80, 0.81, 0.87, 0.93, 0.99, 1.01, 1.00, 1.10, 1.27]
        # self.MCtoDATA_SecndWeigth["MinBias_TuneMBR_13TeV-pythia8_MagnetOff"] = [ 0.86, 0.81, 0.81, 0.83, 0.86, 0.92, 1.01, 1.00, 1.01, 1.14, 1.09]
        # self.MCtoDATA_SecndWeigth["ReggeGribovPartonMC_13TeV-QGSJetII"] = [ 1.17, 1.07, 0.97, 0.87, 0.74, 0.69, 0.70, 0.79, 0.90, 0.93, 0.95]
        # self.MCtoDATA_SecndWeigth["ReggeGribovPartonMC_13TeV-QGSJetII_MagnetOff"] = [ 1.17, 1.07, 0.97, 0.86, 0.74, 0.71, 0.71, 0.79, 0.88, 0.92, 0.94]
        # self.MCtoDATA_SecndWeigth["ReggeGribovPartonMC_13TeV-EPOS"] = [ 1.08, 1.03, 1.01, 0.96, 0.91, 0.82, 0.76, 0.64, 0.58, 0.60, 0.83]
        # self.MCtoDATA_SecndWeigth["ReggeGribovPartonMC_13TeV-EPOS_MagnetOff"] = [ 1.09, 1.03, 1.00, 0.98, 0.90, 0.83, 0.75, 0.66, 0.58, 0.59, 0.67]

        ####################################################
        # collect with pt weighted weights
        # self.MCtoDATA_ThirdWeigth = {}
        # self.MCtoDATA_ThirdWeigth["MinBias_TuneCUETP8M1_13TeV-pythia8"] = [ 1.04, 0.91, 0.93, 0.93, 0.97, 1.03, 1.10, 1.09, 0.98, 1.08, 0.99]
        # self.MCtoDATA_ThirdWeigth["MinBias_TuneZ2star_13TeV-pythia6"] = [ 0.90, 0.89, 0.89, 0.89, 0.93, 0.97, 1.00, 0.99, 0.96, 1.07, 1.16]
        # self.MCtoDATA_ThirdWeigth["MinBias_TuneZ2star_13TeV-pythia6_MagnetOff"] = [ 0.90, 0.88, 0.89, 0.89, 0.93, 0.98, 1.00, 0.97, 0.94, 1.12, 1.02]
        # self.MCtoDATA_ThirdWeigth["MinBias_TuneMonash13_13TeV-pythia8_MagnetOff"] = [ 1.07, 0.93, 0.95, 0.96, 1.00, 1.05, 1.07, 1.09, 1.04, 1.10, 0.98]
        # self.MCtoDATA_ThirdWeigth["MinBias_TuneMBR_13TeV-pythia8"] = [ 0.90, 0.90, 0.91, 0.93, 0.99, 1.02, 1.05, 1.02, 0.97, 1.05, 1.15]
        # self.MCtoDATA_ThirdWeigth["MinBias_TuneMBR_13TeV-pythia8_MagnetOff"] = [ 0.90, 0.89, 0.91, 0.94, 0.97, 1.01, 1.09, 1.02, 0.98, 1.09, 0.98]
        # self.MCtoDATA_ThirdWeigth["ReggeGribovPartonMC_13TeV-QGSJetII"] = [ 1.15, 0.99, 0.93, 0.85, 0.79, 0.87, 0.94, 1.12, 1.18, 1.13, 1.05]
        # self.MCtoDATA_ThirdWeigth["ReggeGribovPartonMC_13TeV-QGSJetII_MagnetOff"] = [ 1.15, 0.99, 0.93, 0.85, 0.79, 0.89, 0.94, 1.10, 1.15, 1.13, 1.06]
        # self.MCtoDATA_ThirdWeigth["ReggeGribovPartonMC_13TeV-EPOS"] = [ 1.07, 1.00, 0.99, 0.95, 0.92, 0.87, 0.83, 0.77, 0.83, 0.96, 1.38]
        # self.MCtoDATA_ThirdWeigth["ReggeGribovPartonMC_13TeV-EPOS_MagnetOff"] = [ 1.07, 1.00, 0.99, 0.97, 0.91, 0.88, 0.83, 0.79, 0.82, 0.93, 1.14]

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


    # returns weight for event
    # to shift MC Reco to Data Reco
    def getMCJetPtEventWeight(self,jetptweight=False):
        sampleName = self.datasetName

        tmp_weight = 0.0
        sum_weight = 0.0
        N_weight = 0.0
        for jet in self.fChain.ak5CastorJetsP4:
            if jet.pt() < 1 or jet.pt() > 20: continue

            ibin = self.hist["hAll_RecoJetPt"].FindBin(jet.pt())
            if ibin < 1 or ibin > 11: continue

            tmp_weight = 1.
            tmp_weight *= self.MCtoDATA_JetPtBinWeigth[sampleName][ibin-1]
            tmp_weight *= self.MCtoDATA_SecndWeigth[sampleName][ibin-1]
            tmp_weight *= self.MCtoDATA_ThirdWeigth[sampleName][ibin-1]

            if jetptweight:
                sum_weight += jet.pt()/tmp_weight
                N_weight += jet.pt()
            else:
                sum_weight += 1./tmp_weight
                N_weight += 1.

        if N_weight == 0: return 1

        return sum_weight/N_weight


    def analyze(self):
        weight = 1
        num = 0
        

        ###################################################
        # get weight for MC event by JetPt bin
        if not self.isData and doReWeight:
            weight = self.getMCJetPtEventWeight()

        evt  = self.fChain.event
        run  = self.fChain.run
        lumi = self.fChain.lumi
        bx   = self.fChain.bx

        self.hist["hRunNbr"].Fill(run-247000)

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

        self.hist["hNentries"].Fill( 0, weight )

        # use only events with Bptx AND
        if self.isData:
            if not self.fChain.trgl1L1GTTech[0] or not ZeroBiasTrg:
                return 0


        # if run >= 247685: return 0
        if self.isData and bx < 200:
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
            self.hist["hAll_RecoJetPt"].Fill( jet.pt() * self.energy_corr_factor , weight )
            self.hist[SplitHistName+"RecoJetPt"].Fill( jet.pt() * self.energy_corr_factor , weight )
            #########################################################

            #########################################################
            self.hist["hScaleLow_RecoJetPt"].Fill( jet.pt() * self.energy_corr_factor * (1-self.castor_energy_uncertanty) , weight )
            self.hist["hScaleUp_RecoJetPt"].Fill( jet.pt() * self.energy_corr_factor * (1+self.castor_energy_uncertanty) , weight )

            self.hist[SplitHistName+"ScaleLow_RecoJetPt"].Fill( jet.pt() * self.energy_corr_factor * (1-self.castor_energy_uncertanty) , weight )
            self.hist[SplitHistName+"ScaleUp_RecoJetPt"].Fill( jet.pt() * self.energy_corr_factor * (1+self.castor_energy_uncertanty) , weight )
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

                self.hist["hAll_GenJetPt"].Fill( gjet.pt() , weight )
                self.hist[SplitHistName+"GenJetPt"].Fill( gjet.pt() , weight )
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
                    self.hist["hAll_PtVsPt_GenRecoJet"].Fill(jet.pt()*self.energy_corr_factor,merged_jet.pt(), weight )
                    self.hist[SplitHistName+"PtVsPt_GenRecoJet"].Fill(jet.pt()*self.energy_corr_factor,merged_jet.pt(), weight )
                    MergedGenJet.append(merged_jet)
                    MergedRecoJet.append(jet)

            if len(MergedGenJet) != len(MergedRecoJet):
                raise Exception("Number of merged Gen and Reco Jets is not the same !!!")

            for jet in CastorRecoJets:
                self.hist["hAll_Count"].Fill("All Reco", weight )
                self.hist[SplitHistName+"Count"].Fill("All Reco", weight )
                if jet in MergedRecoJet:
                    self.hist["hAll_Count"].Fill("Merged Reco", weight )
                    self.hist["hAll_RecoJetPt_Merged"].Fill(jet.pt()*self.energy_corr_factor, weight )
                    self.hist[SplitHistName+"Count"].Fill("Merged Reco", weight )
                    self.hist[SplitHistName+"RecoJetPt_Merged"].Fill(jet.pt()*self.energy_corr_factor, weight )
                else:
                    self.hist["hAll_Count"].Fill("Fake", weight )
                    self.hist["hAll_RecoJetPt_Fake"].Fill(jet.pt()*self.energy_corr_factor, weight )
                    self.hist["hAll_RecoJetPt_RatFake"].Fill(jet.pt()*self.energy_corr_factor, weight )
                    self.hist[SplitHistName+"Count"].Fill("Fake", weight )
                    self.hist[SplitHistName+"RecoJetPt_Fake"].Fill(jet.pt()*self.energy_corr_factor, weight )
                    self.hist[SplitHistName+"RecoJetPt_RatFake"].Fill(jet.pt()*self.energy_corr_factor, weight )
                        
            for gjet in CastorHadronLevelGenJets:
                self.hist["hAll_Count"].Fill("All Gen", weight )
                if gjet in MergedGenJet:
                    self.hist["hAll_Count"].Fill("Merged Gen", weight )
                    self.hist["hAll_GenJetPt_Merged"].Fill(gjet.pt(), weight )
                    self.hist[SplitHistName+"Count"].Fill("Merged Gen", weight )
                    self.hist[SplitHistName+"GenJetPt_Merged"].Fill(gjet.pt(), weight )
                else:
                    self.hist["hAll_Count"].Fill("Misses", weight )
                    self.hist["hAll_GenJetPt_Misses"].Fill(gjet.pt(), weight )
                    self.hist["hAll_GenJetPt_RatMis"].Fill(gjet.pt(), weight )
                    self.hist[SplitHistName+"Count"].Fill("Misses", weight )
                    self.hist[SplitHistName+"GenJetPt_Misses"].Fill(gjet.pt(), weight )
                    self.hist[SplitHistName+"GenJetPt_RatMis"].Fill(gjet.pt(), weight )
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
    sampleList.append("MinBias_TuneCUETP8M1_13TeV-pythia8")
    sampleList.append("MinBias_TuneMonash13_13TeV-pythia8_MagnetOff")

    sampleList.append("MinBias_TuneZ2star_13TeV-pythia6")
    sampleList.append("MinBias_TuneZ2star_13TeV-pythia6_MagnetOff")

    sampleList.append("MinBias_TuneMBR_13TeV-pythia8_MagnetOff")
    sampleList.append("MinBias_TuneMBR_13TeV-pythia8")

    sampleList.append("ReggeGribovPartonMC_13TeV-QGSJetII")
    sampleList.append("ReggeGribovPartonMC_13TeV-EPOS")

    sampleList.append("ReggeGribovPartonMC_13TeV-EPOS_MagnetOff")
    sampleList.append("ReggeGribovPartonMC_13TeV-QGSJetII_MagnetOff")

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
    # maxFilesData = 1
    # nWorkers = 1


    # slaveParams = {}
    # slaveParams["maxEta"] = 2.


    outputFileName = "GenRecoJetAnalysis_MC"
    if doReWeight: outputFileName += "_ReWeightMC"
    outputFileName += ".root"

    # use printTTree.py <sampleName> to see what trees are avaliable inside the skim file
    GenRecoJetAnalysis.runAll(treeName="JetCastor",
           # slaveParameters=slaveParams,
           sampleList=sampleList,
           maxFilesMC = maxFilesMC,
           maxFilesData = maxFilesData,
           nWorkers=nWorkers,
           maxNevents=1000000,
           outFile = outputFileName )
