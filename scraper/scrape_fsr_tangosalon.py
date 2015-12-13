# this script grabs the current marathon list
# from festivalsero.com/style/tango_salon-375

import fsr_lib
import json

url = 'http://www.festivalsero.com/style/tango_salon-375'
mylists = fsr_lib.mainpage(url)
with open("../data/output_fsr_tangosalon.json","w") as writeJSON:
  json.dump(mylists, writeJSON)

