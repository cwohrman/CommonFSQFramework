import FWCore.ParameterSet.Config as cms
import CommonFSQFramework.Core.Util
import os

isData = True

if "TMFSampleName" not in os.environ:
    print "TMFSampleName not found, assuming we are running on MC"
else:
    s = os.environ["TMFSampleName"]
    sampleList=CommonFSQFramework.Core.Util.getAnaDefinition("sam")
    isData =  sampleList[s]["isData"]
    if isData: print "Disabling MC-specific features for sample",s

# for test purpose
# isData = False

process = cms.Process("Treemaker")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10000))

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

# Source
if not isData:
    process.source = cms.Source("PoolSource",
        # fileNames = cms.untracked.vstring('/store/user/hvanhaev/ZeroBias1/Run2015A-v1_RERECO_Run247324_GR_P_V54_withCustomCond-v1/150608_213851/0000/output_data_rereco_1.root')
        #fileNames = cms.untracked.vstring('/store/user/hvanhaev/MinBias_TuneMonash13_13TeV-pythia8/RunIISpring15DR74-NoPU0T_MCRUN2_740TV0_step2-v2/150610_055012/0000/step2_RAW2DIGI_L1Reco_RECO_1.root')
        fileNames = cms.untracked.vstring('/store/mc/RunIISpring15DR74/ReggeGribovPartonMC_13TeV-EPOS/GEN-SIM-RECO/NoPURawReco_castor_MCRUN2_74_V8B-v1/10000/BC62D29E-7707-E511-A6D9-AC853D9F5344.root')
    )
if isData: 
    process.source = cms.Source("PoolSource",
        # fileNames = cms.untracked.vstring('/store/data/Run2015A/ZeroBias/RECO/PromptReco-v1/000/247/607/00000/52EA626D-9210-E511-843F-02163E01451D.root')
        fileNames = cms.untracked.vstring("/store/data/Run2015A/CastorJets/RECO/PromptReco-v1/000/247/607/00000/0066B745-A010-E511-B055-02163E014374.root")
    )


# from PhysicsTools.PatAlgos.patInputFiles_cff import filesRelValProdTTbarGENSIMRECO
# process.source.fileNames = filesRelValProdTTbarGENSIMRECO

# Geometry and Detector Conditions
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
if isData: process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')
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



###############################################################################
###############################################################################

###########################################################################
# Add PAT calo Jets # !!! Still with old JEC (Jet Energy Corrections) !!! #
###########################################################################
## switch to uncheduled mode
process.options.allowUnscheduled = cms.untracked.bool(True)
#process.Tracer = cms.Service("Tracer")

process.load("PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff")
process.load("PhysicsTools.PatAlgos.selectionLayer1.selectedPatCandidates_cff")

from PhysicsTools.PatAlgos.tools.metTools import addMETCollection
addMETCollection(process, labelName='patMETPF', metSource='pfMetT1')

## uncomment the following line to add different jet collections
## to the event content
from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection
from PhysicsTools.PatAlgos.tools.jetTools import switchJetCollection

# uncomment the following lines to switch to ak4CaloJets in your PAT output
labelAK4Calo = 'AK4Calo'
addJetCollection(
   process,
   labelName = labelAK4Calo,
   jetSource = cms.InputTag('ak4CaloJets'),
   jetCorrections = ('AK7Calo', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'Type-1'), # FIXME: Use proper JECs, as soon as available
   btagDiscriminators = [
       'pfJetBProbabilityBJetTags'
     , 'pfJetProbabilityBJetTags'
     , 'pfTrackCountingHighPurBJetTags'
     , 'pfTrackCountingHighEffBJetTags'
     , 'pfSimpleSecondaryVertexHighEffBJetTags'
     , 'pfSimpleSecondaryVertexHighPurBJetTags'
     , 'pfCombinedInclusiveSecondaryVertexV2BJetTags'
     ]
)
process.patJetsAK4Calo.useLegacyJetMCFlavour=True # Need to use legacy flavour since the new flavour requires jet constituents which are dropped for CaloJets from AOD
###############################################################################
###############################################################################



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
            file = cms.FileInPath('data/gain__1200x4_1600x10_led0to38.txt')
        ),
        cms.PSet(
            object = cms.string('ChannelQuality'),
            file = cms.FileInPath('data/quality__2015.txt')
        )
     )
  )
# else if it is MC then using only chanel quality changes
else:
  process.es_ascii = cms.ESSource("CastorTextCalibrations",
      input = cms.VPSet(
        cms.PSet(
            object = cms.string('ChannelQuality'),
            file = cms.FileInPath('data/quality__2015.txt')
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
    )
else:
    process.rechitcorrector = cms.EDProducer("RecHitCorrector",
            rechitLabel = cms.InputTag("castorreco","","RECO"), # choose the original RecHit collection
            revertFactor = cms.double(1), # this is the factor to go back to the original fC - not needed when data is already intercalibrated
            doInterCalib = cms.bool(False) # don't do intercalibration, RecHitCorrector will only correct the EM response and remove BAD channels
    )
process.CastorTowerReco.inputprocess = "rechitcorrector"
process.CastorReReco = cms.Path(process.rechitcorrector*process.CastorFullReco)
###############################################################################
###############################################################################

# define treeproducer
process.JetCastor = cms.EDAnalyzer("CFFTreeProducer")

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
process.JetCastor._Parameterizable__setParameters(CommonFSQFramework.Core.CastorViewsConfigs.get(["ak5CastorJetView"]))
# process.JetCastor._Parameterizable__setParameters(CommonFSQFramework.Core.CastorViewsConfigs.get(["ak5CastorJetView","CastorRecHitViewBasic"]))
# process.JetCastor._Parameterizable__setParameters(CommonFSQFramework.Core.PFObjectsViewsConfigs.get(["PFCandidateView","ecalPFClusterView","hcalPFClusterView","hfPFClusterView"]))
process.JetCastor._Parameterizable__setParameters(CommonFSQFramework.Core.TriggerResultsViewsConfigs.get(["CastorSpecialJetTriggerResultsView","L1GTriggerResultsView"]))
process.JetCastor._Parameterizable__setParameters(CommonFSQFramework.Core.JetViewsConfigs.get(["JetViewAK4Calo"]))

if not isData:
    process.JetCastor._Parameterizable__setParameters(CommonFSQFramework.Core.GenLevelViewsConfigs.get(["GenPartView"]))
    process.JetCastor._Parameterizable__setParameters(CommonFSQFramework.Core.GenLevelViewsConfigs.get(["lowPtak5GenJetView"]))

    process = CommonFSQFramework.Core.customizePAT.addPath(process, process.LowPtGenJetsReCluster)


process = CommonFSQFramework.Core.customizePAT.addPath(process, process.CastorReReco)    
process = CommonFSQFramework.Core.customizePAT.addTreeProducer(process, process.JetCastor)
