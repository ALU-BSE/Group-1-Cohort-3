## Script to parse XML file and convert to JSON file

import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom 
from pprint import pprint

import xmltodict
import json

def generete_id(prefix, counter):
  return f'{prefix}_{counter:04d}'

def build_entities_from_xml_dict(data_dictionary):

  user = []
  transaction_category = []
  transaction = []
  system_log = []
  service_centre = []
  backup = []
  sms = []

  user_counter = 1
  transaction_category_counter = 1
  transaction_counter = 1
  system_log_counter = 1
  service_centre_counter = 1
  backup_counter = 1
  sms_counter = 1

  xml_users = data_dictionary.get('smses', {}).get('sms', [])

  for xml_user in xml_users:
    user_id = generete_id('US', user_counter)
    user.append({
      'id': user_id,
      'mobile_number': xml_user.get('phone_number')
    })
    user_counter += 1

    transaction_category_id = generete_id('TCAT', transaction_category_counter)
    transaction_category.append({
      'id': transaction_category_id,
      'user_id': user_id
    })
    transaction_category_counter += 1

    transaction_id = generete_id('TRNS', transaction_counter)
    transaction.append({
      'id': transaction_id,
      'type': '1',
      'date': xml_user.get('date'),
      'user_id': user_id,
      'transaction_category_id': transaction_category_id
    })
    transaction_counter += 1

    system_log_id = generete_id('SLOG', system_log_counter)
    system_log.append({
      'id': system_log_id,
      'event': '1',
      'date': xml_user.get('date'),
      'transaction_id': transaction_id
    })
    system_log_counter += 1

    service_centre_id = generete_id('SC', service_centre_counter)
    service_centre.append({
      'id': service_centre_id,
      'mobile_number': xml_user.get('service_centre'),
      'ISP_name': 'MTN'
    })
    service_centre_counter += 1

    backup_id = generete_id('BCK', backup_counter)
    backup.append({
      'id': backup_id,
      'date': xml_user.get('date'),
      'user_id': user_id
    })
    backup_counter += 1

    sms_id = generete_id('SMS', sms_counter)
    sms.append({
      'id': sms_id,
      'date': xml_user.get('date'),
      'body': xml_user.get('body'),
      'user_id': user_id,
      'sub_id': '6'
    })
    sms_counter += 1

  return {
    'user': user,
    'transaction_category': transaction_category,
    'transaction': transaction,
    'system_log': system_log,
    'service_centre': service_centre,
    'backup': backup,
    'sms': sms,
  }

def xml_to_json(input_file,output_file):

  with open(input_file) as xml_file:
    data_dictionary = xmltodict.parse(xml_file.read())

  pprint(data_dictionary)

  docs = minidom.parse(input_file) 

  print (docs.nodeName)
  print (docs.firstChild.tagName)

  return data_dictionary

if __name__ == '__main__':
  input_file = 'database/formatted_sms_v2.xml'
  output_file = 'database/xml_to_json.json'

  try:
    data = xml_to_json(input_file,output_file)
    entities = build_entities_from_xml_dict(data)
    with open(output_file, 'w', encoding='utf-8') as out_f:
      json.dump(entities, out_f, indent=4, ensure_ascii=False)

    pprint(entities)
  except FileNotFoundError:
    print(f"Error, File does not exist/cannot be found '{input_file}'")
  except Exception as e:
    print(f'Error : {e}')
