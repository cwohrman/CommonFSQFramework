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
        # fileNames = cms.untracked.vstring("/store/data/Run2015A/CastorJets/RECO/PromptReco-v1/000/247/607/00000/0066B745-A010-E511-B055-02163E014374.root")
        # fileNames = cms.untracked.vstring('root://eoscms.cern.ch//eos/cms/store/express/Run2015A/ExpressPhysics/FEVT/Express-v1/000/247/324/00000/D04CD2F9-130D-E511-B157-02163E014147.root')

        # express stream data from november
        # fileNames = cms.untracked.vstring('/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/261/380/00000/4A46897B-468D-E511-84C8-02163E0144F5.root')
        # express stream run 262021
        # fileNames = cms.untracked.vstring('/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/021/00000/06003B52-748E-E511-955F-02163E01224B.root',
        # '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/021/00000/1475BBE2-718E-E511-801A-02163E011B1F.root',
        # '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/021/00000/2E04A46E-728E-E511-9302-02163E0145B4.root',
        # '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/021/00000/328C9021-748E-E511-8212-02163E0137D5.root',
        # '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/021/00000/3C7F5269-728E-E511-890C-02163E01469D.root',
        # '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/021/00000/3E945330-758E-E511-BA34-02163E014632.root',
        # '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/021/00000/64AFD928-748E-E511-9B19-02163E01282C.root',
        # '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/021/00000/7C868CC5-768E-E511-8250-02163E0145B4.root',
        # '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/021/00000/98F5D22C-758E-E511-B2BA-02163E01440B.root',
        # '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/021/00000/E200BF12-768E-E511-948E-02163E0140FD.root',
        # '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/021/00000/E6F5EC88-748E-E511-A45B-02163E01207C.root')
        # express stream run 262171
        fileNames = cms.untracked.vstring('/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/0281A700-4F8F-E511-B7AE-02163E0146EC.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/028EC463-538F-E511-9B7E-02163E013794.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/04B311F6-5B8F-E511-97BF-02163E011D87.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/0A8EDFB5-518F-E511-B138-02163E011A0F.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/0E507745-5F8F-E511-88CF-02163E014589.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/10C37635-508F-E511-8338-02163E0142A0.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/147916C1-518F-E511-A26D-02163E014707.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/1C24EEF9-5B8F-E511-BD2B-02163E014386.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/22019EBF-5D8F-E511-A532-02163E011824.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/24B70CFA-568F-E511-B50D-02163E013459.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/24CC31D1-4F8F-E511-845E-02163E0146F3.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/345B397B-598F-E511-BE7A-02163E01358E.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/36B0872A-5F8F-E511-A5C5-02163E0136ED.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/3CBB64F2-4E8F-E511-B8F5-02163E014486.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/42FCFC62-638F-E511-B9EE-02163E014331.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/4C8E8661-538F-E511-9BA6-02163E0141DC.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/5446ACDB-528F-E511-AFE5-02163E0141DC.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/565A0558-588F-E511-A154-02163E0142D8.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/5AA6E23C-5F8F-E511-B4A5-02163E0144BA.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/5EE777DB-4F8F-E511-B944-02163E01253D.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/6232D4F1-5B8F-E511-AF45-02163E011824.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/6E9C98CB-518F-E511-B3D5-02163E0142EC.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/6EBC511A-5C8F-E511-A7DE-02163E01423A.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/7C68EA28-5F8F-E511-B59C-02163E014139.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/807FD9F9-568F-E511-817A-02163E0120D9.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/80BFDA12-5C8F-E511-B4FF-02163E0146FE.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/8845A0B5-518F-E511-A79B-02163E0145FB.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/9069AF69-538F-E511-86A4-02163E01381A.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/920F121C-5F8F-E511-8090-02163E0142A3.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/9261DD30-508F-E511-BBAE-02163E01286D.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/9AD08731-568F-E511-94CA-02163E0142EC.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/A4AEC8DC-548F-E511-BAF2-02163E014707.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/AECCD7D8-588F-E511-A377-02163E01450D.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/B0C139C8-518F-E511-8C05-02163E012A3B.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/B4428D74-598F-E511-B95B-02163E0125AE.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/B678CC09-528F-E511-9823-02163E01454A.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/BA466E8E-598F-E511-B9DD-02163E014178.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/BC7E3B6A-588F-E511-B8C4-02163E0144B8.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/C85841E1-548F-E511-82B4-02163E0125AE.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/CEEC9001-558F-E511-AF21-02163E013522.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/D0BEDB57-588F-E511-B3B7-02163E014347.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/D676B040-5F8F-E511-A5E2-02163E014486.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/D87C18D2-588F-E511-AB61-02163E01368D.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/DC8F855A-608F-E511-A07B-02163E014501.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/DE3D2228-5F8F-E511-A518-02163E01453A.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/E4B2928E-4E8F-E511-9219-02163E011E34.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/E624E723-5F8F-E511-A6E5-02163E01441F.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/EC13674C-588F-E511-B00D-02163E014347.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/F03329CE-598F-E511-AED3-02163E01453A.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/F2D07515-5E8F-E511-85C0-02163E011EF7.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/F6365B00-568F-E511-877E-02163E0146FE.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/F6411905-568F-E511-913E-02163E01469C.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/FA0C1AF8-5B8F-E511-9A69-02163E01454A.root',
        '/store/express/Run2015E/ExpressPhysics/FEVT/Express-v1/000/262/171/00000/FAF9BF65-608F-E511-9F54-02163E011EF7.root')
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
        ),
        cms.PSet(
            object = cms.string('ChannelQuality'),
            # file = cms.FileInPath('data/quality__2015.txt')
            file = cms.FileInPath('data/quality__2015_FirstFiveMod.txt')
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
###############################################################################
###############################################################################



###############################################################################
###############################################################################

########################
# Castor Jet-pT Filter #
########################
process.CastorJetFilter = cms.EDFilter("CastorJetFilter",
    minCastorJetPt = cms.double(1.),
    minCastorJetEnergy = cms.double(250.),
    jetRadius = cms.double(0.5)
)
###############################################################################
###############################################################################


# define treeproducer
process.JetCastor = cms.EDAnalyzer("CFFTreeProducer")
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
# process.JetCastor._Parameterizable__setParameters(CommonFSQFramework.Core.JetViewsConfigs.get(["JetViewAK4Calo"]))

if not isData:
    process.JetCastor._Parameterizable__setParameters(CommonFSQFramework.Core.GenLevelViewsConfigs.get(["GenPartView"]))
    process.JetCastor._Parameterizable__setParameters(CommonFSQFramework.Core.GenLevelViewsConfigs.get(["lowPtak5GenJetView"]))

    process = CommonFSQFramework.Core.customizePAT.addPath(process, process.LowPtGenJetsReCluster)



# process = CommonFSQFramework.Core.customizePAT.addPath(process, process.CastorReReco)
process = CommonFSQFramework.Core.customizePAT.addTreeProducer(process, process.JetCastor)
# process = CommonFSQFramework.Core.customizePAT.addPath(process, process.FiltererdTree)
