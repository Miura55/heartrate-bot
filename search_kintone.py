import requests

headers = {
    'X-Cybozu-API-Token': 'ttH24dcvOrkQRtr22Mu0ZvIrw9U7MQVpjD0RVq5h',
}

params = (
    ('app', '13'),
    ('query', 'save_date = TODAY()'),
)

response = requests.get('https://devksmpdi.cybozu.com:443/k/v1/records.json', headers=headers, params=params)
records = response.json()["records"]

res = ""
for num in range(10):
    res += records[num]["save_date"]["value"] + " " + records[num]["heart_rate"]["value"] + "\n"

print(res)
