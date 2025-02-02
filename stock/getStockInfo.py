import yinhepy.yinhe as yh
import urllib.request

# df = yh.history_stock_data("SH.600000", "2024-12-16", "2024-12-18", "15min")

# df = yh.history_stock_data("SH.600000", "2024-12-16", "2024-12-18", "D")
# print(df)
#
# df.to_csv(r"E:\Develop\Repos\pythonProject\stock\files\hq.csv")


# 十大流通股东
top10HolderUrl = "http://api.mairui.club/hscp/ltgd/600769/8AB76BBC-1B08-496E-B240-DF178AAFCBB5"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36"
}
req = urllib.request.Request(top10HolderUrl, headers=headers)
response = urllib.request.urlopen(req)
print(response.read().decode('utf-8'))
# print(response.read())

