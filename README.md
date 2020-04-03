This project was started to build a self-service and partially automated front end to the Influx/Telegraf monitoring tools.

It uses (or rather needs) :<BR>
  InfluxDB - TSDB Store<BR>
  Chronograf - Visualisation<BR>
  Telegraf - Agents for metric collection<BR>
  Elasticsearch - Used to store telegraf configs, alert definitions, logs, etc.<BR>
  Apache HTTPD - Serves up web pages and acts as configuration point for Telegraf<BR>
  <BR>
<BR>
The features are as<BR> follows :<BR>
<BR>
1. Automated Telegraf deployment.  Agent calls in to a Webserver which builds a dynamic config based off config fragments.  <BR>
There is a front end to manage what gets deployed to each host and Telegraf calls the web server on startup with a series of params to help build the config<BR>
2. Event configuration.  Build threshold conditions based on metrics, and generate an alert when breached. (Alert not included).  
   Events can have multiple tags assigned to (see 3)<BR>
3. Event groups. Create a grouping of alerts based on tags and allow these to be evaluated as a single entity, showing the status as RAG status on screen.  <BR>
   Useful if you have a set of standard monitors on each box and you want to check them all in one go<BR>
4. Agent health.  Simple page to show status of each agent by showing host uptime and last measurement with simple RAG status<BR>
<BR>
Will write more when the project is a bit more mature.<BR>
