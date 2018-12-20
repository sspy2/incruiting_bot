import requests
import json
import time
import datetime 

url = 'http://www.saramin.co.kr/zf_user/jobs/api/get-search-count?type=job-category&cat_cd=404'
url = 'http://www.saramin.co.kr/zf_user/jobs/api/get-search-count?type=job-category&cat_cd=417'
response = json.loads(requests.get(url).text)
result_list = response['result_list']

today_list = []
for job in result_list:
    t = time.gmtime(int(job['opening_dt']))
    if(str(datetime.date.today()) == '{}-{}-{}'.format(t.tm_year, t.tm_mon, t.tm_mday)):
        today_list.append(job)
    
print(len(today_list))
