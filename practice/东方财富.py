
import urllib.request


url = "https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery11230720644353114078_1734278619756&sortColumns=APPLY_DATE%2CSECURITY_CODE&sortTypes=-1%2C-1&pageSize=50&pageNumber=1&reportName=RPTA_APP_IPOAPPLY&columns=SECURITY_CODE%2CSECURITY_NAME%2CTRADE_MARKET_CODE%2CAPPLY_CODE%2CTRADE_MARKET%2CMARKET_TYPE%2CORG_TYPE%2CISSUE_NUM%2CONLINE_ISSUE_NUM%2COFFLINE_PLACING_NUM%2CTOP_APPLY_MARKETCAP%2CPREDICT_ONFUND_UPPER%2CONLINE_APPLY_UPPER%2CPREDICT_ONAPPLY_UPPER%2CISSUE_PRICE%2CLATELY_PRICE%2CCLOSE_PRICE%2CAPPLY_DATE%2CBALLOT_NUM_DATE%2CBALLOT_PAY_DATE%2CLISTING_DATE%2CAFTER_ISSUE_PE%2CONLINE_ISSUE_LWR%2CINITIAL_MULTIPLE%2CINDUSTRY_PE_NEW%2COFFLINE_EP_OBJECT%2CCONTINUOUS_1WORD_NUM%2CTOTAL_CHANGE%2CPROFIT%2CLIMIT_UP_PRICE%2CINFO_CODE%2COPEN_PRICE%2CLD_OPEN_PREMIUM%2CLD_CLOSE_CHANGE%2CTURNOVERRATE%2CLD_HIGH_CHANG%2CLD_AVERAGE_PRICE%2COPEN_DATE%2COPEN_AVERAGE_PRICE%2CPREDICT_PE%2CPREDICT_ISSUE_PRICE2%2CPREDICT_ISSUE_PRICE%2CPREDICT_ISSUE_PRICE1%2CPREDICT_ISSUE_PE%2CPREDICT_PE_THREE%2CONLINE_APPLY_PRICE%2CMAIN_BUSINESS%2CPAGE_PREDICT_PRICE1%2CPAGE_PREDICT_PRICE2%2CPAGE_PREDICT_PRICE3%2CPAGE_PREDICT_PE1%2CPAGE_PREDICT_PE2%2CPAGE_PREDICT_PE3%2CSELECT_LISTING_DATE%2CIS_BEIJING%2CINDUSTRY_PE_RATIO%2CINDUSTRY_PE%2CIS_REGISTRATION&quoteColumns=f2~01~SECURITY_CODE~NEWEST_PRICE&quoteType=0&filter=(APPLY_DATE%3E%272010-01-01%27)&source=WEB&client=WEB"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36"
}
req = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(req)
print(response.read().decode('utf-8'))
# print(response.read())

