# this script grabs the current festival list
# from tangofestivals.net
# change 2016 to any other year

from bs4 import BeautifulSoup
import datetime
import requests
import json
import re

def subpage(iurl):
  r = requests.get(iurl)
  if not r:
    return ""
  stew = BeautifulSoup(r.text,'lxml')
  td = stew.find("h1")
  if not td:
    return ""
  weburl = td.a['href']
  return weburl

url = 'http://tangofestivals.net/sections/festivals/calendar_monthly.php'
year = '2016'
mylists = []

for i in range(1,12):
  pgurl = url + "?month=" + str(i) + "&year=" + year
  print "Opening ",pgurl
  r = requests.get(pgurl)
  stew = BeautifulSoup(r.text,'lxml')
  soup = stew.find("div",{"id":"container"})
  sop = soup.find_all("tr")
  print "there are ", len(sop), "entries"

  # start with empty list
  for row in sop:
    mylist = {}
    itncols = row.find_all("td")
    if len(itncols)!=2:
      #print "skip one"
      continue
    #print "ok one" 
    # should have 2 td
    g = itncols[0].find('span',{"class":"calWeeklyWeekday"})
    gd = g.contents 
    gdd = ''.join(gd)
    print "Date is ",gdd
    ps = re.split('\s-\s|,',gdd.strip())
    print ps
    sd = re.split('\s+',ps[0].strip()) 
    ed = re.split('\s+',ps[1].strip())
    sdd = sd[-1]
    edd = ed[-1]
    print sdd, edd
    sd = datetime.datetime.strptime(sdd,"%d/%m-%y")
    sdate = sd.strftime("%Y-%m-%d")
    ed = datetime.datetime.strptime(edd,"%d/%m-%y")
    edate = ed.strftime("%Y-%m-%d")
    print "split to (", sdate, ") (", edate, ")"
    h = itncols[0].find('span',{"class":"calWeeklyEventname"})
    if not h:
      #print "Not found name"
      continue
    #print "name found" 
    #print h.prettify()

    hd = h.get_text()
    fullname = hd.strip()
    print "FOund", fullname
    if not h.a:
      print "no anchor"
      inturl = ''
      exturl = ''
    else:   
      inturl = h.a['href']
      exturl = subpage(inturl)
    x = itncols[0].find('div',{"class":"calLocation"})
    xd = x.a.get_text()
    loc = xd.split(" - ")
    lon = loc[0]
    loccountry,loccity = lon.split(",",1)
    print "location is ", loccountry, '/', loccity 
    mylist['startdate'] = sdate
    mylist['enddate'] = edate
    mylist['country'] = loccountry
    mylist['city'] = loccity
    mylist['url'] = exturl
    mylist['name'] = fullname
    mylist['extra_tfurl'] = inturl
    mylists.append(mylist)



with open("../data/output_tangofest.json","w") as writeJSON:
  json.dump(mylists, writeJSON)





