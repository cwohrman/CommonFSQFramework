import FWCore.ParameterSet.Config as cms
import CommonFSQFramework.Core.Util
import os

isData = True

if "TMFSampleName" not in os.environ:
    print "TMFSampleName not found, assuming we are running on RECO data"
else:
    s = os.environ["TMFSampleName"]
    sampleList=CommonFSQFramework.Core.Util.getAnaDefinition("sam")
    isData =  sampleList[s]["isData"]
    if isData: print "Disabling MC-specific features for sample",s

# for test purpose
# isData = False

process = cms.Process("Treemaker")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

# Source
if not isData:
    process.source = cms.Source("PoolSource",
        # fileNames = cms.untracked.vstring('/store/user/hvanhaev/ZeroBias1/Run2015A-v1_RERECO_Run247324_GR_P_V54_withCustomCond-v1/150608_213851/0000/output_data_rereco_1.root')
        #fileNames = cms.untracked.vstring('/store/user/hvanhaev/MinBias_TuneMonash13_13TeV-pythia8/RunIISpring15DR74-NoPU0T_MCRUN2_740TV0_step2-v2/150610_055012/0000/step2_RAW2DIGI_L1Reco_RECO_1.root')
        # fileNames = cms.untracked.vstring('/store/mc/RunIISpring15DR74/ReggeGribovPartonMC_13TeV-EPOS/GEN-SIM-RECO/NoPURawReco_castor_MCRUN2_74_V8B-v1/10000/BC62D29E-7707-E511-A6D9-AC853D9F5344.root')
        # fileNames = cms.untracked.vstring('/store/mc/RunIISpring15DR74/ReggeGribovPartonMC_13TeV-EPOS/GEN-SIM-RECO/NoPURawReco_castor_MCRUN2_74_V8B_ext1-v1/00000/5E628F10-B40E-E511-BB28-008CFA1111D0.root')
        # fileNames = cms.untracked.vstring('/store/mc/RunIISpring15DR74/ReggeGribovPartonMC_castorJet_13TeV-EPOS/AODSIM/NoPU_castor_MCRUN2_74_V8-v2/00000/C40F2FBD-B007-E511-9F1E-001E67397215.root')
        # fileNames = cms.untracked.vstring('/store/caf/user/vardan/castor2015/measured/reco_000.root')
    )
if isData: 
    process.source = cms.Source("PoolSource",
        # fileNames = cms.untracked.vstring('/store/data/Run2015A/ZeroBias/RECO/PromptReco-v1/000/247/607/00000/52EA626D-9210-E511-843F-02163E01451D.root')
        # fileNames = cms.untracked.vstring('/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/246/908/00000/0AE1AFA5-220B-E511-B7D4-02163E014239.root')
        # fileNames = cms.untracked.vstring("/store/data/Run2015A/CastorJets/RECO/PromptReco-v1/000/247/607/00000/0066B745-A010-E511-B055-02163E014374.root")
        # fileNames = cms.untracked.vstring('root://eoscms.cern.ch//eos/cms/store/express/Run2015A/ExpressPhysics/FEVT/Express-v1/000/247/324/00000/D04CD2F9-130D-E511-B157-02163E014147.root')

        fileNames = cms.untracked.vstring(
          '/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/246/865/00000/C60316FA-150B-E511-AFCE-02163E0136E1.root',
          '/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/246/908/00000/0AE1AFA5-220B-E511-B7D4-02163E014239.root',
          '/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/246/908/00000/0CADC28A-390B-E511-853D-02163E0121C5.root',
          '/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/246/908/00000/10D9909F-260B-E511-9A53-02163E014113.root',
          '/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/246/908/00000/168661B7-300B-E511-870A-02163E013653.root',
          '/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/246/908/00000/1A1D4A18-2E0B-E511-9A5A-02163E012925.root',
          '/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/246/908/00000/1CC6C5E8-220B-E511-8640-02163E011ACE.root',
          '/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/246/908/00000/1E5ADEF5-200B-E511-B722-02163E01184D.root',
          '/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/246/908/00000/1E84CAD2-230B-E511-88F9-02163E013861.root',
          '/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/246/908/00000/20A71F54-550B-E511-B4DD-02163E0142F3.root',
          '/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/246/908/00000/20FBFCC6-240B-E511-A826-02163E012925.root',
          '/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/246/908/00000/2275F0CE-200B-E511-B714-02163E0143FC.root',
          '/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/246/908/00000/26CE2328-410B-E511-833A-02163E01184E.root',
          '/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/246/908/00000/2A151439-2C0B-E511-A1E1-02163E01383E.root',
          '/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/246/908/00000/2C44A971-230B-E511-B5E3-02163E012925.root',
          '/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/246/908/00000/34DC8712-220B-E511-8CE6-02163E0146EE.root',
          '/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/246/908/00000/3C37180B-220B-E511-AA12-02163E014220.root',
          '/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/246/908/00000/4862A3D9-220B-E511-A2CF-02163E013491.root',
          '/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/246/908/00000/4A84D28D-160B-E511-B9A2-02163E0142BF.root',
          '/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/246/908/00000/542C34A0-270B-E511-862E-02163E011BDB.root',
          '/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/246/908/00000/5C1F3477-230B-E511-BD27-02163E0142D7.root',
          '/store/data/Run2015A/ZeroBias1/RECO/PromptReco-v1/000/246/908/00000/62A6E7A7-250B-E511-A56F-02163E011DBC.root',
        )
    )



