This project was started to build a self-service and partially automated front end to the Influx/Telegraf monitoring tools.

It uses (or rather relies on) :<BR>
<LI>InfluxDB - TSDB Store
<LI>Chronograf - Visualisation
<LI>Telegraf - Agents for metric collection
<LI>Elasticsearch - Used to store telegraf configs, alert definitions, logs, etc.
<LI>Apache HTTPD - Serves up web pages and acts as configuration point for Telegraf
  <BR>
<BR>
The features are as<BR> follows :<BR>
<BR>
<LI>Automated Telegraf deployment.  Agent calls in to a Webserver which builds a dynamic config based off config fragments.  <BR>
There is a front end to manage what gets deployed to each host and Telegraf calls the web server on startup with a series of params to help build the config
<LI>Event configuration.  Build threshold conditions based on metrics, and generate an alert when breached. (Alert not included).  Events can have multiple tags assigned to (see 3)
<LI>Event groups. Create a grouping of alerts based on tags and allow these to be evaluated as a single entity, showing the status as RAG status on screen.  Useful if you have a set of standard monitors on each box and you want to check them all in one go<BR>
<LI>Agent health.  Simple page to show status of each agent by showing host uptime and last measurement with simple RAG status<BR>
<BR>
Will write more when the project is a bit more mature.<BR>
