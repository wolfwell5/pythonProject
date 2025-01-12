import urllib.request

# url = 'https://movie.douban.com/'
# url = 'https://www.douban.com/'
# url = 'http://cwzx.shdjt.com/cwcx.asp?gdmc=%C9%E7%B1%A3'  # 社保持仓
url = 'https://data.eastmoney.com/xg/xg/default.html' # 东方财富 新股
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36"
}
req = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(req)
print(response.read().decode('utf-8'))
# print(response.read())

