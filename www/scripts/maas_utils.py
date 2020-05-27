#!/usr/bin/python3

# Module to contain any useful / generic functions

# This checks a value against and operator threshold and returns
# a BOOL if the condition is met
# e.g. 1 < 2 = True
def evaluate_metric(value,operator,threshold):
  status = False
  if operator == ">" :
    if value > float(threshold) :
      status = True
  elif operator == ">=" :
    if value >= float(threshold) :
      status = True
  elif operator == "<" :
    if value < float(threshold) :
      status = True
  elif operator == "<=" :
    if value <= float(threshold) :
      status = True
  elif operator == "=" :
    if value == float(threshold) :
      status = True

  return status


