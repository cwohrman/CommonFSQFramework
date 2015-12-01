#! /usr/bin/env python
#
import os
import subprocess
import shlex

import CommonFSQFramework.Core.Util

sampleList=CommonFSQFramework.Core.Util.getAnaDefinition("sam")

from optparse import OptionParser

parser = OptionParser()
# parser.add_option("-s", "--source", dest="source_dir",
#                   help="SOURCE directory of skimmed trees", metavar="SOURCE")
parser.add_option("-s", "--sample", dest="sample",
                  help="SAMPLE in the sample list to copy", metavar="SAMPLE" )
parser.add_option("-t", "--target", dest="target_dir",
                  help="TARGET directory to copy skimmed trees", metavar="TARGET")
parser.add_option("-a", "--appendix", dest="file_appendix",
                  help="APPENDIX add to copied trees to prevent overwriting", metavar="APPENDIX")
parser.add_option("-v", action="store_true", dest="verbose",
                  help="just show copy command NOT execute it")


cpcmd = 'lcg-cp '
listcmd = 'lcg-ls '
eos_cmd = "/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select"
eos_dir = "srm://srm-eoscms.cern.ch:8443/srm/v2/server?SFN="


(options, args) = parser.parse_args()

if not options.sample:
  parser.error("NO sample name was given")
else:
  source_dir = sampleList[options.sample]['pathSE']  

target_dir = '/tmp/cwohrman/'
if options.target_dir: target_dir = eos_dir + options.target_dir

file_appendix = "_HFX"
if options.file_appendix: file_appendix = "_" + options.file_appendix

listcommand = listcmd + source_dir
# print listcommand
# list files with inname
p = subprocess.Popen(listcommand,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
# readout standard output
stmp = p.stdout.read()
flist = sorted(shlex.split(stmp),key=str.lower)
# print flist

for name in flist:
  if "trees" not in name: continue
  # print name[name.rfind('/')+1:name.rfind('.')]

  target_name = name[name.rfind('/')+1:name.rfind('.')] + file_appendix + '.root'
  # print target_name

  copycommand = cpcmd + source_dir + name[name.rfind('/')+1:] + " " + target_dir + target_name

  if options.verbose:
    print copycommand
  else:
    print copycommand
    os.system(copycommand)
