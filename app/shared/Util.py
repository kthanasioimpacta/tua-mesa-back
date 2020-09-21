import datetime

def format_datetime(data):
  if data is None:
    return data

  return data.strftime('%Y-%m-%d %H%:%M:%S')