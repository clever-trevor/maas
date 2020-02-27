from urllib.request import Request,urlopen
import json

def show_indices(es):
  try :
    url = es['url'] + "/_cat/indices"
    user = es['user']
    pwd = es['pass']
    req = urlopen(Request(url))
  except :
    req = ""
  return req

def create_index(es,index,settings) :
  try :
    url = es['url'] + "/" + index
    user = es['user']
    pwd = es['pass']
    headers = { "Content-Type":"application/json" }
    settings = json.dumps(settings).encode("utf-8")
    req = json.load(urlopen(Request(url,data=settings,method="PUT",headers=headers)))
  except :
    req = {}
  return req

def delete_index(es,index) :
  try :
    url = es['url'] + "/" + index
    user = es['user']
    pwd = es['pass']
    req = json.load(urlopen(Request(url,method='DELETE')))
  except :
    req = {}
  return req
  
def post_document(es,index,type,id,doc) :
  try:
    url = es['url'] + "/" + index + "/" + type
    if id != "" : 
      url += "/" + id
    doc = str(json.dumps(doc)).encode("utf-8")
    headers = { "Content-Type":"application/json" }
    req = json.load(urlopen(Request(url,data=doc,headers=headers)))
  except :
    req = {}
  return req

def get_document_by_id(es,index,type,id) :
  try :
    url = es['url'] + "/" + index + "/" + type + "/" + id 
    headers = { "Content-Type":"application/json" }
    req = json.load(urlopen(Request(url,headers=headers)))
  except :
    req = {}
  return req

def run_search_uri(es,index,query) :
  try :
    url = es['url'] + "/" + index + "/_search?" + query
    headers = { "Content-Type":"application/json" }
    req = json.load(urlopen(Request(url,headers=headers)))
  except :
    req = {}
  return req

def run_search(es,index,query) :
  try :
    url = es['url'] + "/" + index + "/" + type + "/" + id 
    headers = { "Content-Type":"application/json" }
    req = json.load(urlopen(Request(url,headers=headers)))
  except :
    req = {} 
  return req

def es_function(es,index,params,doc,method) :
  try :
    url = es['url'] + "/" + index
    if params != "" : 
      url += "/" + params
    headers = { "Content-Type":"application/json" }
    doc = str(json.dumps(doc)).encode("utf-8")
    req = json.load(urlopen(Request(url,headers=headers,method=method,data=doc)))
  except :
    req = {}
  return req
