#!/usr/bin/python3 

# This simple module reads the MaaS config file and stores in a list
# It is called by every other module to help determine things like
# Elasticsearch endpoint, etc

import configparser

conf = configparser.RawConfigParser()
conf.read('/app/maas/conf/env')