# from PhysicsTools.PatAlgos.patInputFiles_cff import filesRelValProdTTbarGENSIMRECO
# process.source.fileNames = filesRelValProdTTbarGENSIMRECO

# Geometry and Detector Conditions
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
if isData: process.GlobalTag = GlobalTag(process.GlobalTag, 'GR_P_V56', '')
if not isData: process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')
process.load("Configuration.StandardSequences.MagneticField_cff")

# for test purpose
# process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_75_V5', '')

print process.GlobalTag.globaltag
# process.load("Configuration.StandardSequences.Reconstruction_cff")




###############################################################################
###############################################################################

if not isData:
    ############################
    # Add ReReco of ak5GenJets #
    ############################
    process.load('RecoJets.Configuration.GenJetParticles_cff')
    process.load('RecoJets.Configuration.RecoGenJets_cff')
    from RecoJets.JetProducers.ak5GenJets_cfi import ak5GenJets
    process.lowPtak5GenJets = ak5GenJets.clone(jetPtMin = 0.5 )
    process.LowPtGenJetsReCluster = cms.Path(process.lowPtak5GenJets)
###############################################################################
###############################################################################



# ###############################################################################
# ###############################################################################

# ###########################################################################
# # Add PAT calo Jets # !!! Still with old JEC (Jet Energy Corrections) !!! #
# ###########################################################################
# ## switch to uncheduled mode
# process.options.allowUnscheduled = cms.untracked.bool(True)
# #process.Tracer = cms.Service("Tracer")

# process.load("PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff")
# process.load("PhysicsTools.PatAlgos.selectionLayer1.selectedPatCandidates_cff")

# from PhysicsTools.PatAlgos.tools.metTools import addMETCollection
# addMETCollection(process, labelName='patMETPF', metSource='pfMetT1')

# ## uncomment the following line to add different jet collections
# ## to the event content
# from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection
# from PhysicsTools.PatAlgos.tools.jetTools import switchJetCollection

# # uncomment the following lines to switch to ak4CaloJets in your PAT output
# labelAK4Calo = 'AK4Calo'
# addJetCollection(
#    process,
#    labelName = labelAK4Calo,
#    jetSource = cms.InputTag('ak4CaloJets'),
#    jetCorrections = ('AK7Calo', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'Type-1'), # FIXME: Use proper JECs, as soon as available
#    btagDiscriminators = [
#        'pfJetBProbabilityBJetTags'
#      , 'pfJetProbabilityBJetTags'
#      , 'pfTrackCountingHighPurBJetTags'
#      , 'pfTrackCountingHighEffBJetTags'
#      , 'pfSimpleSecondaryVertexHighEffBJetTags'
#      , 'pfSimpleSecondaryVertexHighPurBJetTags'
#      , 'pfCombinedInclusiveSecondaryVertexV2BJetTags'
#      ]
# )
# process.patJetsAK4Calo.useLegacyJetMCFlavour=True # Need to use legacy flavour since the new flavour requires jet constituents which are dropped for CaloJets from AOD
# ###############################################################################
# ###############################################################################



