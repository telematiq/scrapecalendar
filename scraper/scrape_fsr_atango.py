# this script grabs the current marathon list
# from festivalsero.com/style/argentine_tango-11

import fsr_lib
import json

url = 'http://www.festivalsero.com/style/argentine_tango-11'
mylists = fsr_lib.mainpage(url)
with open("../data/output_fsr_atango.json","w") as writeJSON:
  json.dump(mylists, writeJSON)

