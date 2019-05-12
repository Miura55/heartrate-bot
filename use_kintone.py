import requests
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
    headers = {
        'X-Cybozu-API-Token': API_TOKEN,
    }
    params = (
        ('app', appId),
        ('query', 'save_date = TODAY()'),
    )

    response = requests.get('{}/k/v1/records.json'.format(URL), headers=headers, params=params)
    records = response.json()["records"]

    res = ""
    for num in range(10):
        res += records[num]["save_date"]["value"] + " " + records[num]["heart_rate"]["value"] + "\n"

    return res
