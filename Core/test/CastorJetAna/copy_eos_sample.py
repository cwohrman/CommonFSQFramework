#! /usr/bin/env python
#
import os
import subprocess
import shlex

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", "--source", dest="source_dir",
                  help="SOURCE directory of skimmed trees", metavar="SOURCE")
parser.add_option("-t", "--target", dest="target_dir",
                  help="TARGET directory to copy skimmed trees", metavar="TARGET")
parser.add_option("-a", "--appendix", dest="file_appendix",
                  help="APPENDIX add to copied trees to prevent overwriting", metavar="APPENDIX")
parser.add_option("-v", action="store_true", dest="verbose",
                  help="just show copy command NOT execute it")

eos_cmd = "/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select"
eos_dir = "root://eoscms.cern.ch/"
source_dir = eos_dir + "/eos/cms/store/group/phys_heavyions/cwohrman/CFF/CastorJets/L1MinimumBiasHF4/Long_RunIILowPU_0T_20150820_data_L1MinimumBiasHF4_Run2015A/150825_141448/0000/"
target_dir = eos_dir + "/eos/cms/store/group/phys_heavyions/cwohrman/CFF/CastorJets/SumTreesDir_L1MinimumBiasHF/"
file_appendix = "_HFX"

(options, args) = parser.parse_args()

if not options.source_dir:
  parser.error("incorrect number of arguments")
else:
  source_dir = options.source_dir

if options.target_dir: target_dir = options.target_dir
if options.file_appendix: file_appendix = "_" + options.file_appendix

listcommand = eos_cmd + " ls " + source_dir
# list files with inname
p = subprocess.Popen(listcommand,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
# readout standard output
stmp = p.stdout.read()
flist = sorted(shlex.split(stmp),key=str.lower)

for name in flist:
  if "trees" not in name: continue
  # print name[:name.rfind('.')]

  target_name = name[:name.rfind('.')] + file_appendix + '.root'
  # print target_name

  copycommand = eos_cmd + " cp " + source_dir + name + " " + target_dir + target_name
  if options.verbose:
    print copycommand
  else:
    os.system(copycommand)
