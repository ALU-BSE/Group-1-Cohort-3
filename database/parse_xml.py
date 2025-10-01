## Script to parse XML file and convert to JSON file

import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom 
from pprint import pprint

import xmltodict
import json

def xml_to_json(input_file,output_file):

  with open(input_file) as xml_file:
    data_dictionary = xmltodict.parse(xml_file.read())

  json_data = json.dumps(data_dictionary, indent= 4)

  with open(output_file, "w") as json_file:
    json_file.write(json_data)
    pprint(json_data)

  docs = minidom.parse(input_file) 

  print (docs.nodeName)
  print (docs.firstChild.tagName)

if __name__ == '__main__':
  input_file = 'database/formatted_sms_v2.xml'
  output_file = 'database/xml_to_json.json'

  try:
    xml_to_json(input_file,output_file)
  except FileNotFoundError:
    print(f"Error, File does not exist/cannot be found '{input_file}'")
  except Exception as e:
    print(f'Error : {e}')
