import requests
import os

def PostToKintone(heart_rate):
	URL        = os.environ["KINTONE_APP_URL"]											# URL
	API_TOKEN  = os.environ["KINTONE_API_TOKEN"]
	appId = os.environ["APP_ID"]
	record={'heart_rate':{'value' : heart_rate}}
	data = {'app':appId,'record':record}
	headers = {"X-Cybozu-API-Token": API_TOKEN, "Content-Type" : "application/json"}
	resp=requests.post(URL+'/k/v1/record.json',json=data,headers=headers)
	return resp
