import requests
import datetime as dt
from datetime import datetime
import os

URL        = os.environ["KINTONE_APP_URL"]											# URL
API_TOKEN  = os.environ["KINTONE_API_TOKEN"]
appId = os.environ["APP_ID"]

def PostToKintone(heart_rate):
	record={'heart_rate':{'value' : heart_rate}}
	data = {'app':appId,'record':record}
	headers = {"X-Cybozu-API-Token": API_TOKEN, "Content-Type" : "application/json"}
	resp=requests.post('{}/k/v1/record.json'.format(URL),json=data,headers=headers)
	return resp

def query_kintone():
    now = datetime.now()
    min_10s = now - dt.timedelta(seconds=10)
    min_10s = min_10s.strftime('%Y-%m-%dT%H:%M:%mZ')
    headers = {
        'X-Cybozu-API-Token': API_TOKEN,
    }
    params = (
        ('app', appId),
        ('query', 'save_date = TODAY() limit 10'),
    )

    response = requests.get('{}/k/v1/records.json'.format(URL), headers=headers, params=params)
    records = response.json()["records"]

    res = ""
    for num in records:
        res += num["save_date"]["value"] + " " + num["heart_rate"]["value"] + "\n"

    return res
