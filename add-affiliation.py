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
      ET.register_namespace('dcterms', "http://purl.org/dc/terms/")
      ET.register_namespace('etd', "http://www.ndltd.org/standards/metadata/etdms/1.0/")
      ET.register_namespace('flvc', "info:flvc/manifest/v1")
      ET.register_namespace('xlink', "http://www.w3.org/1999/xlink")
      root = mods.getroot()

      # Find name element of the author
      for name in root.findall('mods:name', namespaces):
        for role in name.findall('mods:role', namespaces):
          for roleTerm in role.findall('mods:roleTerm', namespaces):
            if roleTerm.attrib['type'] == 'text' and roleTerm.text == 'author' or roleTerm.text == 'creator':
              affiliation_node = ET.Element("{http://www.loc.gov/mods/v3}affiliation")
              affiliation_node.text = affiliation
              name.append(affiliation_node)
              
      # Find name element usage=primary for the older records
      for name in root.findall('mods:name', namespaces):
        usage = name.get('usage')
        if usage == 'primary':
          affiliation_node = ET.Element("{http://www.loc.gov/mods/v3}affiliation")
          affiliation_node.text = affiliation
          name.append(affiliation_node)

      mods.write(processeddir + "/" + file, encoding='utf-8', xml_declaration=True)
      print(file + " is Done!")
  
    except:
      print(file + " is not wellformed. Please fix.")
      sys.exit()
