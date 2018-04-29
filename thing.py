import urllib
import json
import time


def post(finger):
    url="https://api.thingspeak.com/update?api_key=F8R0OQQVN8HFCRCR&field1={}".format(finger)
    data = urllib.urlopen(url)
    #print data
    time.sleep(16)
