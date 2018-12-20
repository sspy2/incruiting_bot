from flask import Flask, request
import requests
import os
import json
import time
import datetime

app = Flask(__name__)


BIG_CATEGORY = {402: '서버/네트워크/보안 전체',
                404: '웹개발', 
                407: '응용프로그램 개발 전체',
                409: 'ERP/시스템분석/설계 전체',
                410: '통신/모바일 전체',
                411: '하드웨어/소프트웨어 전체',
                416: '데이터베이스/DB 전체',
                417: '인공지능(AI)/빅데이터', 
                }
API_URL = 'https://api.hphk.io/telegram'
TOKEN = os.getenv('TELEGRAM_TOKEN')


def shorten_url(url):
    r = requests.post("https://api.rebrandly.com/v1/links", 
    data = json.dumps({
        "destination": url
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
        #print("Long URL was %s, short URL is %s" % (link["destination"], link["shortUrl"]))
    return link["shortUrl"]
    
    
def check_catetory():
    text = ''
    for cat in BIG_CATEGORY:
        text = text + '{}은(는) {} \n'.format(BIG_CATEGORY[cat], cat)
    return text
    
def today():
    today_list = []
    for num in BIG_CATEGORY:
        url = 'http://www.saramin.co.kr/zf_user/jobs/api/get-search-count?type=job-category&cat_cd={}'.format(num)
        response = json.loads(requests.get(url).text)
        result_list = response['result_list']
        for job in result_list:
            t = time.gmtime(int(job['opening_dt']))
            if(str(datetime.date.today()) == '{}-{}-{}'.format(t.tm_year, t.tm_mon, t.tm_mday)):
                today_list.append(job)
        
    return '오늘 전체 등록정보\n오늘의 정보가 {}건 새로 열렸습니다.'.format(len(today_list))

def today_info(num):
    today_list = []
    url = 'http://www.saramin.co.kr/zf_user/jobs/api/get-search-count?type=job-category&cat_cd={}'.format(num)
    print(url)
    response = json.loads(requests.get(url).text)
    result_list = response['result_list']
    for job in result_list:
        t = time.gmtime(int(job['opening_dt']))
        if(str(datetime.date.today()) == '{}-{}-{}'.format(t.tm_year, t.tm_mon, t.tm_mday)):
            today_list.append(job)
    
    result_dic = []
    for result in today_list:
        target = "http://www.saramin.co.kr/zf_user/jobs/relay/view?view_type=list&rec_idx=" + result["rec_idx"]
        url = shorten_url(target)
        result_dic.append("""
        회사명: {}\n모집분야: {}\n모집공고명: {}\n링크: {}\n회사 홈페이지: {}
        -------------------
        """.format(result["company_nm"], result["rec_division"], result["title"], url, result["homepage"]))
    # return "{}에 대한 등록정보\n오늘 채용공고가 {}건 새로 열렸습니다.\n{}".format(BIG_CATEGORY[int(num)], len(today_list), ''.join(result_dic))
    return result_dic

@app.route("/{}".format(os.getenv('TELEGRAM_TOKEN')), methods=['POST'])
def telegram():
    document = request.get_json()
    chat_id = document['message']['from']['id']
    query = document['message']['text']
    count = 1
    if(query == '분야'):
        result = [check_catetory()]
    elif(query == '오늘'):
        result = [today()]
    elif(int(query) in BIG_CATEGORY.keys()):
        result = today_info(query)
        count = len(result)
        text = "{}에 대한 채용공고가 {}건 있습니다.".format(BIG_CATEGORY[int(query)], count)
        requests.get('{}/bot{}/sendMessage?chat_id={}&text={}'.format(API_URL, TOKEN, chat_id, text))
    else:
        result = ["알 수 없는 명령어 입니다.\n분야정보: '분야',\n금일 업데이트: '오늘',\n분야별은 '분야'를 참고하세요."]
    for i in range(count):
        requests.get('{}/bot{}/sendMessage?chat_id={}&text={}'.format(API_URL, TOKEN, chat_id, result[i]))
    return '', 200
    
@app.route('/set_webhook')
def set_webhook():
    msg = requests.get('https://api.hphk.io/telegram/bot{}/setWebhook?url=https://incruiting-bot-lovings2u.c9users.io/{}'.format(os.getenv('TELEGRAM_TOKEN'), os.getenv('TELEGRAM_TOKEN')))
    print(msg.text)
    return '{}'.format(msg), 200
    
@app.route('/delete_webhook')
def delete_webhook():
    msg = requests.get('https://api.hphk.io/telegram/bot{}/deleteWebhook'.format(os.getenv('TELEGRAM_TOKEN')))
    print(msg.text)
    return '{}'.format(msg), 200