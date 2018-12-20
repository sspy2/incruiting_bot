small_category = {'웹개발>백엔드': 40430, }

big_category = {'웹개발': 404, '인공지능(AI)/빅데이터': 417, '하드웨어/소프트웨어 전체': 411}


import requests
import json
import os
r = requests.post("https://api.rebrandly.com/v1/links", 
  data = json.dumps({
        "destination": "https://www.youtube.com/channel/UCHK4HD0ltu1-I212icLPt3g"
      , "domain": { "fullName": "rebrand.ly" }
    # , "slashtag": "A_NEW_SLASHTAG"
    # , "title": "Rebrandly YouTube channel"
  }),
  headers={
    "Content-type": "application/json",
    "apikey": os.getenv('REBRAND_KEY'),
    "workspace": os.getenv('REBRAND_WORKSPACE')
  })

if (r.status_code == requests.codes.ok):
  link = r.json()
  print("Long URL was %s, short URL is %s" % (link["destination"], link["shortUrl"]))