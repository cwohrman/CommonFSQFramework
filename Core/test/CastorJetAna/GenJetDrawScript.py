# here you can write down the draw functions/sequence/stuff you want to be executed with the main DrawTool.py program.
# For a complete list of all available functions and options
# please visit: https://twiki.cern.ch/twiki/bin/viewauth/CMS/CFFDrawTool

# specify if you want to run the script and ROOT in batch mode (this will not show any canvases):
#setBatchMode()

# Set the wanted input file and load all available histograms in this file in the memory:
setInput("plotsGenJetAnalysis.root")
getAllHistos()

# define nice legend names for the samples that you are plotting:
#setLegend("MinBias_TuneEE5C_13TeV-herwigpp","HERWIG")
setLegend("ReggeGribovPartonMC_13TeV-EPOS","EPOS")
setLegend("MinBias_TuneZ2star_13TeV-pythia6_MagnetOff","Pythia6 TuneZ2star (B=0T)")
setLegend("MinBias_TuneMonash13_13TeV-pythia8_MagnetOff","Pythia8 Monash13 (B=0T)")
setLegend("MinBias_TuneMBR_13TeV-pythia8_MagnetOff","Pythia8 MBR (B=0T)")
#setLegend("MinBias_TuneCUETP8M1_13TeV-pythia8","Pythia8 CUETP8S1")
setLegend("ReggeGribovPartonMC_13TeV-QGSJetII","QGSJetII")
#setLegend("data_MinBias_TuneCUETP8S1-HERAPDF_13TeV-pythia8","data (CUETP8S1)")


# this will plot ALL histograms found the in the file:
# GlobalPlotRatioToSample = "MinBias_TuneEE5C_13TeV-herwigpp"
# plotRatio()
draw()

# this will plot all histograms containing the string "RecoTrack" in their names normalised to their integral:
# turn on this function to plot with ratio to a data sample
#plotRatio(data="MinBias_TuneEE5C_13TeV-herwigpp")
#draw(["hdNdDeltaPtCenCasGenJet"],"int")

# this will plot a combination of histograms containing either of the two strings in their names:
#draw(["hdNdEak4GenJets","hdNdEak5CastorJets"],localSampleList=["ReggeGribovPartonMC_13TeV-EPOS"])

# by default all histograms are not normalised
# you can optionally normalise them to their integrals (int) or to their maxima (max):
#draw(["RecoTrack"],"max")

# you can also specify which samples you want to plot
# draw all GenTrack histograms normalised to their integral for only one MC sample:
#draw(["GenTrack"],"int",["MinBias_TuneMonash13_13TeV-pythia8"])

# add "CMS" or "CMS Preliminary" labels to all open canvases
printCMSPreliminary()

# add the centre-of-mass energy label to all open canvases
# by default this is 13 TeV
printCMEnergy()

# add the integrated luminosity to all open canvases
#printLumi("3 nb^{-1}")

# update all open canvases to display the changes
updateCanvas()

# after drawing one can save the plots as files
# by default the PDF format is chosen to save a plot
# by default they are saved in the current directory
# save all open canvases to pdf files:
#saveCanvas()

# save all canvases with the string "etaRecoTrack" in their names:
#saveCanvas("./",["etaRecoTrack"])
# to save in another directory, change the path of the first argument in the above command,
# the directory needs to be an existing one

# in addition, other file formats are supported:
#saveCanvas("./",["etaRecoTrack"],["pdf","eps","png","C"])
# saveCanvas("./",["hdNdEtaak4GenJets"],["png"])
# saveCanvas("./",["hdNdEtaak4CaloJets"],["png"])

# when you are done and you want to close the open canvases to plot other histograms
# delete all canvases from the memory (not needed when running script in batch mode):
#resetCanvas()
# you can off course also just click on a particular canvas to close it, the above function is just usefull when you have 10+ plots open or so

# when done with this file, you can reset the memory and go to another one:
# this is probably only useful when running a complicated script in batch mode
#resetHisto()
#setInput("../test/CSA14/plotsCSA14_UEAna.root")
#getAllHistos()
#draw(["RecoTrack"])
