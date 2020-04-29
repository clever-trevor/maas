
# This routing controls viewing and setting of alerting
from urllib.request import Request,urlopen
import json
import maas_conf

api_url = maas_conf.conf['api']['url']
# Routine to print a Select block with a preselected option if a match found
def print_select(id,name,options,match) :

  content = str(type(options))
  content += "<select id='%s' name='%s'>" % (id,name)
  for option in options.split(",") :
    content += "<option value='%s'" % ( option )
    if option == match :
      content += " selected "
    content += ">%s</option>" % (option)
  return content


def alert(args,form):
  content = "<html><head><link rel='stylesheet' type='text/css' href='/static/dark.css'></head>"
  content += "<h1><A style='text-decoration:none' HREF='/'>Monitoring Alert Management</a></h1>"
  content += "<hr>"

  # Pull in URL parameters
  try:
    mode = args['mode']
  except:
    mode = "view"

  ########### EDIT
  if mode == "edit":
    # We have passed in the contents and entity so we will just set them 
    # Note : "edit=true" means don't write the detail but pre-populate form (next section)
    if 'entity' in form and not 'edit' in form :
      entity = form['entity']
      metric_class = form['metric_class']
      metric_object = form['metric_object']
      metric_instance = form['metric_instance']
      metric_name = form['metric_name']
      alert_operator = form['alert_operator']
      alert_threshold = form['alert_threshold']
      support_team = form['support_team']
      try:
        alert_tag = form['alert_tag']
      except:
        alert_tag = ""
      if entity == "" or metric_class == "" or metric_object == "" or metric_instance == "" or metric_name == "" or alert_operator == "" or alert_threshold == "" or support_team == "" :
        content += "<h3>One or more parameters were missing - please press back on browser to correct"
      else :

        doc = { "entity":entity, "metric_class":metric_class, "metric_object":metric_object, "metric_instance":metric_instance, "metric_name":metric_name, "alert_operator":alert_operator, "alert_threshold":alert_threshold, "support_team":support_team, "alert_tag":alert_tag }
        data = str(json.dumps(doc)).encode("utf-8")

        try : 
          req = Request(api_url + "/config/alert",data=data)
          req.add_header('Content-Type','application/json')
          resp = str(urlopen(req).read(),'utf-8')
          if resp == 'created' or resp == 'updated' :
            content += "<h3><font color='Green'>Alert was %s in Database</font></h3>" % (resp)
            content += "<h4><A HREF='/alert?mode=view'>View all Alert Configuration</A></h4>"
          else :
            content += "<h3><font color='Red'>** Alert Could not be written to Database (Result = %s) **</font></h3>" % (resp)
        except:
          content += "<h3>Bad response from /config/alert API"
     
    # Either some detail was missing, or we want to go into form "edit" mode
    else :
      # See if we can get some details from the URL params
      if 'entity' in args : 
        entity = args['entity']
      else :
        entity = ""
      if 'metric_class' in args : 
        metric_class = args['metric_class']
      else :
        metric_class = ""
      if 'metric_object' in args : 
        metric_object = args['metric_object']
      else :
        metric_object = ""
      if 'metric_instance' in args : 
        metric_instance = args['metric_instance']
      else :
        metric_instance = ""
      if 'metric_name' in args : 
        metric_name = args['metric_name']
      else :
        metric_name = ""
      if 'alert_operator' in args : 
        alert_operator = args['alert_operator']
      else :
        alert_operator = ""
      if 'alert_threshold' in args : 
        alert_threshold = args['alert_threshold']
      else :
        alert_threshold = ""
      if 'support_team' in args : 
        support_team = args['support_team']
      else :
        support_team = ""
      if 'alert_tag' in args : 
        alert_tag = args['alert_tag']
      else :
        alert_tag = ""

      # Now lets build the form, populating values if we have them
      content += """
<html>
<h2>Configure metric collection for an entity </h2>
<h4>Set the condition so that it will evaluate to true when an alert should be generated</h4>
<FORM ACTION="/alert?mode=edit" METHOD="POST">
<TABLE>
 <TR>
  <TD>Hostname</TD>
  <TD>
    """
      # Build list of entities based on entitys that are currently configured
      req = Request(api_url + "/entity",method='GET')
      entities = json.loads(json.load(urlopen(req)))
      entities = sorted(entities,key=lambda i: i['entity']) # Sort it
      entity_list = ""
      for e in entities:
        entity_list += e['entity'] + ","
      content += print_select("entity","entity",entity_list[:-1],entity)
      content += """

  </TD>
 </TR>
 <TR>
  <TD>Metric Class</TD>
  <TD>
  """
      content += print_select("metric_class","metric_class","cpu,disk,procstat,procstat_lookup,http",metric_class)
      content += """
  </TD>
 </TR>
 <TR>
  <TD>Metric Object</TD>
  <TD>
  """
      content += "<input name='metric_object' id='metric_object' value='" + metric_object + "'>"
      content += """
    </input>
  </TD>
 </TR>
 <TR>
  <TD>Metric Instance</TD>
  <TD>
  """
      content += "<input name='metric_instance' id='metric_instance' value='" + metric_instance + "'>"
      content += """
    </input>
  </TD>
 </TR>
 <TR>
  <TD>Metric Name</TD>
  <TD>
  """
      content += "<input name='metric_name' id='metric_name' value='" + metric_name + "'>"
      content += """
    </input>
  </TD>
 </TR>
 <TR>
  <TD>Alert Operator</TD>
  <TD>
  """
      content += print_select("alert_operator","alert_operator","<,<=,>,<=,=",alert_operator)
      content += """
  </TD>
 </TR>
 <TR>
  <TD>Alert Threshold</TD>
  <TD>
  """
      content += "<input name='alert_threshold' id='alert_threshold' value='" + alert_threshold+ "'>"
      content += """
    </input>
  </TD>
 </TR>
 <TR>
  <TD>Support Queue</TD>
  <TD>
  """
      content += "<input name='support_team' id='support_team' value='" + support_team + "'>"
      content += """
    </input>
  </TD>
 </TR>
 <TR>
  <TD>Tag (Optional)</TD>
  <TD>
  """
      content += "<input name='alert_tag' id='alert_tag' value='" + alert_tag + "'>"
      content += """
    </input>
  </TD>
 </TR>
 <TR>
  <TD COLSPAN=2 ALIGN=CENTER>
   <input class="form-submit-button" type="submit"></input>
  </TD>
 </TR>
  
</TABLE>
</FORM>

<B>Example Metrics</B><BR>
<TABLE border=1><TR><TH>Metric Class<TH>Metric Object<TH>Metric Instance<TH>Metric Name</TR>
<TR><TD>cpu<TD>cpu<TD>cpu-total<TD>usage_idle<BR>usage_system<BR>usage_user</TR>
<TR><TD>disk<TD>path<TD>/opt<BR>C:<TD>free<BR>inodes_free<BR>used<BR>used_percent</TR>
<TR><TD>procstat<TD>exe<TD>sshd<BR>syslogd<TD>cpu_time_idle<BR>cpu_time_user<BR>cpu_time_system<BR>memory_usage<BR>num_threads</TR>
<TR><TD>procstat_lookup<TD>exe<TD>sshd<BR>syslogd<TD>pid_count<BR>runnning</TR>
<TR><TD>http<TD>server<TD>http://1.2.3.4/index.html<TD>response_time<BR>result_code</TR>
</TABLE>
"""

  ################### VIEW Alert config
  elif mode == "view":
    content += "<h2>Alert Config View</h2>"
    # Alert configuration
    try:
      req = Request(api_url + "/config/alert",method="GET")
      alerts = json.loads(json.load(urlopen(req)))
      alerts = sorted(alerts,key=lambda i: i['entity'] )

      content += "<TABLE class='blueTable'><TR><TH>Host<TH>Metric Class<TH>Metric Object<TH>Metric Instance<TH>Metric Name<TH>Alert Operator<TH>Alert Threshold<TH>Support Team<TH>Alert Tag</TR>"

      for r in alerts:
        entity = r['entity']
        metric_class = r['metric_class']
        metric_object = r['metric_object']
        metric_instance = r['metric_instance']
        metric_name = r['metric_name']
        alert_operator = r['alert_operator']
        alert_threshold = r['alert_threshold']
        support_team = r['support_team']
        try :
          alert_tag = r['alert_tag']
        except:
          alert_tag = ""

        params = "&entity=%s&metric_class=%s&metric_object=%s&metric_instance=%s&metric_name=%s&alert_operator=%s&alert_threshold=%s&support_team=%s&alert_tag=%s&edit=true" % ( entity,metric_class,metric_object,metric_instance,metric_name,alert_operator,alert_threshold,support_team,alert_tag)
        url = "/alert?" 
        content += "<TR><TD>%s<TD>%s<TD>%s<TD>%s<TD>%s<TD>%s<TD>%s<TD>%s<TD>%s<TD><A HREF='%s'>Edit</A><TD><A HREF='%s'>Delete</A></TR>" % ( entity,metric_class,metric_object,metric_instance,metric_name,alert_operator,alert_threshold,support_team,alert_tag,url + "mode=edit" + params, url + "mode=delete" + params)
      content += "</TABLE>"
    except:
      content += "<h3>Unable to get alert config</h3>"
    content += "<h3><A HREF='/alert?mode=edit'>Add New Alert</A></h3>"

  elif mode == "delete" :
    entity = args['entity']
    metric_class = args['metric_class']
    metric_object = args['metric_object']
    metric_instance = args['metric_instance']
    metric_name = args['metric_name']

    doc = {"entity":entity,"metric_class":metric_class,"metric_object":metric_object,"metric_instance":metric_instance,"metric_name":metric_name} 
    data = str(json.dumps(doc)).encode('utf-8')

    req = Request(api_url + "/config/alert",method='DELETE',data=data)
    req.add_header('Content-Type','application/json')
    resp = str(urlopen(req).read(),'utf-8')
 
    if resp == "deleted":
      content += "<h4><font color='Green'>Alert config Deleted from Database</font></h4>"
    else:
      content += "<h4><font color='Red'>** Alert was not deleted from Database (Response = %s)**</font></h4>" % (resp)

    content += "<h3><A HREF='/alert?mode=view'>View Alert Configuration</A></H3>"

  content += "</html>"

  return content
