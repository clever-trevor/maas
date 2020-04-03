This project was started to build a self-service and partially automated front end to the Influx/Telegraf monitoring tools.

It uses (or rather needs) :
  InfluxDB - TSDB Store
  Chronograf - Visualisation
  Telegraf - Agents for metric collection
  Elasticsearch - Used to store telegraf configs, alert definitions, logs, etc.
  Apache HTTPD - Serves up web pages and acts as configuration point for Telegraf
  

The features are as follows :

1. Automated Telegraf deployment.  Agent calls in to a Webserver which builds a dynamic config based off config fragments.  
There is a front end to manage what gets deployed to each host and Telegraf calls the web server on startup with a series of params to help build the config
2. Event configuration.  Build threshold conditions based on metrics, and generate an alert when breached. (Alert not included).  
   Events can have multiple tags assigned to (see 3)
3. Event groups. Create a grouping of alerts based on tags and allow these to be evaluated as a single entity, showing the status as RAG status on screen.  
   Useful if you have a set of standard monitors on each box and you want to check them all in one go
4. Agent health.  Simple page to show status of each agent by showing host uptime and last measurement with simple RAG status

Will write more when the project is a bit more mature.