# Here starts the CFF specific part
import CommonFSQFramework.Core.customizePAT
process = CommonFSQFramework.Core.customizePAT.customize(process)

# GT customization
process = CommonFSQFramework.Core.customizePAT.customizeGT(process)



###############################################################################
###############################################################################

############################################################################
# get custom CASTOR conditions to remove bad channels and gain corrections #
############################################################################
process.load("CondCore.DBCommon.CondDBSetup_cfi")
process.CastorDbProducer = cms.ESProducer("CastorDbProducer")

# when using data apply gain and quality corrections
if isData:
  process.es_ascii = cms.ESSource("CastorTextCalibrations",
      input = cms.VPSet(
        cms.PSet(
            object = cms.string('Gains'),
            # file = cms.FileInPath('data/gain__1200x4_1600x10_led0to38.txt')
            file = cms.FileInPath('data/gain_MelikeMuon_InterCalib_AbsCalib_AdjustToMeanFiveModInterCalibValues_20151105.txt')
            # file = cms.FileInPath('data/gain__1200x4_1600x10_4T.txt')
        ),
        cms.PSet(
            object = cms.string('ChannelQuality'),
            # file = cms.FileInPath('data/quality__2015.txt')
            # file = cms.FileInPath('data/quality__2015a.txt')
            file = cms.FileInPath('data/BadChannels_FinalManualSelection_20151113.txt')
        )
     )
  )
# else if it is MC then using only chanel quality changes
else:
  process.es_ascii = cms.ESSource("CastorTextCalibrations",
      input = cms.VPSet(
        cms.PSet(
            object = cms.string('ChannelQuality'),
            # file = cms.FileInPath('data/quality__2015.txt')
            file = cms.FileInPath('data/BadChannels_FinalManualSelection_20151113.txt')
        )
     )
  )

process.es_prefer_castor = cms.ESPrefer('CastorTextCalibrations','es_ascii')
###############################################################################
###############################################################################

###############################################################################
###############################################################################

########################
# Castor RecHit ReReco #
########################
process.load('RecoLocalCalo.Castor.Castor_cff')
# construct the module which executes the RechitCorrector for data reconstructed in releases >= 4.2.X
if isData:
    process.rechitcorrector = cms.EDProducer("RecHitCorrector",
            rechitLabel = cms.InputTag("castorreco","","RECO"), # choose the original RecHit collection
            revertFactor = cms.double(1), # this is the factor to go back to the original fC - not needed when data is already intercalibrated
            doInterCalib = cms.bool(True) # do intercalibration
            # For HighJet Trigger Test use not intercalib jets but still remove bad channels because some of them had really bad response
            # doInterCalib = cms.bool(False) # do intercalibration
    )
else:
    process.rechitcorrector = cms.EDProducer("RecHitCorrector",
            rechitLabel = cms.InputTag("castorreco","","RECO"), # choose the original RecHit collection
            revertFactor = cms.double(1), # this is the factor to go back to the original fC - not needed when data is already intercalibrated
            doInterCalib = cms.bool(False) # don't do intercalibration, RecHitCorrector will only correct the EM response and remove BAD channels
    )
process.CastorTowerReco.inputprocess = "rechitcorrector"
process.CastorReReco = cms.Path(process.rechitcorrector*process.CastorFullReco)
# process.CastorReReco = cms.Path(process.CastorFullReco)
###############################################################################
###############################################################################



###############################################################################
###############################################################################

# ########################
# # Castor Jet-pT Filter #
# ########################
# process.CastorJetFilter = cms.EDFilter("CastorJetFilter",
#     minCastorJetPt = cms.double(1.),
#     minCastorJetEnergy = cms.double(250.),
#     jetRadius = cms.double(0.5)
# )
# ###############################################################################
# ###############################################################################



