import uuid
import random
import string
import requests
import json
from datetime import date
from datetime import timedelta
from random import uniform
 
query_metadata_pattern = """
{{
    "name": "{}"
}}
"""
 
def create_es_mapping(url, index, type):
    mappingurl = '{0}/{1}'.format(url, index)
    mappingspayload = '{' \
    '  "mappings": {' \
    '    "' + type + '": {' \
    '      "properties": {' \
    '        "geometry": {' \
    '            "type" : "geo_shape"' \
    '        },' \
    '        "geometry_wkt": {' \
    '          "type": "text",' \
    '          "fields": {' \
    '            "keyword": {' \
    '              "type": "keyword",' \
    '              "ignore_above": 256' \
    '            }' \
    '          }' \
    '        },' \
    '        "properties": {' \
    '          "properties": {' \
    '            "Current Speed": {' \
    '              "type": "double",' \
    '              "index": false' \
    '            },' \
    '            "Description": {' \
    '              "type": "keyword"' \
    '            },' \
    '            "Latitude": {' \
    '              "type": "double"' \
    '            },' \
    '            "Longitude": {' \
    '              "type": "double"' \
    '            }' \
    '          }' \
    '        },' \
    '        "type": {' \
    '          "type": "text",' \
    '          "fields": {' \
    '            "keyword": {' \
    '              "type": "keyword",' \
    '              "ignore_above": 256' \
    '            }' \
    '          }' \
    '        },' \
    '        "uuid": {' \
    '          "type": "text",' \
    '          "fields": {' \
    '            "keyword": {' \
    '              "type": "keyword",' \
    '              "ignore_above": 256' \
    '            }' \
    '          }' \
    '        }' \
    '      }' \
    '    }' \
    '  }' \
    '}'
 
    headers = {'Content-type': 'application/json'}
     
    r = requests.put(mappingurl, data=mappingspayload, headers=headers)
     
    if r.status_code == requests.codes.ok:
        mapping = r.json()
 
    else:
        print('Error creating mapping:')
    #    print(r.text)
    #    raise Exception(r.text)
 
def create_feature():
    xPos = round(uniform(-180,180)*1000)/1000
    yPos = round(uniform(-90,90)*1000)/1000
    payload = '{' \
    '   "uuid" : "' + str(uuid.uuid4()) + '",' \
    '   "geometry" : {' \
    '       "coordinates" : [' \
    '           ' + str(xPos) + ',' \
    '           ' + str(yPos) + '' \
    '       ],' \
    '       "type" : "Point"' \
    '   },' \
    '   "type": "Feature",' \
    '   "properties": {' \
    '       "Description" : "Random (' + str(xPos) + ' ' + str(yPos) + ')",' \
    '       "Current Speed" : ' + str(yPos) + ',' \
    '       "Latitude" : ' + str(yPos) + ',' \
    '       "Longitude" : ' + str(xPos) + '' \
    '   },' \
    '   "geometry_wkt" : "POINT (' + str(xPos) + ' ' + str(yPos) + ')"' \
    '}'
	
    #print(payload)
    return payload
	
def create_bulk(featuresnum, url, index, type):
 
    bulkurl = '{0}/{1}/_bulk'.format(url, index)
     
    totalbulkload = ''
    for i in range(featuresnum):
        bulkload = '{' \
        '   "index": {' \
        '       "_index": "' + index + '",' \
        '       "_type": "' + type + '"' \
        '   }' \
        '}\n'
        features = create_feature() + '\n'
        totalbulkload = totalbulkload + bulkload + features
         
    headers = {'Content-type': 'application/json'}
    r = requests.post(bulkurl, data=totalbulkload, headers=headers)
 
    if r.status_code == requests.codes.ok:
    #    results = r.json()
    #    prettyJson = json.dumps(results, sort_keys=True, indent=4, separators=(',', ': '))
    #    print(prettyJson)
        print('insert ' + str(featuresnum) + ' features into index ' + index)
    else:
        # created go here
        print(r.text)
         
def create_alias(url, alias, index):
 
    aliasurl = '{0}/_aliases'.format(url)
    aliaspayload = '{' \
        '   "actions": [' \
        '       {'\
        '           "add": {'\
        '               "index": "' + index + '",' \
        '               "alias": "' + alias + '"' \
        '           }' \
        '       }' \
        '   ]' \
        '}'   
     
    headers = {'Content-type': 'application/json'}
    r = requests.post(aliasurl, data=aliaspayload, headers=headers)
     
    if r.status_code == requests.codes.ok:
        print('create alias ' + alias + ' for index ' + index)
    else:
        print(r.text)
         
def delete_es_alias(url, alias):
    alias = alias + '*'
    delete_alias_url = '{0}/{1}'.format(url, alias)
  
    r = requests.delete(delete_alias_url)
  
    if r.status_code != requests.codes.ok:
        print('Error deleting alias:')
        print(r.text)
        #raise Exception(r.text)
         
def query_all_es_documents(url, index):
    queryurl = '{0}/{1}/_search?pretty=true'.format(url, index)
  
    query = """
    {
        "query" : {
            "match_all" : {}
        }
    }
    """
  
    headers = {'Content-type': 'application/json'}
    r = requests.post(queryurl, data=query, headers=headers)
  
    if r.status_code == requests.codes.ok:
        documents = r.json()
        docjson = json.dumps(documents, sort_keys=True, indent=4, separators=(',', ': '))
        docdata = json.loads(docjson)
        print("The number of records in " + index + " is " + str(docdata['hits']['total']))
    else:
        print('Error querying documents:')
        print(r.text)
        #raise Exception(r.text)     
     
def main():
    #adjust url accordingly
    es_url = 'http://localhost:9200'
    es_host = 'localhost'
    es_cluster = 'docker-cluster'
     
    num_of_ds = 1
    date_of_index = 55
    num_features = 20000
     
    for j in range(num_of_ds):
     
        alias = 'tanggeoshape'
        es_type = alias + '_type'
        
        create_es_mapping(es_url, alias, es_type)
		
        for i in range(date_of_index):
            docdate = date.today() - timedelta(days=i)
            docdatestring = docdate.strftime("%Y.%m.%d")
            es_index = alias
            create_bulk(num_features, es_url, es_index, es_type)
            query_all_es_documents(es_url, alias)
            #create_alias(es_url, alias, es_index)
     
main()