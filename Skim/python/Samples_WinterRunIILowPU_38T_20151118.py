anaVersion="WinterRunIILowPU_38T_20151118"
anaType="WinterRunIILowPU_38T"

cbSmartCommand="smartCopy"
cbSmartBlackList=""
cbWMS="https://wmscms.cern.ch:7443/glite_wms_wmproxy_server"
skimEfficiencyMethod="getSkimEff"

sam = {}

sam["data_ExpressPhysics_Run2015E"]={}
sam["data_ExpressPhysics_Run2015E"]["crabJobs"]=50
sam["data_ExpressPhysics_Run2015E"]["GT"]='GR_R_75_V5A'
sam["data_ExpressPhysics_Run2015E"]["name"]='data_ExpressPhysics_Run2015E'
sam["data_ExpressPhysics_Run2015E"]["isData"]=True
sam["data_ExpressPhysics_Run2015E"]["numEvents"]=310395
# sam["data_ExpressPhysics_Run2015E"]["pathSE"]='srm://srm-eoscms.cern.ch:8443/srm/v2/server?SFN=/eos/cms/store/group/phys_heavyions/cwohrman/CFF/CastorJets/ZeroBias1/Long_RunIILowPU_0T_20150820_data_ZeroBias1_Run2015A/150928_131441/0000/'
# sam["data_ExpressPhysics_Run2015E"]["pathTrees"]='/XXXTMFTTree/store/group/phys_heavyions/cwohrman/CFF/CastorJets/ZeroBias1/Long_RunIILowPU_0T_20150820_data_ZeroBias1_Run2015A/150928_131441/0000//'
sam["data_ExpressPhysics_Run2015E"]["json"]='CommonFSQFramework/Skim/lumi/Run261445.json'
sam["data_ExpressPhysics_Run2015E"]["lumiMinBias"]=-1
sam["data_ExpressPhysics_Run2015E"]["XS"]=-1
# sam["data_ExpressPhysics_Run2015E"]["pathPAT"]='/XXXTMFPAT/store/group/phys_heavyions/cwohrman/CFF/CastorJets/ZeroBias1/Long_RunIILowPU_0T_20150820_data_ZeroBias1_Run2015A/150928_131441/0000//'
sam["data_ExpressPhysics_Run2015E"]["DS"]='/ExpressPhysics/Run2015E-Express-v1/FEVT'

def fixLocalPaths(sam):
        import os,imp
        if "SmallXAnaDefFile" not in os.environ:
            print "Please set SmallXAnaDefFile environment variable:"
            print "export SmallXAnaDefFile=FullPathToFile"
            raise Exception("Whooops! SmallXAnaDefFile env var not defined")

        anaDefFile = os.environ["SmallXAnaDefFile"]
        mod_dir, filename = os.path.split(anaDefFile)
        mod, ext = os.path.splitext(filename)
        f, filename, desc = imp.find_module(mod, [mod_dir])
        mod = imp.load_module(mod, f, filename, desc)

        localBasePathPAT = mod.PATbasePATH
        localBasePathTrees = mod.TTreeBasePATH

        for s in sam:
            if "pathPAT" in sam[s]:
                sam[s]["pathPAT"] = sam[s]["pathPAT"].replace("XXXTMFPAT", localBasePathPAT)
            if "pathTrees" in sam[s]:
                sam[s]["pathTrees"] = sam[s]["pathTrees"].replace("XXXTMFTTree", localBasePathTrees)
            #print sam[s]["pathPAT"]
            #print sam[s]["pathTrees"]
        return sam
sam = fixLocalPaths(sam)