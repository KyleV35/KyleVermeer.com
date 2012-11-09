import logging
from google.appengine.api import memcache

def safeMemcacheSet(key,value):
    if memcache.set(key,value) is False:
        logging.error("Memcache set error for key %s and value %s" % (key,value))