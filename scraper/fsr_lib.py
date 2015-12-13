# this script grabs a list from
# festivalsero.com/
# http://www.festivalsero.com/style/argentine_tango-11
# http://www.festivalsero.com/style/tango_salon-375
# http://www.festivalsero.com/style/tango-33


from bs4 import BeautifulSoup
import daterangeparser 
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
  td = stew.find("div",{"class":"content_area"})
  title = td.h1.contents
  tdr = td.find_all("p")
  print "number of p is ",len(tdr)
  fburl = ''
  emurl=''
  sdate=''
  edate=''

  for t in tdr:
    if not t.span:
      continue
    label = ''.join(t.span.contents)
    print "Check label ",label
    if label=="More info:":
      url = t.a['href']
    if label=="Location:":
      where = t.find_all("a")
      country = ''.join(where[1].contents)
      city = ''.join(where[0].contents)
    if label=="Dates:":
      t.span.extract()
      when  = t.get_text()
      sdate,edate = daterangeparser.parse(when)
      
      print "Time is ",when 
      print "Start is ",sdate
      print "End is ",edate
  return sdate,edate,country,city,url,fburl,emurl


def mainpage(url):
  print "Opening ",url
  mylists = []
  while True:
    r = requests.get(url)
    stew = BeautifulSoup(r.text,'lxml')
    soup = stew.find("div",{"id":"festival-list"})
    row = soup.children
    while True:
      try:
        r = row.next()
        if (r.name != 'a'):
          continue
      except:
        break
      #only check the A
      inturl = 'http://www.festivalsero.com' + r['href']
      etitle = r['title'] 
      if r.b:
        ename = r.b.contents
        etype = True
        print "Found ", etitle
      else:
        ename = r.contents
        etype = False
        print "Skip ", etitle
      #, aplace, intref
      a1s,a1e,a2z,a2c,a3,a4,a5 = subpage(inturl)
      print "Dates are",a1s, a1e 
      print "Places are", a2z, a2c
      #,a2,a3,a4,a5
      mylist={}
      mylist['name'] = ename
      mylist['startdate'] = a1s
      mylist['enddate'] = a1e
      mylist['country'] = a2z
      mylist['city'] = a2c
      mylist['url'] = a3
      mylist['fburl'] = a4
      mylist['emurl'] = a5
      mylist['extra_fsrurl'] = inturl
      mylist['extra_fsrtyp'] = etype
      #mylists.append(mylist)
    break
  print "NO MORE!!"
  return mylists


