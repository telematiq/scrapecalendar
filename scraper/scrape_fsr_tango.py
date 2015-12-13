# this script grabs the current marathon list
# from festivalsero.com/style/tango-33

import fsr_lib
import json

url = 'http://www.festivalsero.com/style/tango-33'
mylists = fsr_lib.mainpage(url)
with open("../data/output_fsr_tango.json","w") as writeJSON:
  json.dump(mylists, writeJSON)

