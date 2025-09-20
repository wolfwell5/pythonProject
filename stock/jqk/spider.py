import csv
import time

import parsel
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from stock.jqk.basicReqeustParam.headers import tempHeader
from stock.jqk.paths.cssPath import tbodyPath
from stock.jqk.utils.loadLocalHtml import loadLocalHtml
from stock.jqk.utils.sleepRandom import sleep_random

basicUrl = "https://q.10jqka.com.cn/index/index/board/all/field/xj/order/desc/page/{page}/ajax/1/"
holderUrl = "https://basic.10jqka.com.cn/{stock_code}/holder.html"

excel_title = [
    '序号',
    '代码',
    '名称',
    '现价',
    '涨跌幅(%)',
    '涨跌',
    '涨速(%)',
    '换手(%)',
    '量比',
    '振幅(%)',
    '成交额',
    '流通股',
    '流通市值',
    '市盈率',
    'link',
]

total_page_num = 1
csv_file_name = 'allStocks.csv'


def getStocksOfOnePage(url) -> str:
    # response = requests.get(basic_url, headers=chromeHeaders, stream=True)
    response = requests.get(url, headers=tempHeader, stream=True)
    response.encoding = 'gbk'
    data = response.text

    # print(rf'getStocksOfOnePage {data}')
    return data


def fetchHoldInfo(code) -> str:
    print(rf'code is {code}')
    # seleniumFuc()
    holder_url = holderUrl.format(stock_code=code)
    hodl_info = getStocksOfOnePage(holder_url)
    print(rf'hodl_info: {hodl_info}')
    return hodl_info


def theadParse(csv_file) -> csv.DictWriter:
    csv_writer = csv.DictWriter(csv_file, fieldnames=excel_title)
    csv_writer.writeheader()

    return csv_writer


def tbodyParse(selector, csv_writer):
    tbody = selector.css(tbodyPath)
    data_row = {}

    for y, row in enumerate(tbody):
        # if y > 0:
        #     break
        # print(f"y: {y}, el: {row}")
        tds = row.css('td')
        link = ''
        for col, td in enumerate(tds):
            if col == 1:
                # print(f'col: {col},    code: {td.css("a::text").get()}')
                data_row[excel_title[col]] = td.css("::text").get()
                link = td.css("a::attr(href)").get()
            else:
                # print(f'col: {col},    val: {td.css("::text").get()}')
                data_row[excel_title[col]] = td.css("::text").get()
        data_row[excel_title[14]] = link
        # print(f'data_row:  {data_row}')
        csv_writer.writerow(data_row)


def fetchAllStockCodes():
    csv_file = open(csv_file_name, mode='w', encoding='utf-8', newline='')
    csv_writer = theadParse(csv_file)

    for i in range(total_page_num):
        each_page_url = basicUrl.format(page=i + 1)
        stocks = getStocksOfOnePage(each_page_url)

        # stocks = loadLocalHtml('./testdata/temp.html')
        print(rf'fetchAllStockCodes stocks{stocks}')
        selector = parsel.Selector(stocks)

        tbodyParse(selector, csv_writer)

        sleep_random()


def parseHoldInfo(hold_info_html):
    stocks = loadLocalHtml('./testdata/holder.html', 'gbk')
    print(f'stocks {stocks}')


def main():
    # getAllStockList(basicUrl)
    # 1. get all stock code, save in DB
    # 2. fetch from DB, use stock code to get all holder info
    # fetchAllStockCodes()
    # hold_info = fetchHoldInfo(688692)
    parseHoldInfo("hold_info")


if __name__ == "__main__":
    main()


def seleniumFuc():
    holder_url = holderUrl.format(stock_code=688692)

    # 指定 ChromeDriver 的路径
    driver_path = 'C:/Program Files/Google/Chrome/chromedriver-win64/chromedriver.exe'
    # 创建一个 Service 对象
    service = Service(driver_path)
    # 使用 Service 对象来初始化 Chrome 浏览器驱动
    driver = webdriver.Chrome(service=service)
    driver.get(holder_url)

    # 可以使用显式等待确保页面动态内容加载完成
    time.sleep(7)

    page_source = driver.page_source
    print(page_source)

    driver.quit()
