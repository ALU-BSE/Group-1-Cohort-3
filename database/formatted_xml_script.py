## Script to format XML file into a more readable structure
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom 
from pprint import pprint


def format_xml(input_file, output_file):
  tree = ET.parse(input_file)
  root = tree.getroot()
  
  new_root = ET.Element("smses")
  for attribute, value in root.attrib.items():
    new_root.set(attribute, value)
  
  for sms in root.findall('sms'):
    new_sms = ET.SubElement(new_root, 'sms')

    for attribute, value in sms.attrib.items():
      child = ET.SubElement(new_sms, attribute)
      child.text = value
  
  rough_string = ET.tostring(new_root, encoding='utf-8')
  reparsed = minidom.parseString(rough_string)
  pretty_xml = reparsed.toprettyxml(indent="  ", encoding='utf-8')

  with open(output_file, "wb") as f:
    f.write(pretty_xml)
  
  print(f'Successfully formatted XML saved to: {output_file}')
  print(f"Processed {len(root.findall('sms'))} SMS messages")


if __name__ == '__main__':
  input_file = 'database/modified_sms_v2.xml'
  output_file = 'database/formatted_sms_v2.xml'

  try:
    format_xml(input_file,output_file)
  except FileNotFoundError:
    print(f"Error, File does not exist/cannot be found '{input_file}'")
  except Exception as e:
    print(f'Error : {e}')

    

