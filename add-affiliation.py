#!/usr/bin/env python3

import os
import sys
import shutil
from xml.etree import ElementTree as ET


targetdir = os.path.realpath(sys.argv[1])
affiliation = sys.argv[2]
files = os.listdir(targetdir)

processeddir = targetdir + "_processed"
if os.path.exists(processeddir):
  shutil.rmtree(processeddir) 
os.mkdir(processeddir)

for file in files:
  if file.endswith('.xml'):
    try:
      mods = ET.parse(targetdir + "/" + file)
      namespaces = {'mods': 'http://www.loc.gov/mods/v3'}
      root = mods.getroot()
      for name in root.findall('mods:name', namespaces):
        print(name)


    except:
      print(file + " is not wellformed. Please fix.")
      sys.exit()
