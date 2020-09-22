import datetime

def format_datetime(data):
  if not data is None:
    return data.strftime('%Y-%m-%d %H:%M:%S')
  return ""