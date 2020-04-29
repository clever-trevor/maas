import urllib.parse
from urllib.request import Request,urlopen
import json
import base64

def add_creds(es):
  creds = es['user'] + ":" + es['pass']
  b64 = str(base64.b64encode(creds.encode("utf-8")),"utf-8")
  return b64

def show_indices(es):
  try :
    url = es['url'] + "/_cat/indices"
    req = Request(url)
    req.add_header("Authorization","Basic %s" % add_creds(es))
    resp = urlopen(req)
  except :
    resp = ""
  return resp

def create_index(es,index,settings) :
  try :
    url = es['url'] + "/" + index
    headers = { "Content-Type":"application/json" }
    settings = json.dumps(settings).encode("utf-8")
    req = Request(url,data=settings,method="PUT",headers=headers)
    req.add_header("Authorization","Basic %s" % add_creds(es))
    resp = json.load(urlopen(req))
  except :
    resp = {}
  return resp

def delete_index(es,index) :
  try :
    url = es['url'] + "/" + index
    req = Request(url,method='DELETE')
    req.add_header("Authorization","Basic %s" % add_creds(es))
    resp = json.load(urlopen(req))
  except :
    resp = {}
  return resp
  
def post_document(es,index,type,id,doc) :
  try:
    url = es['url'] + "/" + index + "/" + type
    if id != "" : 
      url += "/" + id
    doc = str(json.dumps(doc)).encode("utf-8")
    headers = { "Content-Type":"application/json" }
    req = Request(url,data=doc,headers=headers)
    req.add_header("Authorization","Basic %s" % add_creds(es))
    resp = json.load(urlopen(req))
  except :
    resp = {}
  return resp

def get_document_by_id(es,index,type,id) :
  try :
    url = es['url'] + "/" + index + "/" + type + "/" + id 
    headers = { "Content-Type":"application/json" }
    req = Request(url,headers=headers)
    req.add_header("Authorization","Basic %s" % add_creds(es))
    resp = json.load(urlopen(req))
  except :
    resp = {}
  return resp

def delete_document_by_id(es,index,type,id) :
  try :
    url = es['url'] + "/" + index + "/" + type + "/" + id 
    headers = { "Content-Type":"application/json" }
    req = Request(url,method='DELETE',headers=headers)
    req.add_header("Authorization","Basic %s" % add_creds(es))
    resp = json.load(urlopen(req))
  except :
    resp = {}
  return resp

def run_search_uri(es,index,query,params) :
  try :
    query = urllib.parse.quote(query)
    url = es['url'] + "/" + index + "/_search?q=" + query + params
    req = Request(url)
    req.add_header("Authorization","Basic %s" % add_creds(es))
    req.add_header("Content-Type","application/json")
    resp = json.load(urlopen(req))
  except :
    resp = {}
  return resp

def run_search(es,index,query):
  try :
    url = es['url'] + "/" + index  + "/_search"
    query = str(json.dumps(query)).encode("utf-8")
    headers = { "Content-Type":"application/json" }
    req = Request(url,method="GET",data=query,headers=headers)
    req.add_header("Authorization","Basic %s" % add_creds(es))
    resp = json.load(urlopen(req))
  except :
    resp = {} 
  return resp

def es_function(es,index,params,doc,method) :
  try :
    url = es['url'] + "/" + index
    if params != "" : 
      url += "/" + params
    headers = { "Content-Type":"application/json" }
    doc = str(json.dumps(doc)).encode("utf-8")
    req = Request(url,headers=headers,method=method,data=doc)
    req.add_header("Authorization","Basic %s" % add_creds(es))
    resp = json.load(urlopen(req))
  except :
    resp = {}
  return resp
