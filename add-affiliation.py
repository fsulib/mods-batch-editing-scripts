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
      ET.register_namespace('', "http://www.loc.gov/mods/v3")
      ET.register_namespace('mods', "http://www.loc.gov/mods/v3")
      ET.register_namespace('etd', "http://www.ndltd.org/standards/metadata/etdms/1.0/")
      ET.register_namespace('flvc', "info:flvc/manifest/v1")
      root = mods.getroot()

      # Find name element of the author
      for name in root.findall('mods:name', namespaces):
        for role in name.findall('mods:role', namespaces):
          for roleTerm in role.findall('mods:roleTerm', namespaces):
            if roleTerm.attrib['type'] == 'text' and roleTerm.text == 'author':
              affiliation_node = ET.Element("{http://www.loc.gov/mods/v3}affiliation")
              affiliation_node.text = affiliation
              name.append(affiliation_node)

      mods.write(processeddir + "/" + file)
    
    except:
      print(file + " is not wellformed. Please fix.")
      sys.exit()
