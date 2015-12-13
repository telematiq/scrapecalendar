# this script grabs the current marathon list
# from tangomarathons.com/events/categories/marathon/
# could be more than one page ?pno=2

from bs4 import BeautifulSoup
import urllib2
import datetime
import requests
import re

def subpage(iurl):
  print "Opening ",iurl
  retry=0
  while True:
    try:
      r = requests.get(iurl)
      break
    except requests.ConnectionError:
      print "FAILED",retry
      retry=retry+1
      if retry > 5:
        return '','','','','','',''
      continue
  stew = BeautifulSoup(r.text,'lxml')
  td = stew.find("table",{"class":"event_facts"})
  tdr = td.find_all("tr")
  when  = tdr[1].find_all("td")[1].contents
  when  = ''.join(when)
  where = tdr[2].find_all("td")[1].contents
  where = ''.join(where)
  links = tdr[0].find_all("td")[1].find_all("a")
  url=''
  fburl=''
  emurl=''
  c = len(links)
  if c > 2:
    emurl = links[2]['href'] 
  if c > 1:
    fburl = links[1]['href']
  if c > 0:
    url = links[0]['href']
  sdate,edate = when.split(' - ')
  sd = datetime.datetime.strptime(sdate, "%d/%m/%Y")
  sdate = sd.strftime("%Y-%m-%d")
  ed = datetime.datetime.strptime(edate, "%d/%m/%Y")
  edate = ed.strftime("%Y-%m-%d")
  
  parts = where.split(', ')
  country = parts.pop()
  city = ' '.join(parts)
  return sdate,edate,country,city,url,fburl,emurl


def mainpage(url):
  mylists = []
  while True:
    r = urllib2.urlopen(url)
    stew = BeautifulSoup(r,'lxml')
    soup = stew.find("div",{"class":"entry-content"}).ul
    row = soup.children
    while True:
      try:
        r = row.next()
        if (r.name != "hr"):
          continue
        r = row.next()
        drange = r.contents
        r = row.next()
      except:
        break
      fullname = r.a.contents
      intref = r.a['href']
      aplace = r.i.contents
      print "Found ", fullname
      #, aplace, intref
      a1s,a1e,a2z,a2c,a3,a4,a5 = subpage(intref)
      print a1s, a1e 
      print a2z, a2c
      #,a2,a3,a4,a5
      mylist={}
      mylist['name'] = fullname
      mylist['startdate'] = a1s
      mylist['enddate'] = a1e
      mylist['country'] = a2z
      mylist['city'] = a2c
      mylist['url'] = a3
      mylist['fburl'] = a4
      mylist['emurl'] = a5
      mylist['extra_tmdurl'] = intref
      mylists.append(mylist)
  
    pagesnav = stew.find("span",{"class":"em-pagination"})
    if not pagesnav:
      break
    pagenext = pagesnav.find("a",{"class":"next"})
    if not pagenext:
      break
    url = "http://tangomarathons.com" + pagenext['href']
    print "ANOTHER PAGE"
  print "NO MORE!!"
  return mylists


