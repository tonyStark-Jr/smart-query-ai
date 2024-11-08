import requests
proxies = {
"http": "http://iec2022027:praKhar@5@172.31.2.4:8080"
}
payload={
    'api_key'
}
r = requests.get('http://httpbin.org/ip', proxies=proxies, verify=False)
print(r.text)