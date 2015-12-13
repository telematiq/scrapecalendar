# this script grabs the current festival list
# from tango.info/festivals/2016
# change 2016 to any other year

from bs4 import BeautifulSoup
import urllib
import json
import re

def subpage(iurl):
  r = urllib.urlopen(iurl)
  if not r:
    return ""
  stew = BeautifulSoup(r,'lxml')
  td = stew.find("tr",{"class":"website"})
  if not td:
    return ""
  tdr = td.find_all("td")
  weburl = tdr[1].a['href']
  return weburl

url = 'https://tango.info/festivals/2016'
r = urllib.urlopen(url)
stew = BeautifulSoup(r,'lxml')


soup = stew.find("tbody").find_all("tr",{"class":"vevent"})

# start with empty list
mylists = []

for row in soup:
  mylist = {}
  cols = row.find_all("td")
  sdate= cols[0].contents
  edate= cols[1].contents
  fullname= cols[2].a.contents
  shorttitle= cols[2].a['title']
  flags = cols[3].span.find_all('a')
  loccountry= flags[0]['title']
  loccountry= re.sub('Tango Festivals ','',loccountry)
  loccity= flags[1]['title']
  loccity= re.sub('Tango Festivals ','',loccity)
  inturl= cols[2].a['href']
  relurl = 'https://tango.info'+inturl
  exturl = subpage(relurl)
  print "FOUND: ", sdate, loccountry, '/', loccity, exturl
  mylist['startdate'] = sdate
  mylist['enddate'] = edate
  mylist['country'] = loccountry
  mylist['city'] = loccity
  mylist['url'] = exturl
  mylist['name'] = fullname
  mylist['extra_title'] = shorttitle
  mylist['extra_tiurl'] = relurl
  mylists.append(mylist)



with open("../data/output_tangoinfo.json","w") as writeJSON:
  json.dump(mylists, writeJSON)





