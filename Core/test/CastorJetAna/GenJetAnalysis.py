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

class GenJetAnalysis(CommonFSQFramework.Core.ExampleProofReader.ExampleProofReader):
    def init(self):

        self.jetPrePtCutValue = 1.
        if "castorJet_13TeV-EPOS" in self.datasetName:
            self.jetPrePtCutValue = 1.

        self.hist = {}
        self.hist["hNentries"] = ROOT.TH1F("hNentries","hNentries",3,-0.5,2.5)

        self.hist["bx"] = ROOT.TH1F("bx",";bx",4000,0,4000)
        self.hist["bx_MB"] = ROOT.TH1F("bx_MB","bx_MB",4000,0,4000)
        self.hist["bx_MedJet"] = ROOT.TH1F("bx_MedJet","bx_MedJet",4000,0,4000)

        self.hist["TrgCount"] = ROOT.TH1F("TrgCount","TrgCount",10,0,10)

        emin = 0
        emax = 10000
        nebin = 100

        ptmin = 0
        ptmax = 50
        nptbin = 100

        etamin = -7.3 # -6.6 - 0.7 -> ak7
        etamax = -4.5 # -5.2 + 0.7 -> ak7
        netabin = 28

        if not self.isData:
            self.hist["hNak5GenJets"]          = ROOT.TH1F("hNak5GenJets","hNak5GenJets",100,-0.5, 99.5)
            self.hist["hdNdEak5GenJets"]       = ROOT.TH1F("hdNdEak5GenJets","hdNdEak5GenJets",nebin,emin,emax)
            self.hist["hdNdPtak5GenJets"]      = ROOT.TH1F("hdNdPtak5GenJets","hdNdPtak5GenJets",nptbin,ptmin,ptmax)
            self.hist["hdNdEtaak5GenJets"]     = ROOT.TH1F("hdNdEtaak5GenJets","hdNdEtaak5GenJets",60,-6,6)
            self.hist["hdNdEak5GenVsRecoJets"] = ROOT.TH2F("hdNdEak5GenVsRecoJets","hdNdEak5GenVsRecoJets",nebin,emin,emax,nebin,emin,emax)
            self.hist["hdNdPtak5GenVsRecoJets"] = ROOT.TH2F("hdNdPtak5GenVsRecoJets","hdNdPtak5GenVsRecoJets",nptbin,ptmin,ptmax,nptbin,ptmin,ptmax)

            self.hist["hDeltaPhiGenJetHotCasJet"] = ROOT.TH1F("hDeltaPhiGenJetHotCasJet","hDeltaPhiGenJetHotCasJet",50,-pi,pi)
            self.hist["hEGenJetVsECasJet"]        = ROOT.TH2F("hEGenJetVsECasJet","hEGenJetVsECasJet",nebin,emin,emax,nebin,emin,emax)
            self.hist["hPtGenJetVsPtCasJet"]      = ROOT.TH2F("hPtGenJetVsPtCasJet","hPtGenJetVsPtCasJet",nptbin,ptmin,ptmax,nptbin,ptmin,ptmax)
            self.hist["hEGenJetVsCorECasJet"]        = ROOT.TH2F("hEGenJetVsCorECasJet","hEGenJetVsCorECasJet",nebin,emin,emax,nebin,emin,emax)
            self.hist["hPtGenJetVsCorPtCasJet"]      = ROOT.TH2F("hPtGenJetVsCorPtCasJet","hPtGenJetVsCorPtCasJet",nptbin,ptmin,ptmax,nptbin,ptmin,ptmax)

            self.hist["hPtGenJetVsPtCasJet_EtaPhiCut"]    = ROOT.TH2F("hPtGenJetVsPtCasJet_EtaPhiCut","hPtGenJetVsPtCasJet_EtaPhiCut",nptbin,ptmin,ptmax,nptbin,ptmin,ptmax)
            self.hist["hPtGenJetVsPtCasJet_NoSecJet"]     = ROOT.TH2F("hPtGenJetVsPtCasJet_NoSecJet","hPtGenJetVsPtCasJet_NoSecJet",nptbin,ptmin,ptmax,nptbin,ptmin,ptmax)
            self.hist["hPtGenJetVsPtCasJet_NoPartInCone"] = ROOT.TH2F("hPtGenJetVsPtCasJet_NoPartInCone","hPtGenJetVsPtCasJet_NoPartInCone",nptbin,ptmin,ptmax,nptbin,ptmin,ptmax)

            self.hist["hCountMergedJet"] = ROOT.TH1F("hCountMergedJet","hCountMergedJet",10,0,10)

            self.hist["hdNdEak5GenJetsHOT"]            = ROOT.TH1F("hdNdEak5GenJetsHOT","hdNdEak5GenJetsHOT",nebin,emin,emax)
            self.hist["hdNdEak5GenJetsHOT_TrgMedJet"]  = ROOT.TH1F("hdNdEak5GenJetsHOT_TrgMedJet","hdNdEak5GenJetsHOT_TrgMedJet",nebin,emin,emax)
            self.hist["hdNdEak5GenJetsHOT_TrgHighJet"] = ROOT.TH1F("hdNdEak5GenJetsHOT_TrgHighJet","hdNdEak5GenJetsHOT_TrgHighJet",nebin,emin,emax)

            self.hist["hdNdPtak5GenJetsHOT"]            = ROOT.TH1F("hdNdPtak5GenJetsHOT","hdNdPtak5GenJetsHOT",nptbin,ptmin,ptmax)
            self.hist["hdNdPtak5GenJetsHOT_TrgMedJet"]  = ROOT.TH1F("hdNdPtak5GenJetsHOT_TrgMedJet","hdNdPtak5GenJetsHOT_TrgMedJet",nptbin,ptmin,ptmax)
            self.hist["hdNdPtak5GenJetsHOT_TrgHighJet"] = ROOT.TH1F("hdNdPtak5GenJetsHOT_TrgHighJet","hdNdPtak5GenJetsHOT_TrgHighJet",nptbin,ptmin,ptmax)

            # self.hist[""]

            bb = array('d',[])
            nb = 3
            bmin = 250.
            bmax = 2500.
            for i in range(nb+1):
                b = log(bmin) + i*(log(bmax)-log(bmin))/nb
                bb.append(exp(b))

            self.hist["pECasJetGenReco"]          = ROOT.TProfile("pECasJetGenReco","pECasJetGenReco",len(bb)-1,bb)
            self.hist["ptest"]                    = ROOT.TProfile("ptest","ptest",len(bb)-1,bb)

            self.hist["hdNdPtHotCasGenJet"]       = ROOT.TH1F("hdNdPtHotCasGenJet","hdNdPtHotCasGenJet",nptbin,ptmin,ptmax)
            self.hist["hdNdPtHotCenGenJet"]       = ROOT.TH1F("hdNdPtHotCenGenJet","hdNdPtHotCenGenJet",nptbin,ptmin,ptmax)
            self.hist["hdNdDeltaPhiCasCenGenJet"] = ROOT.TH1F("hdNdDeltaPhiCasCenGenJet","hdNdDeltaPhiCasCenGenJet",50,-pi,pi)
            self.hist["hdNdDeltaPtCenCasGenJet"]  = ROOT.TH1F("hdNdDeltaPtCenCasGenJet","hdNdDeltaPtCenCasGenJet",40,-1,1)
            self.hist["hdNdDeltaEtaCenCasGenJet"] = ROOT.TH1F("hdNdDeltaEtaCenCasGenJet","hdNdDeltaEtaCenCasGenJet",20,0,10)

            self.hist["hdNdDeltaPhiCasCenRecoGenJet"] = ROOT.TH1F("hdNdDeltaPhiCasCenRecoGenJet","hdNdDeltaPhiCasCenRecoGenJet",50,-pi,pi)
            self.hist["hdNdDeltaPtCenCasGenRecoJet"]  = ROOT.TH1F("hdNdDeltaPtCenCasGenRecoJet","hdNdDeltaPtCenCasGenRecoJet",40,-1,1)
            self.hist["hdNdDeltaEtaCenCasGenRecoJet"] = ROOT.TH1F("hdNdDeltaEtaCenCasGenRecoJet","hdNdDeltaEtaCenCasGenRecoJet",20,0,10)

            self.hist["hPtVsPtCenCasGenJet"] = ROOT.TH2F("hPtVsPtCenCasGenJet","hPtVsPtCenCasGenJet",nptbin,ptmin,ptmax,nptbin,ptmin,ptmax)
            self.hist["hEVsECenCasGenJet"]   = ROOT.TH2F("hEVsECenCasGenJet","hEVsECenCasGenJet",nebin,emin,emax,nebin,emin,emax)

            self.hist["hPtVsPtCenCasGenRecoJet"] = ROOT.TH2F("hPtVsPtCenCasGenRecoJet","hPtVsPtCenCasGenRecoJet",nptbin,ptmin,ptmax,nptbin,ptmin,ptmax)
            self.hist["hEVsECenCasGenRecoJet"]   = ROOT.TH2F("hEVsECenCasGenRecoJet","hEVsECenCasGenRecoJet",nebin,emin,emax,nebin,emin,emax)

            self.hist["hdNdENotMergedCasJet"]  = ROOT.TH1F("hdNdENotMergedCasJet","hdNdENotMergedCasJet",nebin,emin,emax)
            self.hist["hdNdPtNotMergedCasJet"] = ROOT.TH1F("hdNdPtNotMergedCasJet","hdNdPtNotMergedCasJet",nptbin,ptmin,ptmax)
            self.hist["hdNdEMergedCasJet"]     = ROOT.TH1F("hdNdEMergedCasJet","hdNdEMergedCasJet",nebin,emin,emax)
            self.hist["hdNdPtMergedCasJet"]    = ROOT.TH1F("hdNdPtMergedCasJet","hdNdPtMergedCasJet",nptbin,ptmin,ptmax)

            self.hist["hdNdEtadPtHotCasRegionGenJet"] = ROOT.TH2F("hdNdEtadPtHotCasRegionGenJet","hdNdEtadPtHotCasRegionGenJet",nptbin,ptmin,ptmax,netabin,etamin,etamax)
            self.hist["hdNdEtadPtHotCasRegionGenRecoJet"] = ROOT.TH2F("hdNdEtadPtHotCasRegionGenRecoJet","hdNdEtadPtHotCasRegionGenRecoJet",nptbin,ptmin,ptmax,netabin,etamin,etamax)
            self.hist["hdNDeltaEtadPtHotCasRegionGenJet"] = ROOT.TH2F("hdNDeltaEtadPtHotCasRegionGenJet","hdNDeltaEtadPtHotCasRegionGenJet",nptbin,ptmin,ptmax,24,0,1.2)
            self.hist["hdNDeltaEtadPtHotCasRegionGenRecoJet"] = ROOT.TH2F("hdNDeltaEtadPtHotCasRegionGenRecoJet","hdNDeltaEtadPtHotCasRegionGenRecoJet",nptbin,ptmin,ptmax,24,0,1.2)

            for ideta in xrange(0,15):
                for idphi in xrange(0,6):
                    str_name_1 = "hRM_PtVsPt_GenRecoJet_{de}_{dp}".format(de=ideta,dp=idphi)
                    self.hist[str_name_1] = ROOT.TH2F(str_name_1,str_name_1,nptbin,ptmin,ptmax,nptbin,ptmin,ptmax)
                    str_name_2 = "hRM_Count_{de}_{dp}".format(de=ideta,dp=idphi)
                    self.hist[str_name_2] = ROOT.TH1F(str_name_2,str_name_2,10,0,10)
                    str_name_3 = "hRM_Pt_RecoJet_NoFake_{de}_{dp}".format(de=ideta,dp=idphi)
                    self.hist[str_name_3] = ROOT.TH1F(str_name_3,str_name_3,nptbin,ptmin,ptmax)
                    str_name_4 = "hRM_Pt_RecoJet_Fake_{de}_{dp}".format(de=ideta,dp=idphi)
                    self.hist[str_name_4] = ROOT.TH1F(str_name_4,str_name_4,nptbin,ptmin,ptmax)
                    str_name_5 = "hRM_Pt_RecoJet_Ratio_{de}_{dp}".format(de=ideta,dp=idphi)
                    self.hist[str_name_5] = ROOT.TH1F(str_name_5,str_name_5,nptbin,ptmin,ptmax)
                    str_name_6 = "hRM_Pt_RecoJet_Misses_{de}_{dp}".format(de=ideta,dp=idphi)
                    self.hist[str_name_6] = ROOT.TH1F(str_name_6,str_name_6,nptbin,ptmin,ptmax)
                    str_name_7 = "hRM_Pt_RecoJet_RatMis_{de}_{dp}".format(de=ideta,dp=idphi)
                    self.hist[str_name_7] = ROOT.TH1F(str_name_7,str_name_7,nptbin,ptmin,ptmax)

        self.hist["hdNdEak5CastorJetsHOT_Only"]            =  ROOT.TH1F("hdNdEak5CastorJetsHOT_Only","hdNdEak5CastorJetsHOT_Only",nebin,emin,emax)
        self.hist["hdNdEak5CastorJetsHOT_Only_TrgMedJet"]  =  ROOT.TH1F("hdNdEak5CastorJetsHOT_Only_TrgMedJet","hdNdEak5CastorJetsHOT_Only_TrgMedJet",nebin,emin,emax)
        self.hist["hdNdEak5CastorJetsHOT_Only_TrgHighJet"] =  ROOT.TH1F("hdNdEak5CastorJetsHOT_Only_TrgHighJet","hdNdEak5CastorJetsHOT_Only_TrgHighJet",nebin,emin,emax)

        self.hist["hdNdPtak5CastorJetsHOT_Only"]            =  ROOT.TH1F("hdNdPtak5CastorJetsHOT_Only","hdNdPtak5CastorJetsHOT_Only",nptbin,ptmin,ptmax)
        self.hist["hdNdPtak5CastorJetsHOT_Only_TrgMedJet"]  =  ROOT.TH1F("hdNdPtak5CastorJetsHOT_Only_TrgMedJet","hdNdPtak5CastorJetsHOT_Only_TrgMedJet",nptbin,ptmin,ptmax)
        self.hist["hdNdPtak5CastorJetsHOT_Only_TrgHighJet"] =  ROOT.TH1F("hdNdPtak5CastorJetsHOT_Only_TrgHighJet","hdNdPtak5CastorJetsHOT_Only_TrgHighJet",nptbin,ptmin,ptmax)        

        self.hist["hDeltaPhiRecoJetHotCasJet"] = ROOT.TH1F("hDeltaPhiRecoJetHotCasJet","hDeltaPhiRecoJetHotCasJet",50,-pi,pi)

        self.hist["hdNdEtaak4CaloJets"]  =  ROOT.TH1F("hdNdEtaak4CaloJets","hdNdEtaak4CaloJets",60,-6,6)

        self.hist["hdNdEak5CastorJets"]  =  ROOT.TH1F("hdNdEak5CastorJets","hdNdEak5CastorJets",nebin,emin,emax)
        self.hist["hdNdPtak5CastorJets"] =  ROOT.TH1F("hdNdPtak5CastorJets","hdNdPtak5CastorJets",nptbin,ptmin,ptmax)
        self.hist["hNTowak5CastorJets"]  =  ROOT.TH1F("hNTowak5CastorJets","hNTowak5CastorJets",7,-0.5,6.5)

        self.hist["hdNdEak5CastorJetsHOT"]            =  ROOT.TH1F("hdNdEak5CastorJetsHOT","hdNdEak5CastorJetsHOT",nebin,emin,emax)
        self.hist["hdNdEak5CastorJetsHOT_TrgMedJet"]  =  ROOT.TH1F("hdNdEak5CastorJetsHOT_TrgMedJet","hdNdEak5CastorJetsHOT_TrgMedJet",nebin,emin,emax)
        self.hist["hdNdEak5CastorJetsHOT_TrgHighJet"] =  ROOT.TH1F("hdNdEak5CastorJetsHOT_TrgHighJet","hdNdEak5CastorJetsHOT_TrgHighJet",nebin,emin,emax)

        self.hist["hdNdEak5CastorJetsHOT_ZB"]            =  ROOT.TH1F("hdNdEak5CastorJetsHOT_ZB","hdNdEak5CastorJetsHOT_ZB",nebin,emin,emax)
        self.hist["hdNdEak5CastorJetsHOT_ZB_TrgMedJet"]  =  ROOT.TH1F("hdNdEak5CastorJetsHOT_ZB_TrgMedJet","hdNdEak5CastorJetsHOT_ZB_TrgMedJet",nebin,emin,emax)
        self.hist["hdNdEak5CastorJetsHOT_ZB_TrgHighJet"] =  ROOT.TH1F("hdNdEak5CastorJetsHOT_ZB_TrgHighJet","hdNdEak5CastorJetsHOT_ZB_TrgHighJet",nebin,emin,emax)

        self.hist["hdNdEak5CastorJetsHOT_ZBMB"]             =  ROOT.TH1F("hdNdEak5CastorJetsHOT_ZBMB","hdNdEak5CastorJetsHOT_ZBMB",nebin,emin,emax)
        self.hist["hdNdEak5CastorJetsHOT_ZBMB_TrgMedJet"]   =  ROOT.TH1F("hdNdEak5CastorJetsHOT_ZBMB_TrgMedJet","hdNdEak5CastorJetsHOT_ZBMB_TrgMedJet",nebin,emin,emax)
        self.hist["hdNdEak5CastorJetsHOT_ZBMB_TrgHighJet"]  =  ROOT.TH1F("hdNdEak5CastorJetsHOT_ZBMB_TrgHighJet","hdNdEak5CastorJetsHOT_ZBMB_TrgHighJet",nebin,emin,emax)

        self.hist["hdNdPtak5CastorJetsHOT"]             =  ROOT.TH1F("hdNdPtak5CastorJetsHOT","hdNdPtak5CastorJetsHOT",nptbin,ptmin,ptmax)
        self.hist["hdNdPtak5CastorJetsHOT_TrgMedJet"]   =  ROOT.TH1F("hdNdPtak5CastorJetsHOT_TrgMedJet","hdNdPtak5CastorJetsHOT_TrgMedJet",nptbin,ptmin,ptmax)
        self.hist["hdNdPtak5CastorJetsHOT_TrgHighJet"]  =  ROOT.TH1F("hdNdPtak5CastorJetsHOT_TrgHighJet","hdNdPtak5CastorJetsHOT_TrgHighJet",nptbin,ptmin,ptmax)

        self.hist["hdNdCorrEak5CastorJetsHOT"]            =  ROOT.TH1F("hdNdCorrEak5CastorJetsHOT","hdNdCorrEak5CastorJetsHOT",nebin,emin,emax)
        self.hist["hdNdCorrEak5CastorJetsHOT_TrgMedJet"]  =  ROOT.TH1F("hdNdCorrEak5CastorJetsHOT_TrgMedJet","hdNdCorrEak5CastorJetsHOT_TrgMedJet",nebin,emin,emax)
        self.hist["hdNdCorrEak5CastorJetsHOT_TrgHighJet"] =  ROOT.TH1F("hdNdCorrEak5CastorJetsHOT_TrgHighJet","hdNdCorrEak5CastorJetsHOT_TrgHighJet",nebin,emin,emax)

        self.hist["hdNdCorrPtak5CastorJetsHOT"]            =  ROOT.TH1F("hdNdCorrPtak5CastorJetsHOT","hdNdCorrPtak5CastorJetsHOT",nptbin,ptmin,ptmax)
        self.hist["hdNdCorrPtak5CastorJetsHOT_TrgMedJet"]  =  ROOT.TH1F("hdNdCorrPtak5CastorJetsHOT_TrgMedJet","hdNdCorrPtak5CastorJetsHOT_TrgMedJet",nptbin,ptmin,ptmax)
        self.hist["hdNdCorrPtak5CastorJetsHOT_TrgHighJet"] =  ROOT.TH1F("hdNdCorrPtak5CastorJetsHOT_TrgHighJet","hdNdCorrPtak5CastorJetsHOT_TrgHighJet",nptbin,ptmin,ptmax)


        # ======================
        phimin = -pi
        phimax = pi
        nphibin = 16

        self.hist["hdNdPhiak5CastorJetsHOT"]            = ROOT.TH1F("hdNdPhiak5CastorJetsHOT","hdNdPhiak5CastorJetsHOT",nphibin,phimin,phimax)
        self.hist["hdNdPhiak5CastorJetsHOT_TrgMedJet"]  = ROOT.TH1F("hdNdPhiak5CastorJetsHOT_TrgMedJet","hdNdPhiak5CastorJetsHOT_TrgMedJet",nphibin,phimin,phimax)
        self.hist["hdNdPhiak5CastorJetsHOT_TrgHighJet"] = ROOT.TH1F("hdNdPhiak5CastorJetsHOT_TrgHighJet","hdNdPhiak5CastorJetsHOT_TrgHighJet",nphibin,phimin,phimax)

        self.hist["hdNdPhiak5CastorJetsHOT_ZB"]            = ROOT.TH1F("hdNdPhiak5CastorJetsHOT_ZB","hdNdPhiak5CastorJetsHOT_ZB",nphibin,phimin,phimax)
        self.hist["hdNdPhiak5CastorJetsHOT_ZB_TrgMedJet"]  = ROOT.TH1F("hdNdPhiak5CastorJetsHOT_ZB_TrgMedJet","hdNdPhiak5CastorJetsHOT_ZB_TrgMedJet",nphibin,phimin,phimax)
        self.hist["hdNdPhiak5CastorJetsHOT_ZB_TrgHighJet"] = ROOT.TH1F("hdNdPhiak5CastorJetsHOT_ZB_TrgHighJet","hdNdPhiak5CastorJetsHOT_ZB_TrgHighJet",nphibin,phimin,phimax)

        self.hist["hdNdPhiak5CastorJetsHOT_ZBMB"]            = ROOT.TH1F("hdNdPhiak5CastorJetsHOT_ZBMB","hdNdPhiak5CastorJetsHOT_ZBMB",nphibin,phimin,phimax)
        self.hist["hdNdPhiak5CastorJetsHOT_ZBMB_TrgMedJet"]  = ROOT.TH1F("hdNdPhiak5CastorJetsHOT_ZBMB_TrgMedJet","hdNdPhiak5CastorJetsHOT_ZBMB_TrgMedJet",nphibin,phimin,phimax)
        self.hist["hdNdPhiak5CastorJetsHOT_ZBMB_TrgHighJet"] = ROOT.TH1F("hdNdPhiak5CastorJetsHOT_ZBMB_TrgHighJet","hdNdPhiak5CastorJetsHOT_ZBMB_TrgHighJet",nphibin,phimin,phimax)

        self.hist["hdNdPhiak5CastorJetsHOT_Ecut"]            = ROOT.TH1F("hdNdPhiak5CastorJetsHOT_Ecut","hdNdPhiak5CastorJetsHOT_Ecut",nphibin,phimin,phimax)
        self.hist["hdNdPhiak5CastorJetsHOT_Ecut_TrgMedJet"]  = ROOT.TH1F("hdNdPhiak5CastorJetsHOT_Ecut_TrgMedJet","hdNdPhiak5CastorJetsHOT_Ecut_TrgMedJet",nphibin,phimin,phimax)
        self.hist["hdNdPhiak5CastorJetsHOT_Ecut_TrgHighJet"] = ROOT.TH1F("hdNdPhiak5CastorJetsHOT_Ecut_TrgHighJet","hdNdPhiak5CastorJetsHOT_Ecut_TrgHighJet",nphibin,phimin,phimax)

        self.hist["hdNdEdPhiak5CastorJetsHOT"]            = ROOT.TH2F("hdNdEdPhiak5CastorJetsHOT","hdNdEdPhiak5CastorJetsHOT",nebin,emin,emax,nphibin,phimin,phimax)
        self.hist["hdNdEdPhiak5CastorJetsHOT_TrgMedJet"]  = ROOT.TH2F("hdNdEdPhiak5CastorJetsHOT_TrgMedJet","hdNdEdPhiak5CastorJetsHOT_TrgMedJet",nebin,emin,emax,nphibin,phimin,phimax)
        self.hist["hdNdEdPhiak5CastorJetsHOT_TrgHighJet"] = ROOT.TH2F("hdNdEdPhiak5CastorJetsHOT_TrgHighJet","hdNdEdPhiak5CastorJetsHOT_TrgHighJet",nebin,emin,emax,nphibin,phimin,phimax)

        self.hist["hdNdPtdPhiak5CastorJetsHOT"]            = ROOT.TH2F("hdNdPtdPhiak5CastorJetsHOT","hdNdPtdPhiak5CastorJetsHOT",nptbin,ptmin,ptmax,nphibin,phimin,phimax)
        self.hist["hdNdPtdPhiak5CastorJetsHOT_TrgMedJet"]  = ROOT.TH2F("hdNdPtdPhiak5CastorJetsHOT_TrgMedJet","hdNdPtdPhiak5CastorJetsHOT_TrgMedJet",nptbin,ptmin,ptmax,nphibin,phimin,phimax)
        self.hist["hdNdPtdPhiak5CastorJetsHOT_TrgHighJet"] = ROOT.TH2F("hdNdPtdPhiak5CastorJetsHOT_TrgHighJet","hdNdPtdPhiak5CastorJetsHOT_TrgHighJet",nptbin,ptmin,ptmax,nphibin,phimin,phimax)

        self.hist["hdNdEdPhiak5CastorJetsHOT_ZB"]            = ROOT.TH2F("hdNdEdPhiak5CastorJetsHOT_ZB","hdNdEdPhiak5CastorJetsHOT_ZB",nebin,emin,emax,nphibin,phimin,phimax)
        self.hist["hdNdEdPhiak5CastorJetsHOT_ZB_TrgMedJet"]  = ROOT.TH2F("hdNdEdPhiak5CastorJetsHOT_ZB_TrgMedJet","hdNdEdPhiak5CastorJetsHOT_ZB_TrgMedJet",nebin,emin,emax,nphibin,phimin,phimax)
        self.hist["hdNdEdPhiak5CastorJetsHOT_ZB_TrgHighJet"] = ROOT.TH2F("hdNdEdPhiak5CastorJetsHOT_ZB_TrgHighJet","hdNdEdPhiak5CastorJetsHOT_ZB_TrgHighJet",nebin,emin,emax,nphibin,phimin,phimax)

        self.hist["hdNdEdPhiak5CastorJetsHOT_ZBMB"]            = ROOT.TH2F("hdNdEdPhiak5CastorJetsHOT_ZBMB","hdNdEdPhiak5CastorJetsHOT_ZBMB",nebin,emin,emax,nphibin,phimin,phimax)
        self.hist["hdNdEdPhiak5CastorJetsHOT_ZBMB_TrgMedJet"]  = ROOT.TH2F("hdNdEdPhiak5CastorJetsHOT_ZBMB_TrgMedJet","hdNdEdPhiak5CastorJetsHOT_ZBMB_TrgMedJet",nebin,emin,emax,nphibin,phimin,phimax)
        self.hist["hdNdEdPhiak5CastorJetsHOT_ZBMB_TrgHighJet"] = ROOT.TH2F("hdNdEdPhiak5CastorJetsHOT_ZBMB_TrgHighJet","hdNdEdPhiak5CastorJetsHOT_ZBMB_TrgHighJet",nebin,emin,emax,nphibin,phimin,phimax)
        # ======================



        # ======================
        zmin = -16000
        zmax = -14000
        nzbin = 80

        self.hist["hdNdZak5CastorJetsHOT"]            = ROOT.TH1F("hdNdZak5CastorJetsHOT","hdNdZak5CastorJetsHOT",nzbin,zmin,zmax)
        self.hist["hdNdZak5CastorJetsHOT_TrgMedJet"]  = ROOT.TH1F("hdNdZak5CastorJetsHOT_TrgMedJet","hdNdZak5CastorJetsHOT_TrgMedJet",nzbin,zmin,zmax)
        self.hist["hdNdZak5CastorJetsHOT_TrgHighJet"] = ROOT.TH1F("hdNdZak5CastorJetsHOT_TrgHighJet","hdNdZak5CastorJetsHOT_TrgHighJet",nzbin,zmin,zmax)

        self.hist["hdNdZdPhiak5CastorJetsHOT"]            = ROOT.TH2F("hdNdZdPhiak5CastorJetsHOT","hdNdZdPhiak5CastorJetsHOT",nzbin,zmin,zmax,nphibin,phimin,phimax)
        self.hist["hdNdZdPhiak5CastorJetsHOT_TrgMedJet"]  = ROOT.TH2F("hdNdZdPhiak5CastorJetsHOT_TrgMedJet","hdNdZdPhiak5CastorJetsHOT_TrgMedJet",nzbin,zmin,zmax,nphibin,phimin,phimax)
        self.hist["hdNdZdPhiak5CastorJetsHOT_TrgHighJet"] = ROOT.TH2F("hdNdZdPhiak5CastorJetsHOT_TrgHighJet","hdNdZdPhiak5CastorJetsHOT_TrgHighJet",nzbin,zmin,zmax,nphibin,phimin,phimax)
        # ======================



        self.hist["hEvsFem_ak5CastorJetsHOT_TrgMedJet"]  = ROOT.TH2F("hEvsFem_ak5CastorJetsHOT_TrgMedJet","hEvsFem_ak5CastorJetsHOT_TrgMedJet",nebin,emin,emax,10,0,1)
        self.hist["hEvsFem_ak5CastorJetsHOT_TrgHighJet"] = ROOT.TH2F("hEvsFem_ak5CastorJetsHOT_TrgHighJet","hEvsFem_ak5CastorJetsHOT_TrgHighJet",nebin,emin,emax,10,0,1)


        self.hist["Tower_Energy"]            = ROOT.TH1F("Tower_Energy","Tower_Energy",30,0,500e3)
        self.hist["Tower_Energy_TrgMedJet"]  = ROOT.TH1F("Tower_Energy_TrgMedJet","Tower_Energy_TrgMedJet",30,0,500e3)
        self.hist["Tower_Energy_TrgHighJet"] = ROOT.TH1F("Tower_Energy_TrgHighJet","Tower_Energy_TrgHighJet",30,0,500e3)
        self.hist["dPhi_HotTower_HotCasJet"] = ROOT.TH1F("dPhi_HotTower_HotCasJet","dPhi_HotTower_HotCasJet",10,-pi,pi)


        self.hist["htest"] = ROOT.TH2F("htest","htest",100,-pi,pi,100,-pi,3*pi)
        self.hist["htest2"] = ROOT.TH2F("htest2","htest2",100,0,10,100,0,2*pi)



        for h in self.hist:
            self.hist[h].Sumw2()
            self.GetOutputList().Add(self.hist[h])

        # self.SectorBorders = [ 0.,    pi/8.,    pi/4.,  3*pi/8.,  pi/2.,  5*pi/8., 3*pi/4., 7*pi/8., 
        #                        pi, -7*pi/8., -3*pi/4., -5*pi/8., -pi/2., -3*pi/8.,  -pi/4.,  -pi/8. ]
                                
        self.TmpLorVec = ROOT.ROOT.Math.LorentzVector('ROOT::Math::PxPyPzE4D<double>')()
        self.energy_corr_factor = 1.46

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
        if self.isData and bx < 200:
            return 0

        # algo100prescale = self.getPrescaleAlog100(run,lumi)
        # if algo100prescale < 0: return 0

        NCastorRecoJets = self.fChain.ak5CastorJetsP4.size()
        if NCastorRecoJets == 0:
            return 0

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


        self.hist["TrgCount"].Fill("all",1)
        if CastorMedJetTrg:  self.hist["TrgCount"].Fill("MedJet",1)
        if CastorHighJetTrg: self.hist["TrgCount"].Fill("HighJet",1)
        if ZeroBiasTrg:      self.hist["TrgCount"].Fill("ZeroBias",1)
        if MinBiasTrg:       self.hist["TrgCount"].Fill("MinBias",1)
        if RandomTrg:        self.hist["TrgCount"].Fill("RndTrg",1)
        if self.fChain.trgCastorMedJet: self.hist["TrgCount"].Fill("MedJet_HLT",1)
        if self.fChain.trgCastorHighJet: self.hist["TrgCount"].Fill("HighJet_HLT",1)


        isCastorJetSample = False
        if "data_CastorJets_Run2015A" in self.datasetName:
            isCastorJetSample = True

        # to overwrite previous result
        isCastorJetSample = False

        max_tower_em_sat = True
        if isCastorJetSample:
            max_tower_em_sat = False

            if self.fChain.CastorRecHitisSaturated.size() != 224:
                return 0

            # reshape -> ch_eng[sec][mod]
            ch_mod = np.array(self.fChain.CastorRecHitModule).reshape(16,14)
            ch_sec = np.array(self.fChain.CastorRecHitSector).reshape(16,14)
            ch_eng = np.array(self.fChain.CastorRecHitEnergy).reshape(16,14)
            ch_sat = np.array(self.fChain.CastorRecHitisSaturated).reshape(16,14)


            # tow_eng = np.sum(ma.masked_array(ch_eng, mask=(ch_mod>12)&(ch_mod<3)), axis=1)
            # another test to get the sector with the overall hottest energy and check for saturation
            tow_eng = np.sum(ma.masked_array(ch_eng, mask=(ch_mod>12)), axis=1)
            max_tower_e   = tow_eng.max()
            max_tower_sec = tow_eng.argmax()

            if ch_sat[max_tower_sec][0] and ch_sat[max_tower_sec][1]:
                max_tower_em_sat = True
            # 
            # Use instead a more relax condition to see a better result
            # for isec in xrange(0,16):
            #     if ch_sat[isec][0] and ch_sat[isec][1]:
            #         max_tower_em_sat = True

            if CastorMedJetTrg:
                self.hist["Tower_Energy"].Fill(max_tower_e, weight)
            if CastorMedJetTrg and max_tower_em_sat:
                self.hist["Tower_Energy_TrgMedJet"].Fill(max_tower_e, weight)
            if CastorHighJetTrg and max_tower_em_sat:
                self.hist["Tower_Energy_TrgHighJet"].Fill(max_tower_e, weight)


        CastorRecoJets = []
        CorrCastorRecoJets = []
        for ijet in xrange(0,NCastorRecoJets):
            jet = self.fChain.ak5CastorJetsP4[ijet]
            nTow = self.fChain.ak5CastorJetsnTowers[ijet]
            fem = self.fChain.ak5CastorJetsfem[ijet]
            zDpt = self.fChain.ak5CastorJetsdepth[ijet]


            ReAbsCalibFactor = 1.
            # if "MelIntCalib_SumL1MinimumBiasHF" in self.datasetName:
            #     ReAbsCalibFactor = 1.0

            E  = ReAbsCalibFactor * jet.e()
            px = ReAbsCalibFactor * jet.px()
            py = ReAbsCalibFactor * jet.py()
            pz = ReAbsCalibFactor * jet.pz()

            jet.SetPxPyPzE(px,py,pz,E)
            
            # ecjet.SetPxPyPzE(self.energy_corr_factor*px,
            #                  self.energy_corr_factor*py,
            #                  self.energy_corr_factor*pz,
            #                  self.energy_corr_factor*E)

            self.hist["hdNdEak5CastorJets"].Fill(jet.e(), weight) 
            self.hist["hdNdPtak5CastorJets"].Fill(jet.pt(), weight)
            self.hist["hNTowak5CastorJets"].Fill(nTow, weight)

            if not self.jetPreCut(jet): CastorRecoJets.append([jet, nTow, fem, zDpt])
                
            # if not self.jetPreCut(ecjet): CorrCastorRecoJets.append(ecjet)

        CastorRecoJets.sort(cmp=compareSpecialListJetPt)
        if len(CastorRecoJets) > 0:
            jet = CastorRecoJets[0][0]
            ecjet = self.TmpLorVec
            ecjet = ecjet.SetPxPyPzE(self.energy_corr_factor*jet.px(),
                                     self.energy_corr_factor*jet.py(),
                                     self.energy_corr_factor*jet.pz(),
                                     self.energy_corr_factor*jet.E() )
            if not self.jetPreCut_corrE(ecjet): CorrCastorRecoJets.append(ecjet)


        # MaxCentralRecoJetPt = [0.,0.]
        # NCentralRecoJets = self.fChain.PFAK4Calophi.size()
        # for ijet in xrange(0,NCentralRecoJets):
        #     jetphi = self.fChain.PFAK4Calophi[ijet]
        #     jetpt  = self.fChain.PFAK4Calopt[ijet]

        #     if jetpt > MaxCentralRecoJetPt[0]:
        #         MaxCentralRecoJetPt[0] = jetpt
        #         MaxCentralRecoJetPt[1] = jetphi





        # trgpsc_weight = 1
        # if CastorMedJetTrg: trgpsc_weight = algo100prescale

        TrgMainSample = MinBiasTrg
        if "ZeroBias" in self.datasetName:
            TrgMainSample = ZeroBiasTrg
        elif "CastorJets" in self.datasetName:
            TrgMainSample = CastorMedJetTrg

        if len(CastorRecoJets) > 0:
            jet = CastorRecoJets[0][0]
            nTow = CastorRecoJets[0][1]
            fem = CastorRecoJets[0][2]
            zDpt = CastorRecoJets[0][3]
            if len(CorrCastorRecoJets) > 0: 
                ecjet = CorrCastorRecoJets[0]

            # if jet.e() > 200e3: return 0

            # fem_thr = 0.8
            # fem_thr = 1e6 # -> infinity for no threshold :)

            medjet_energy_trigger_threshold = False
            if jet.e() >= 2300:
                medjet_energy_trigger_threshold = True

            # if jet.phi() < 0 or jet.phi() > pi/8.: return 0
            # if not ch_sat[0][0] or not ch_sat[0][1]: return 0

            # self.hist["dPhi_HotTower_HotCasJet"].Fill( self.movePhiRange( jet.phi() - max_tower_sec*pi/8. ) )

            # if CastorDiJetTrg:
            #     if not NCentralRecoJets == 0:
            #         if jet.e() > 2000:
            #             dphi = self.movePhiRange( MaxCentralRecoJetPt[1] - jet.phi() )
            #             self.hist["hDeltaPhiRecoJetHotCasJet"].Fill(dphi)

            # ###########################################################################
            # just counting
            self.hist["hdNdEak5CastorJetsHOT_Only"].Fill(jet.e(), weight)
            self.hist["hdNdPtak5CastorJetsHOT_Only"].Fill(jet.pt(), weight)

            if CastorMedJetTrg:
                self.hist["hdNdEak5CastorJetsHOT_Only_TrgMedJet"].Fill(jet.e(), weight)
                self.hist["hdNdPtak5CastorJetsHOT_Only_TrgMedJet"].Fill(jet.pt(), weight)

            if CastorHighJetTrg:
                self.hist["hdNdEak5CastorJetsHOT_Only_TrgHighJet"].Fill(jet.e(), weight)
                self.hist["hdNdPtak5CastorJetsHOT_Only_TrgHighJet"].Fill(jet.pt(), weight)
            # ###########################################################################


            # if nTow == 2:
            if TrgMainSample:
            # if CastorMedJetTrg and max_tower_em_sat:
                self.hist["hdNdEak5CastorJetsHOT"].Fill(jet.e(), weight)
                self.hist["hdNdPtak5CastorJetsHOT"].Fill(jet.pt(), weight)

                self.hist["hdNdPhiak5CastorJetsHOT"].Fill(jet.phi(), weight)
                if medjet_energy_trigger_threshold: self.hist["hdNdPhiak5CastorJetsHOT_Ecut"].Fill(jet.phi(), weight)
                self.hist["hdNdEdPhiak5CastorJetsHOT"].Fill(jet.e(), jet.phi(), weight)
                self.hist["hdNdPtdPhiak5CastorJetsHOT"].Fill(jet.pt(), jet.phi(), weight)

                self.hist["hdNdZak5CastorJetsHOT"].Fill(zDpt, weight)
                self.hist["hdNdZdPhiak5CastorJetsHOT"].Fill(zDpt, jet.phi(), weight)
                if len(CorrCastorRecoJets) > 0: 
                    self.hist["hdNdCorrEak5CastorJetsHOT"].Fill(ecjet.e(), weight)
                    self.hist["hdNdCorrPtak5CastorJetsHOT"].Fill(ecjet.pt(), weight)

                self.hist["bx"].Fill( bx, weight )


            if CastorMedJetTrg and TrgMainSample and max_tower_em_sat:
            # if CastorMedJetTrg and max_tower_em_sat:
                self.hist["hdNdEak5CastorJetsHOT_TrgMedJet"].Fill(jet.e(), weight)
                self.hist["hdNdPtak5CastorJetsHOT_TrgMedJet"].Fill(jet.pt(), weight)
                self.hist["hEvsFem_ak5CastorJetsHOT_TrgMedJet"].Fill(jet.e(), fem, weight)

                self.hist["hdNdPhiak5CastorJetsHOT_TrgMedJet"].Fill(jet.phi(), weight)
                if medjet_energy_trigger_threshold: self.hist["hdNdPhiak5CastorJetsHOT_Ecut_TrgMedJet"].Fill(jet.phi(), weight)
                self.hist["hdNdEdPhiak5CastorJetsHOT_TrgMedJet"].Fill(jet.e(), jet.phi(), weight)
                self.hist["hdNdPtdPhiak5CastorJetsHOT_TrgMedJet"].Fill(jet.pt(), jet.phi(), weight)

                self.hist["hdNdZak5CastorJetsHOT_TrgMedJet"].Fill(zDpt, weight)
                self.hist["hdNdZdPhiak5CastorJetsHOT_TrgMedJet"].Fill(zDpt, jet.phi(), weight)
                if len(CorrCastorRecoJets) > 0: 
                    self.hist["hdNdCorrEak5CastorJetsHOT_TrgMedJet"].Fill(ecjet.e(), weight)
                    self.hist["hdNdCorrPtak5CastorJetsHOT_TrgMedJet"].Fill(ecjet.pt(), weight)

                self.hist["bx_MedJet"].Fill( bx, weight )


            if CastorHighJetTrg and TrgMainSample and max_tower_em_sat:
            # if CastorHighJetTrg and CastorMedJetTrg and max_tower_em_sat:
                self.hist["hdNdEak5CastorJetsHOT_TrgHighJet"].Fill(jet.e(), weight)
                self.hist["hdNdPtak5CastorJetsHOT_TrgHighJet"].Fill(jet.pt(), weight)
                self.hist["hEvsFem_ak5CastorJetsHOT_TrgHighJet"].Fill(jet.e(), fem, weight)

                self.hist["hdNdPhiak5CastorJetsHOT_TrgHighJet"].Fill(jet.phi(), weight)
                if medjet_energy_trigger_threshold: self.hist["hdNdPhiak5CastorJetsHOT_Ecut_TrgHighJet"].Fill(jet.phi(), weight)
                self.hist["hdNdEdPhiak5CastorJetsHOT_TrgHighJet"].Fill(jet.e(), jet.phi(), weight)
                self.hist["hdNdPtdPhiak5CastorJetsHOT_TrgHighJet"].Fill(jet.pt(), jet.phi(), weight)

                self.hist["hdNdZak5CastorJetsHOT_TrgHighJet"].Fill(zDpt, weight)
                self.hist["hdNdZdPhiak5CastorJetsHOT_TrgHighJet"].Fill(zDpt, jet.phi(), weight)
                if len(CorrCastorRecoJets) > 0: 
                    self.hist["hdNdCorrEak5CastorJetsHOT_TrgHighJet"].Fill(ecjet.e(), weight)
                    self.hist["hdNdCorrPtak5CastorJetsHOT_TrgHighJet"].Fill(ecjet.pt(), weight)


            ################################################
            # Additional for some special cases            #
            # Above one are main plots to take             #
            ################################################
            if ZeroBiasTrg:
                self.hist["hdNdEak5CastorJetsHOT_ZB"].Fill(jet.e(), weight)
                self.hist["hdNdPhiak5CastorJetsHOT_ZB"].Fill(jet.phi(), weight)
                self.hist["hdNdEdPhiak5CastorJetsHOT_ZB"].Fill(jet.e(), jet.phi(), weight)

            if CastorMedJetTrg and ZeroBiasTrg:
                self.hist["hdNdEak5CastorJetsHOT_ZB_TrgMedJet"].Fill(jet.e(), weight)
                self.hist["hdNdPhiak5CastorJetsHOT_ZB_TrgMedJet"].Fill(jet.phi(), weight)
                self.hist["hdNdEdPhiak5CastorJetsHOT_ZB_TrgMedJet"].Fill(jet.e(), jet.phi(), weight)

            if CastorHighJetTrg and ZeroBiasTrg:
                self.hist["hdNdEak5CastorJetsHOT_ZB_TrgHighJet"].Fill(jet.e(), weight)
                self.hist["hdNdPhiak5CastorJetsHOT_ZB_TrgHighJet"].Fill(jet.phi(), weight)
                self.hist["hdNdEdPhiak5CastorJetsHOT_ZB_TrgHighJet"].Fill(jet.e(), jet.phi(), weight)

            if ZeroBiasTrg and MinBiasTrg:
                self.hist["hdNdEak5CastorJetsHOT_ZBMB"].Fill(jet.e(), weight)
                self.hist["hdNdPhiak5CastorJetsHOT_ZBMB"].Fill(jet.phi(), weight)
                self.hist["hdNdEdPhiak5CastorJetsHOT_ZBMB"].Fill(jet.e(), jet.phi(), weight)

            if CastorMedJetTrg and ZeroBiasTrg and MinBiasTrg:
                self.hist["hdNdEak5CastorJetsHOT_ZBMB_TrgMedJet"].Fill(jet.e(), weight)
                self.hist["hdNdPhiak5CastorJetsHOT_ZBMB_TrgMedJet"].Fill(jet.phi(), weight)
                self.hist["hdNdEdPhiak5CastorJetsHOT_ZBMB_TrgMedJet"].Fill(jet.e(), jet.phi(), weight)

            if CastorHighJetTrg and ZeroBiasTrg and MinBiasTrg:
                self.hist["hdNdEak5CastorJetsHOT_ZBMB_TrgHighJet"].Fill(jet.e(), weight)
                self.hist["hdNdPhiak5CastorJetsHOT_ZBMB_TrgHighJet"].Fill(jet.phi(), weight)
                self.hist["hdNdEdPhiak5CastorJetsHOT_ZBMB_TrgHighJet"].Fill(jet.e(), jet.phi(), weight)
            ################################################



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
                if len(CorrCastorRecoJets) > 0: 
                    HottestCorrCasJet = CorrCastorRecoJets[0]
                # NTowerHotCastorJet = 4

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
                    if len(CorrCastorRecoJets) > 0: 
                        self.hist["hEGenJetVsCorECasJet"].Fill( HottestCorrCasJet.e(), MergedGenCastorJet.e(), weight )
                        self.hist["hPtGenJetVsCorPtCasJet"].Fill( HottestCorrCasJet.pt(), MergedGenCastorJet.pt(), weight )
                    self.hist["hdNdEMergedCasJet"].Fill( HottestCastorJet.e() )
                    self.hist["hdNdPtMergedCasJet"].Fill( HottestCorrCasJet.pt() )

                
                LooseMergedGenJets = []
                for jet in self.fChain.ak5GenJetsp4:
                    dRecoJet = self.getDcone(HottestCastorJet,jet)
                    if dRecoJet < 0.5+0.5: LooseMergedGenJets.append(jet)
                LooseMergedGenJets.sort(cmp=compareJetPt)

                if len(LooseMergedGenJets) != 1:
                    self.hist["hdNdENotMergedCasJet"].Fill( HottestCastorJet.e() )
                    self.hist["hdNdPtNotMergedCasJet"].Fill( HottestCastorJet.pt() )


            mindphi = 0.5
            mindeta = 0.5
            dphi = 10.0
            # for ijet in xrange(0,len(CastorRecoJets)):
            for ideta in xrange(0,15):
                for idphi in xrange(0,6):
                    str_name_1 = "hRM_PtVsPt_GenRecoJet_{de}_{dp}".format(de=ideta,dp=idphi)
                    str_name_2 = "hRM_Count_{de}_{dp}".format(de=ideta,dp=idphi)
                    str_name_3 = "hRM_Pt_RecoJet_NoFake_{de}_{dp}".format(de=ideta,dp=idphi)
                    str_name_4 = "hRM_Pt_RecoJet_Fake_{de}_{dp}".format(de=ideta,dp=idphi)
                    str_name_5 = "hRM_Pt_RecoJet_Ratio_{de}_{dp}".format(de=ideta,dp=idphi)
                    str_name_6 = "hRM_Pt_RecoJet_Misses_{de}_{dp}".format(de=ideta,dp=idphi)
                    str_name_7 = "hRM_Pt_RecoJet_RatMis_{de}_{dp}".format(de=ideta,dp=idphi)
                    mindeta = float(ideta)/10.
                    mindphi = float(idphi)/10.
                    # used_genjet_list = []
                    if len(CastorRecoJets) > 0:
                        cjet = CastorRecoJets[0][0]
                        mgjet = None # merged gen jet
                        hotgenjet = None # hottest gen jet
                        for gjet in self.fChain.ak5GenJetsp4:
                            # if gjet.eta() > -5.9+mindeta or gjet.eta() < -6.6-mindeta:
                            if gjet.eta() > -5.9+mindeta or gjet.eta() < -5.9-mindeta:
                                continue
                            if not hotgenjet: hotgenjet = gjet
                            if hotgenjet.pt() < gjet.pt(): hotgenjet = gjet
                            # if gjet in used_genjet_list:
                                # continue
                            dphi = abs(self.getDphi(cjet,gjet))
                            if dphi < mindphi:
                                mgjet = gjet
                        if mgjet:
                            self.hist[str_name_1].Fill(cjet.pt(),mgjet.pt(),weight)
                            self.hist[str_name_2].Fill("no fake",1)
                            self.hist[str_name_3].Fill(cjet.pt(), weight)
                            # used_genjet_list.append(mgjet)
                            if not mgjet == hotgenjet and hotgenjet:
                                self.hist[str_name_6].Fill(hotgenjet.pt(),weight)
                                self.hist[str_name_7].Fill(hotgenjet.pt(),weight)
                        else:
                            self.hist[str_name_2].Fill("fake",1)
                            self.hist[str_name_4].Fill(cjet.pt(), weight)
                            self.hist[str_name_5].Fill(cjet.pt(), weight)
                            if hotgenjet: 
                                self.hist[str_name_6].Fill(hotgenjet.pt(),weight)
                                self.hist[str_name_7].Fill(hotgenjet.pt(),weight)

        # for jet_eta in self.fChain.PFAK4Caloeta:
        #     self.hist["hdNdEtaak4CaloJets"].Fill(jet_eta, weight)


        if not self.isData:
            CastorRangeGenJets = []
            CastorGenJets = []
            CentralGenJets = []
            for jet in self.fChain.ak5GenJetsp4:
                if jet.eta() > -7.1 and jet.eta() < -4.7: CastorRangeGenJets.append(jet)
                if not self.jetPreCut_corrE(jet): CastorGenJets.append(jet)

                if jet.eta() > -5 and jet.eta() <  5:
                    CentralGenJets.append(jet)

            CastorRangeGenJets.sort(cmp=compareJetPt)
            CastorGenJets.sort(cmp=compareJetPt)
            CentralGenJets.sort(cmp=compareJetPt)

            nCasJet = len(CastorGenJets)
            nCenJet = len(CentralGenJets)


            if len(CastorRangeGenJets) > 0:
                deltaeta = abs(CastorRangeGenJets[0].eta() + 5.9)
                self.hist["hdNdEtadPtHotCasRegionGenJet"].Fill( CastorRangeGenJets[0].pt(), CastorRangeGenJets[0].eta(), weight )
                if len(CastorRecoJets) > 0:
                    self.hist["hdNdEtadPtHotCasRegionGenRecoJet"].Fill( CastorRecoJets[0][0].pt(), CastorRangeGenJets[0].eta(), weight )
                    self.hist["hdNDeltaEtadPtHotCasRegionGenRecoJet"].Fill( CastorRecoJets[0][0].pt(), deltaeta, weight )
                if len(CastorGenJets) > 0:
                    self.hist["hdNDeltaEtadPtHotCasRegionGenJet"].Fill( CastorGenJets[0].pt(), deltaeta, weight )

            if nCenJet > 1:
                if CentralGenJets[0].pt() < CentralGenJets[1].pt():
                    raise Exception("Jet sort incorrect!!!")

            if nCasJet > 0: 
                CasJet = CastorGenJets[0]

                self.hist["hdNdPtHotCasGenJet"].Fill( CasJet.pt(), weight )

                if TrgMainSample:
                    self.hist["hdNdEak5GenJetsHOT"].Fill( CasJet.e(), weight)
                    self.hist["hdNdPtak5GenJetsHOT"].Fill( CasJet.pt(), weight)
                if CastorMedJetTrg and TrgMainSample and max_tower_em_sat:
                    self.hist["hdNdEak5GenJetsHOT_TrgMedJet"].Fill( CasJet.e(), weight)
                    self.hist["hdNdPtak5GenJetsHOT_TrgMedJet"].Fill( CasJet.pt(), weight)
                if CastorHighJetTrg and TrgMainSample and max_tower_em_sat:
                    self.hist["hdNdEak5GenJetsHOT_TrgHighJet"].Fill( CasJet.e(), weight)
                    self.hist["hdNdPtak5GenJetsHOT_TrgHighJet"].Fill( CasJet.pt(), weight)
                
                if len(CorrCastorRecoJets) > 0:
                    ecjet = CorrCastorRecoJets[0]
                    self.hist["hdNdEak5GenVsRecoJets"].Fill( ecjet.e(), CasJet.e(), weight)
                    self.hist["hdNdPtak5GenVsRecoJets"].Fill( ecjet.pt(), CasJet.pt(), weight)


                self.hist["hNentries"].Fill( 1, weight )
                
            if nCenJet > 0: 
                self.hist["hdNdPtHotCenGenJet"].Fill( CentralGenJets[0].pt(), weight )

            if nCasJet > 0 and nCenJet > 0:

                CasJet = CastorGenJets[0]
                CenJet = CentralGenJets[0]

                ptcut = 5
                if CasJet.pt() > ptcut and CenJet.pt() > ptcut:

                    dphi = self.movePhiRange( CenJet.phi() - CasJet.phi() )
                    self.hist["hdNdDeltaPhiCasCenGenJet"].Fill( dphi, weight )

                    dijetDphiAndIso = True

                    if abs(dphi) < 2.7: dijetDphiAndIso = False

                    pcut = 0.2 * (CenJet.pt()+CasJet.pt())/2
                    if nCasJet > 1:
                        if CastorGenJets[1].pt() > pcut: dijetDphiAndIso = False
                    if nCenJet > 1:
                        if CentralGenJets[1].pt() > pcut: dijetDphiAndIso = False

                    if dijetDphiAndIso:
                        self.hist["hNentries"].Fill( 2, weight )
                        self.hist["hPtVsPtCenCasGenJet"].Fill( CasJet.pt(), CenJet.pt(), weight )
                        self.hist["hEVsECenCasGenJet"].Fill( CasJet.e(), CenJet.e(), weight )

                        dpt = (CenJet.pt()-CasJet.pt())/(CenJet.pt()+CasJet.pt())
                        self.hist["hdNdDeltaPtCenCasGenJet"].Fill( dpt, weight )

                        deta = CenJet.eta()-CasJet.eta()
                        self.hist["hdNdDeltaEtaCenCasGenJet"].Fill( deta, weight )

            if nCenJet > 0 and len(CorrCastorRecoJets) > 0:

                CasJet = CorrCastorRecoJets[0]
                CenJet = CentralGenJets[0]

                ptcut = 5
                if CasJet.pt() > ptcut and CenJet.pt() > ptcut:

                    dphi = self.movePhiRange( CenJet.phi() - CasJet.phi() )
                    self.hist["hdNdDeltaPhiCasCenRecoGenJet"].Fill( dphi, weight )     

                    dijetDphiAndIso = True

                    if abs(dphi) < 2.7: dijetDphiAndIso = False

                    pcut = 0.2 * (CenJet.pt()+CasJet.pt())/2
                    if len(CastorRecoJets) > 1:
                        if CastorRecoJets[1][0].pt()*self.energy_corr_factor > pcut: dijetDphiAndIso = False
                    if nCenJet > 1:
                        if CentralGenJets[1].pt() > pcut: dijetDphiAndIso = False

                    if dijetDphiAndIso:
                        self.hist["hPtVsPtCenCasGenRecoJet"].Fill( CasJet.pt(), CenJet.pt(), weight )
                        self.hist["hEVsECenCasGenRecoJet"].Fill( CasJet.e(), CenJet.e(), weight )

                        dpt = (CenJet.pt()-CasJet.pt())/(CenJet.pt()+CasJet.pt())
                        self.hist["hdNdDeltaPtCenCasGenRecoJet"].Fill( dpt, weight )

                        deta = CenJet.eta()-CasJet.eta()
                        self.hist["hdNdDeltaEtaCenCasGenRecoJet"].Fill( deta, weight )


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

        for ideta in xrange(0,15):
            for idphi in xrange(0,6):
                str_name_3 = "hRM_Pt_RecoJet_NoFake_{de}_{dp}".format(de=ideta,dp=idphi)
                str_name_5 = "hRM_Pt_RecoJet_Ratio_{de}_{dp}".format(de=ideta,dp=idphi)
                str_name_7 = "hRM_Pt_RecoJet_RatMis_{de}_{dp}".format(de=ideta,dp=idphi)

                histos[str_name_5].Divide(histos[str_name_3])
                histos[str_name_7].Divide(histos[str_name_3])



        # if not self.isData:
        #     histos["hNak5GenJets"].Scale( 1./histos["hNentries"].GetBinContent(1) )

        #     histos["hdNdEak5GenJets"].Scale( 1./histos["hNentries"].GetBinContent(1) )
        #     histos["hdNdPtak5GenJets"].Scale( 1./histos["hNentries"].GetBinContent(1) )
        #     histos["hdNdEtaak5GenJets"].Scale( 1./histos["hNentries"].GetBinContent(1) )

        #     histos["hdNdPtHotCasGenJet"].Scale( 1./histos["hNentries"].GetBinContent(1) )
        #     histos["hdNdPtHotCenGenJet"].Scale( 1./histos["hNentries"].GetBinContent(1) )
        #     histos["hdNdDeltaPhiCasCenGenJet"].Scale( 1./histos["hNentries"].GetBinContent(1) )
        #     histos["hdNdDeltaPtCenCasGenJet"].Scale( 1./histos["hNentries"].GetBinContent(1) )
        #     histos["hdNdDeltaEtaCenCasGenJet"].Scale( 1./histos["hNentries"].GetBinContent(1) )

        # histos["hdNdEtaak4CaloJets"].Scale( 1./histos["hNentries"].GetBinContent(1) )

        # histos["hdNdEak5CastorJets"].Scale( 1./histos["hNentries"].GetBinContent(1) )
        # histos["hdNdPtak5CastorJets"].Scale( 1./histos["hNentries"].GetBinContent(1) )
        # histos["hNTowak5CastorJets"].Scale( 1./histos["hNentries"].GetBinContent(1) )

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
    nWorkers = 1 #None # Use all cpu cores

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

    # maxFilesMC = 50
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
           outFile = "plotsGenJetAnalysis_TEST_2015AIC.root" )