###############################################################################
###############################################################################
# HLT path filter
process.hltzerobias = cms.EDFilter("HLTHighLevel",
     TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
     HLTPaths = cms.vstring('HLT_L1CastorMediumJet_v1'), # provide list of HLT paths (or patterns) you want
     eventSetupPathsKey = cms.string(''), # not empty => use read paths from AlCaRecoTriggerBitsRcd via this key #HLT_MinBiasBSC # HLT_L1Tech_BSC_minBias
     andOr = cms.bool(True),             # how to deal with multiple triggers: True (OR) accept if ANY is true, False (AND) accept if ALL are true
     throw = cms.bool(False)    # throw exception on unknown path names
) 
###############################################################################
###############################################################################



# define treeproducer
process.JetCastor = cms.EDAnalyzer("CFFTreeProducer")

# apply filter on treeproducer
process.FiltererdTree = cms.Path(process.hltzerobias*process.JetCastor)
# process.FiltererdTree = cms.Path(process.CastorJetFilter*process.JetCastor)

import CommonFSQFramework.Core.VerticesViewsConfigs
import CommonFSQFramework.Core.CaloRecHitViewsConfigs
import CommonFSQFramework.Core.CaloTowerViewsConfigs
import CommonFSQFramework.Core.CastorViewsConfigs
import CommonFSQFramework.Core.PFObjectsViewsConfigs
import CommonFSQFramework.Core.TriggerResultsViewsConfigs
import CommonFSQFramework.Core.JetViewsConfigs

if not isData:
    import CommonFSQFramework.Core.GenLevelViewsConfigs
    

# process.JetCastor._Parameterizable__setParameters(CommonFSQFramework.Core.VerticesViewsConfigs.get(["VerticesView"]))
# process.JetCastor._Parameterizable__setParameters(CommonFSQFramework.Core.CaloRecHitViewsConfigs.get(["HBHERecHitView","HFRecHitView"]))
# process.JetCastor._Parameterizable__setParameters(CommonFSQFramework.Core.CaloTowerViewsConfigs.get(["CaloTowerView"]))
# Add also Basic Castor RecHits to Skimmed tree also for Test purpose
# process.JetCastor._Parameterizable__setParameters(CommonFSQFramework.Core.CastorViewsConfigs.get(["ak5CastorJetView"]))
process.JetCastor._Parameterizable__setParameters(CommonFSQFramework.Core.CastorViewsConfigs.get(["ak5CastorJetView","CastorRecHitViewFull"]))
# process.JetCastor._Parameterizable__setParameters(CommonFSQFramework.Core.PFObjectsViewsConfigs.get(["PFCandidateView","ecalPFClusterView","hcalPFClusterView","hfPFClusterView"]))
process.JetCastor._Parameterizable__setParameters(CommonFSQFramework.Core.TriggerResultsViewsConfigs.get(["CastorSpecialJetTriggerResultsView","L1GTriggerResultsView"]))

# Jet View only works with pat::Jet; Need to uncomment pat::Jet creation lines before
# process.JetCastor._Parameterizable__setParameters(CommonFSQFramework.Core.JetViewsConfigs.get(["JetViewAK4Calo"]))

if not isData:
    process.JetCastor._Parameterizable__setParameters(CommonFSQFramework.Core.GenLevelViewsConfigs.get(["GenPartView"]))
    process.JetCastor._Parameterizable__setParameters(CommonFSQFramework.Core.GenLevelViewsConfigs.get(["lowPtak5GenJetView"]))

    process = CommonFSQFramework.Core.customizePAT.addPath(process, process.LowPtGenJetsReCluster)



process = CommonFSQFramework.Core.customizePAT.addPath(process, process.CastorReReco)

# Tree without filter
# process = CommonFSQFramework.Core.customizePAT.addTreeProducer(process, process.JetCastor)

# Tree with filter
process = CommonFSQFramework.Core.customizePAT.addPath(process, process.FiltererdTree)
