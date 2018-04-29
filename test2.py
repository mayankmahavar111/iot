import urllib
from bs4 import BeautifulSoup
import time

data=urllib.urlopen("https://api.thingspeak.com/update?api_key=F8R0OQQVN8HFCRCR&field1=10&field2=60")
print data
"""
time.sleep(16)
data=urllib.urlopen("https://api.thingspeak.com/update?api_key=F8R0OQQVN8HFCRCR&field2=10")
print data
"""
