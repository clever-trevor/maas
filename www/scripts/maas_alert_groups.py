#!/usr/bin/python3

# This routing controls viewing and running Groups of tests

# There are two modes of operation :
#  * View alert configs which contain a given tag
#  * Execute all tests for a given tag
from urllib.request import Request,urlopen
import maas_utils
import datetime
import json
import maas_conf

# Set some variables from this
api_url = maas_conf.conf['api']['url']

# Routine to view alerts groups and/or contents
def alert_groups(args):

  # Build HTML header
  content = "<html><head><link rel='stylesheet' type='text/css' href='/static/dark.css'></head>"
  content += "<h1><A style='text-decoration:none' HREF='/'>Group Alert Management</a></h1>"
  content += "<hr>"

  # Set the default mode if not provided
  mode = "view"
  if 'mode' in args :
    mode = args['mode']

  # If entity was passed in then additionally filter on this 
  if 'entity' in args :
    entity_filter = args['entity']
  else:
    entity_filter = ""

  alert_tag_in = ""
  if 'alert_tag' in args :
    alert_tag_in = args['alert_tag']
  else:

    # No alert_tag was supplied so get the complete set and show
    # them on the screen
    content += "<H3>You need to pass in a parameter called <b>alert_tag</b></H3>"
    content += "<H4>Available alert_tags below</H4>"
    content += "<TABLE class='blueTable'><TR><TH>Tag</TH></TR>"
   
    # Retrieve all tags from alert configs but only show each once 
    try:
      req = Request(api_url + "/config/alert/tags",method='GET')
      tags = json.loads(json.load(urlopen(req)))
      tags = sorted(tags,key=lambda i: i['tag'])
      tagfound = {}
      for alert_tag in tags :
        myalert_tags = alert_tag['tag'].split()
        for myalert_tag in myalert_tags:
          if myalert_tag not in tagfound :
            content += "<TR><TD><A HREF='/alert-groups?alert_tag=%s'>%s</A></TD></TR>" % ( myalert_tag,myalert_tag)
          tagfound[myalert_tag] = True
      content += "</TABLE>"
      return content
    except:
      content += "Error connecting to /config/alert/tags API"
      return content

  # An alert_tag was provided so fetch the results from Elastic
  # Build Elastic query to return all records which match the supplied alert_tag
  try:
    # Call the API to get all alert configs which contain the tag
    req = Request(api_url + "/config/alert?alert_tag=" + alert_tag_in,method='GET')
    tags = json.loads(json.load(urlopen(req)))
    records = sorted(tags,key=lambda i: i['entity'] )
  except:
    content += "Unable to connect to /config/alert API"
    return content

  
  # Test mode means to execute all alert tests which match the config
  if mode == "test" :

    content += "<H2>Running tests in group <i>%s</i><h2>" % (alert_tag_in)

    # Build a table of each test executed to show at the end
    monitors = "<TABLE class='blueTable'><TR><TH>Tag(s)<TH>Entity<TH>Metric Class<TH>Metric Object<TH>Metric Instance<TH>Metric Name<TH>Operator<TH>Threshold<TH>Actual<TH>Status<TH>Sample Time</TR>"

    status = {}  # Dictionary used to store the overall monitors and status
    for r in records :
      entity = r['entity']

      # IF we supplied an entity filter, then only evaluate that host
      if entity_filter != "" and entity != entity_filter :
        continue

      metric_class = r['metric_class']
      metric_object = r['metric_object']
      metric_instance = r['metric_instance']
      metric_name = r['metric_name']
      alert_operator = r['alert_operator']
      alert_threshold = r['alert_threshold']
      support_team = r['support_team']
      alert_tag = r['alert_tag']
 
      # Run an Influx query for each metric
      params = "entity=%s&metric_class=%s&metric_object=%s&metric_instance=%s&metric_name=%s" % ( entity,metric_class,metric_object,metric_instance,metric_name)

      req = Request(api_url + "/metric/last?" + params,method='GET')
      value, metric_timestamp = str(urlopen(req).read(),'utf-8').split(' ')
      try:
        value = float(value)
      except:
        value = 0

      # Test the result
      result = maas_utils.evaluate_metric(value,alert_operator,alert_threshold)
      # Reformat the time stamp field
      metric_timestamp = metric_timestamp.replace("T"," ").replace("Z"," ")

      # If first record, then create a dictionary to show overall summary later on
      if alert_tag_in not in status :
        status[alert_tag_in] = {}
        status[alert_tag_in]['outcome'] = "PASS"
        status[alert_tag_in]['tests'] = 0
        status[alert_tag_in]['failed'] = 0
        status[alert_tag_in]['passed'] = 0

      # Add to number of tests found
      status[alert_tag_in]['tests'] += 1

      # Result of "true" means the condition was true.  i.e. failed
      if result is True or value == -1 :
        status[alert_tag_in]['outcome'] = "FAIL"
        status[alert_tag_in]['failed'] += 1
        result = "<FONT Color=Red>FAIL</font>"
      else :
        status[alert_tag_in]['passed'] += 1
        result = "<FONT Color=Green>PASS</font>"

      # Add record to the monitors table
      value = "{:.2f}".format(value)
      monitors += "<TR><TD>%s<TD>%s<TD>%s<TD>%s<TD>%s<TD>%s<TD>%s<TD>%s<TD>%s<TD>%s<TD>%s</TR>" % (alert_tag,entity,metric_class,metric_object,metric_instance,metric_name,alert_operator,alert_threshold,str(value),str(result),metric_timestamp)
  
    monitors += "</TABLE>"
 
    # Print one line summary of all tests executed
    content += "<TABLE class='blueTable'><TR><TH>Tag<TH>Total Tests<TH>Failed<TH>Passed<TH>Outcome</TR>"
    for alert_tag in status:
      outcome = status[alert_tag]['outcome']
      if outcome == "FAIL" :
        outcome = "<FONT Color=Red>FAIL</font>"
      else :
        outcome = "<FONT Color=Green>PASS</font>"
      tests = status[alert_tag]['tests']
      failed = status[alert_tag]['failed']
      passed = status[alert_tag]['passed']
      content += "<TR><TD>%s<TD>%s<TD>%s<TD>%s<TD>%s</TR>" % (alert_tag,tests,failed,passed,outcome)
  
    content += "</TABLE>"

    # Now print the detailed table 
    content += "<h2>Breakdown</h2>" + monitors


  # View Mode
  else :
    content += "<h2>Viewing matches for alert_tag <i>%s</i></h2>" % ( alert_tag_in )
    content += "<TABLE class='blueTable'><TR><TH>Tag(s)<TH>Entity<TH>Monitor Class<TH>Metric Object<TH>Metric Instance<TH>Metric Name<TH>Operator<TH>Threshold</TR>"

    # Loop through each record that was found
    for r in records :
      entity = r['entity']

      # IF we supplied an entity filter, then only evaluate that host
      if entity_filter != "" and entity != entity_filter :
        continue

      metric_class = r['metric_class']
      metric_object = r['metric_object']
      metric_instance = r['metric_instance']
      metric_name = r['metric_name']
      alert_operator = r['alert_operator']
      alert_threshold = r['alert_threshold']
      support_team = r['support_team']
      alert_tag= r['alert_tag']
      # And print it
      content += "<TR><TD>%s<TD>%s<TD>%s<TD>%s<TD>%s<TD>%s<TD>%s<TD>%s</TR>" % (alert_tag,entity,metric_class,metric_object,metric_instance,metric_name,alert_operator,alert_threshold)

  content += "</html>"

  return content
