anaType="Long_RunIILowPU_0T"

# root path needs proper XXX
# some stuff needed for crab configuration, e.g. blacklisting
preamble='''
cbSmartCommand="smartCopy"
cbSmartBlackList=""
cbWMS="https://wmscms.cern.ch:7443/glite_wms_wmproxy_server"
skimEfficiencyMethod="getSkimEff"
'''

# point towards your list of samples you want
dsFile="CommonFSQFramework/Skim/python/ds_Long_RunIILowPU_0T.txt"

# define the util decorator. Functions marked with this wont turn into ds attribute
def util(func):
    setattr(func, "ignore", 1)
    return func
setattr(util, "ignore", 1) # for this function only


def DS(ds):
    return ds

def name(ds):
    split=ds.split("/") 
    if len(split) == 0: return None

    if "NoPU0TRawReco_magnetOff" in ds: return split[1]+"_MagnetOff"
    
    if not isData(ds): return split[1]

    if isData(ds):
	if "Commissioning2015" in ds: return "data_"+split[1]+"_Commissioning2015"
	if "Run2015A" in ds: return "data_"+split[1]+"_Run2015A"
	return "data_"+split[1]

def isData(ds):
    realData = False
    if "Commissioning2015" in ds: realData = True
    if "Run2015A" in ds: realData = True
    return realData

def json(ds):
    realData = isData(ds)
    if realData:
        return "CommonFSQFramework/Skim/lumi/LHCf_lowPUruns_v2.json"
    else:
        return ""

def crabJobs(ds):
    dsName = name(ds)
    # define to run 100 crab jobs
    # make something more clever, based on number of events in the dataset:
    # require around 50000 events to be processed per job
    return int(round(numEvents(ds)/200000.0))
    # return 20


def numEvents(ds):
    
    # 0T MC - put this first to work!
    if "ReggeGribovPartonMC_13TeV-EPOS_MagnetOff" in name(ds): return 998671
    if "ReggeGribovPartonMC_13TeV-QGSJetII_MagnetOff" in name(ds): return 980585
    if "MinBias_TuneMonash13_13TeV-pythia8_MagnetOff" in name(ds): return 953393
    if "MinBias_TuneZ2star_13TeV-pythia6_MagnetOff" in name(ds): return 998082
    if "MinBias_TuneMBR_13TeV-pythia8_MagnetOff" in name(ds): return 997146
    if "MinBias_TuneEE5C_13TeV-herwigpp_MagnetOff" in name(ds): return 997682
    
    # 3.8T MC
    if "MinBias_TuneMonash13_13TeV-pythia8" in name(ds): return 997552
    if "ReggeGribovPartonMC_13TeV-EPOS" in name(ds): return 998312
    if "ReggeGribovPartonMC_13TeV-QGSJetII" in name(ds): return 1000000
    if "MinBias_TuneZ2star_13TeV-pythia6" in name(ds): return 998098
    if "MinBias_TuneCUETP8M1_13TeV-pythia8" in name(ds): return 999330
    if "MinBias_TuneMBR_13TeV-pythia8" in name(ds): return 998920
    if "MinBias_TuneEE5C_13TeV-herwigpp" in name(ds): return 1000000 
    
    # data
    if "ZeroBias" in name(ds): return 2001085
    if "CastorJets" in name(ds): return 36204306

    if "L1MinimumBias" in name(ds):
        if "HF1" in name(ds): return 8450456
        if "HF2" in name(ds): return 8450345
        if "HF3" in name(ds): return 8449900
        if "HF4" in name(ds): return 8449353
        if "HF5" in name(ds): return 8448734
        if "HF6" in name(ds): return 8449157
        if "HF7" in name(ds): return 8449944
        if "HF8" in name(ds): return 8449349
        return 752615
    
    if "ZeroBias" in name(ds):
        return 36297806

    return evts

def GT(ds):
    if isData(ds): return "GR_R_75_V5A"
    
    # # 0T MC GT
    # if "magnetOff_MCRUN2_740TV0" in ds: return "MCRUN2_740TV0"
	
    # # 3.8T MC GT
    # if "NoPU_castor_MCRUN2_74_V8" in ds: return "MCRUN2_74_V8" 
    # if "NoPURawReco_castor_MCRUN2_74_V8B" in ds: return "MCRUN2_74_V8B"
    
    return "MCRUN2_75_V5"
    
def XS(ds):
    '''
    Note: all cross sections given in pb
    # http://iopscience.iop.org/0295-5075/96/2/21002
    LHCtotal= 73.5 mili b

    conversion factors cheatsheet:
    nano = 10^-6 mili
    nano = 10^-3 micro
    nano = 10^3 pico
    '''
    # if real data return nothing, not needed here but keep for other Templates
    realData = isData(ds)
    if realData:
        return -1

    # list all datasets
    # Give all XS in pb
    s = {}
    s["MinBias_TuneMonash13_13TeV-pythia8"] = 78418400000.0 # from DAS - McM
    s["MinBias_TuneCUETP8S1-HERAPDF_13TeV-pythia8"] = 78418400000.0
    s["ReggeGribovPartonMC_13TeV-EPOS"] = 78418400000.0
    s["ReggeGribovPartonMC_13TeV-QGSJetII"] = 78418400000.0
    s["MinBias_TuneZ2star_13TeV-pythia6"] = 78260000000.0
    s["MinBias_TuneCUETP8M1_13TeV-pythia8"] = 78418400000.0
    s["MinBias_TuneMBR_13TeV-pythia8"] = 78418400000.0
    s["MinBias_TuneEE5C_13TeV-herwigpp"] = 36460000000.0
    
    s["MinBias_TuneMonash13_13TeV-pythia8_MagnetOff"] = 78418400000.0 # from DAS - McM
    s["ReggeGribovPartonMC_13TeV-EPOS_MagnetOff"] = 78418400000.0
    s["ReggeGribovPartonMC_13TeV-QGSJetII_MagnetOff"] = 78418400000.0
    s["MinBias_TuneZ2star_13TeV-pythia6_MagnetOff"] = 78260000000.0
    s["MinBias_TuneCUETP8M1_13TeV-pythia8_MagnetOff"] = 78418400000.0
    s["MinBias_TuneMBR_13TeV-pythia8_MagnetOff"] = 78418400000.0
    s["MinBias_TuneEE5C_13TeV-herwigpp_MagnetOff"] = 36460000000.0


    dsName = name(ds)
    if dsName in s:
        return s[dsName]
    else:
        print "FIXME - XS missing for", dsName
        print '    s["'+dsName+'"] = '
    return -1

@util
def getLumi(ds, trg):
    '''
    all lumi values here should be given in picob
    '''
    
    realData = isData(ds)
    if realData:
        return -1
    
    # for MC just do something very simple for now
    lumi = float(numEvents(ds)/XS(ds)) # pb, Nevents/XS
    return lumi

def lumiMinBias(ds):
    return getLumi(ds,"minbias")


# could useful in the future
@util
def onTheFlyCustomization():
    ret = ""

    return ret
#setattr(onTheFlyCustomization, "ignore", 1)


fun = {}
import copy,types
glob = copy.copy(globals())
for f in glob:
    if type(glob[f])==types.FunctionType:
        if hasattr(glob[f],"ignore"): 
            print "Skip", f
            continue
        #print f
        fun[f]=glob[f]




