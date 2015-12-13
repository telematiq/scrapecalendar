# this script grabs the current marathon list
# from tangomarathons.com/events/categories/marathon/
# could be more than one page ?pno=2

import tmd_lib
import json

url = 'http://tangomarathons.com/events/categories/festivalito/'
mylists = tmd_lib.mainpage(url)
with open("../data/output_tmd_festivalitos.json","w") as writeJSON:
  json.dump(mylists, writeJSON)

