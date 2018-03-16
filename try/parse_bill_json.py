# encoding:utf-8


sss= {
  "Basic Ads - Phone-Banner 1": "test_bill03iOS-Phone-Banner-v1080_ID1", 
  "Basic Ads - Phone-Banner 2": "test_bill03iOS-Phone-Banner-v1080_ID2", 
  "Basic Ads - Phone-Banner 3": "test_bill03iOS-Phone-Banner-v1080_ID3", 
  "Basic Ads - Phone-Banner 4": "test_bill03iOS-Phone-Banner-v1080_ID4", 
  "Basic Ads - Phone-Interstitial 1": "test_bill03iOS-Phone-Interstitial-v1080_ID1", 
  "Basic Ads - Phone-Interstitial 3": "test_bill03iOS-Phone-Interstitial-v1080_ID3", 
  "Basic Ads - Phone-Reward 1": "test_bill03iOS-Phone-Reward-v1080_ID1", 
  "Basic Ads - Tablet-Banner 1": "test_bill03iOS-Tablet-Banner-v1080_ID1", 
  "Basic Ads - Tablet-Banner 2": "test_bill03iOS-Tablet-Banner-v1080_ID2", 
  "Basic Ads - Tablet-Banner 3": "test_bill03iOS-Tablet-Banner-v1080_ID3", 
  "Basic Ads - Tablet-Banner 4": "test_bill03iOS-Tablet-Banner-v1080_ID4", 
  "Basic Ads - Tablet-Interstitial 1": "test_bill03iOS-Tablet-Interstitial-v1080_ID1", 
  "Basic Ads - Tablet-Interstitial 3": "test_bill03iOS-Tablet-Interstitial-v1080_ID3", 
  "Basic Ads - Tablet-Reward 1": "test_bill03iOS-Tablet-Reward-v1080_ID1"
}

import re

def parse_json(json_dc): 
    out_dc={}
    for k,v in json_dc.items():
        mt = re.search('- (\w+)-(\w+)',k)
        if mt:
            key='_'.join(mt.groups()).lower()
            out_dc[key] = out_dc.get(key,[])
            out_dc[key].append([k,v])
    
    return out_dc


print( parse_json(sss))