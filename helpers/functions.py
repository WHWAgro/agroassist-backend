from json import dumps
from urllib.parse import urlparse
import io

import datetime

import random
import string
import unicodedata



def generateFileName():
  uniq_filename = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '-')
  
  return uniq_filename










def strip_accents(text):
    """
    Strip accents from input String.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    try:
        text = unicodedata(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)
  
def is_float(element):
    try:
        float(element)
        return True
    except ValueError:
        return False


def datetimeJSONConverter(date_value):
    if isinstance(date_value, datetime.datetime):
        return date_value.__str__()
      
def to_json(cursor):
  list_cur = list(cursor)
    
  return dumps(list_cur)
      



def randomPassword(length=8):
  # get random password pf length 8 with letters, digits, and symbols
  characters = string.ascii_letters + string.digits + string.punctuation
  password = ''.join(random.choice(characters) for i in range(length))

  return password
