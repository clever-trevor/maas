# Module to contain useful functions, etc

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


