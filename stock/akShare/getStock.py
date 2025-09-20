import akshare as ak


# stock_sse_summary_df = ak.stock_sse_summary()
# print(stock_sse_summary_df)

# stock_szse_summary_df = ak.stock_szse_summary(date="20200619")
# stock_szse_summary_df = ak.stock_szse_summary()
# print(stock_szse_summary_df)

# stock_szse_area_summary_df = ak.stock_szse_area_summary(date="202412")
# print(stock_szse_area_summary_df)


# stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
# print(stock_zh_a_spot_em_df)


# 实时雪球行情， not work
# stock_individual_spot_xq_df = ak.stock_individual_spot_xq(symbol="SH600769")
# print(stock_individual_spot_xq_df.dtypes)
# stock_individual_spot_xq_df = ak.stock_individual_spot_xq(symbol="SPY")
# print(stock_individual_spot_xq_df.dtypes)


# 历史行情数据-东财     https://akshare.akfamily.xyz/data/stock/stock.html#id22
# stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="600769", period="daily", start_date="20240101", end_date='20250127', adjust="qfq")
# print(stock_zh_a_hist_df)


# 历史行情数据-新浪
# 限量: 单次返回指定沪深京 A 股上市公司指定日期间的历史行情日频率数据, 多次获取容易封禁 IP
# stock_zh_a_daily_qfq_df = ak.stock_zh_a_daily(symbol="sh600769", start_date="20240101", end_date="20250127", adjust="qfq")
# print(stock_zh_a_daily_qfq_df)


# 历史行情数据-腾讯
# 限量: 单次返回指定沪深京 A 股上市公司、指定周期和指定日期间的历史行情日频率数据
# 速度有点慢，还有进度条。。。
# stock_zh_a_hist_tx_df = ak.stock_zh_a_hist_tx(symbol="sh600769", start_date="20240101", end_date="20250127", adjust="qfq")
# print(stock_zh_a_hist_tx_df)


# 日内分时数据-东财     https://akshare.akfamily.xyz/data/stock/stock.html#id27
# 限量: 单次返回指定股票最近一个交易日的分时数据, 包含盘前数据
# 数据示例
#          时间    成交价    手数 买卖盘性质
# 0     09:15:00  10.60    11   中性盘
# 1     09:15:09  10.57  1547   中性盘
# 4400  15:00:00  10.50  8338    买盘

# stock_intraday_em_df = ak.stock_intraday_em(symbol="600769")
# print(stock_intraday_em_df.to_string())
# to_string() 方法打印全部， debug 看到有array 很多值


# 日内分时数据-新浪
# 数据不一致，提个 issue  辣鸡新浪
# stock_intraday_sina_df = ak.stock_intraday_sina(symbol="sh600769", date="20250127")
# print(stock_intraday_sina_df.to_string())


# 腾讯财经
#  获取较慢，等待5秒，但是和同花顺、东财完全一致
# stock_zh_a_tick_tx_js_df = ak.stock_zh_a_tick_tx_js(symbol="sh600769")
# print(stock_zh_a_tick_tx_js_df.to_string())


# 历史分笔数据      https://akshare.akfamily.xyz/data/stock/stock.html#id30
# 腾讯财经    实际就是当天的每笔成交
# stock_zh_a_tick_tx_js_df = ak.stock_zh_a_tick_tx_js(symbol="sh600769")
# stock_zh_a_tick_tx_js_df.to_csv(generate_file_name('历史分笔数据  东财'), index=False)


# 机构调研      https://akshare.akfamily.xyz/data/stock/stock.html#id69
# stock_jgdy_tj_em_df = ak.stock_jgdy_tj_em(date="20250107")
# stock_jgdy_tj_em_df.to_csv(generate_file_name('机构调研  东财'), index=False)


# 机构调研-详细
# stock_jgdy_detail_em_df = ak.stock_jgdy_detail_em(date="20250107")


# 主营介绍-同花顺        https://akshare.akfamily.xyz/data/stock/stock.html#id72
# stock_zyjs_ths_df = ak.stock_zyjs_ths(symbol="000066")


# 股票账户统计
# 描述: 东方财富网-数据中心-特色数据-股票账户统计
# 限量: 单次返回从 201504 开始 202308 的所有账户增减数据，只更新到 23年
# https://data.eastmoney.com/cjsj/yzgptjnew.html
# stock_account_statistics_em_df = ak.stock_account_statistics_em()
# print(stock_account_statistics_em_df)
# stock_account_statistics_em_df.to_csv('data', mode='a', index=False, header=True)  # header=False 表示不保存列名



# 年报季报    https://akshare.akfamily.xyz/data/stock/stock.html#id129
# todo  0210



# 股东持股统计-十大流通股东
# https://akshare.akfamily.xyz/data/stock/stock.html#id209
# todo 这个没搞懂，只返回了38条数据，文档说返回所有数据， 返回数据在 holders 文件。 20240930_holders 似乎有全部数据，241231日期 很多企业未公告？
# stock_gdfx_free_holding_statistics_em_df = ak.stock_gdfx_free_holding_statistics_em(date="20240930")
# stock_gdfx_free_holding_statistics_em_df.to_csv('20240930_holders', mode='a', index=False, header=True)

# 股东户数 todo 结合A股总市值，户数增减，可判断多空风向
# https://akshare.akfamily.xyz/data/stock/stock.html#id213
# stock_zh_a_gdhs_df = ak.stock_zh_a_gdhs(symbol="20230930")
# print(stock_zh_a_gdhs_df)


# 财务指标
# https://akshare.akfamily.xyz/data/stock/stock.html#id196
# 限量: 单次获取指定 symbol 和 start_year 的所有财务指标历史数据
# stock_financial_analysis_indicator_df = ak.stock_financial_analysis_indicator(symbol="600769", start_year="2024")
# print(stock_financial_analysis_indicator_df.to_string())


# 热门 可以综合问财和东财起来 todo
# stock_hot_rank_wc_df = ak.stock_hot_rank_wc(date="20250207")
# stock_hot_rank_wc_df.to_csv(f'最热门 问财 {datetime.now().strftime("当前日期：%Y-%m-%d")}.csv')

# stock_hot_rank_em_df = ak.stock_hot_rank_em()
# stock_hot_rank_em_df.to_csv(f'最热门 东财 {datetime.now().strftime("当前日期：%Y-%m-%d")}.csv')


# 飙升榜
# 限量: 单次返回当前交易日前 100 个股票的飙升榜排名数据
# stock_hot_up_em_df = ak.stock_hot_up_em()
# stock_hot_up_em_df.to_csv(f'飙升榜 东财 {datetime.now().strftime("当前日期：%Y-%m-%d")}.csv')


# 热门关键词
# 限量: 单次返回指定 symbol 的最近交易日时点数据
# stock_hot_keyword_em_df = ak.stock_hot_keyword_em(symbol="SH600769")
# stock_hot_keyword_em_df.to_csv(f'热门关键词 东财 {datetime.now().strftime("当前日期：%Y-%m-%d")}.csv')


# 热搜股票  https://akshare.akfamily.xyz/data/stock/stock.html#id374
# 组合文件夹路径和文件名
# stock_hot_search_baidu_df = ak.stock_hot_search_baidu(symbol="A股", date="20250207", time="今日")
# stock_hot_search_baidu_df.to_csv(generate_file_name('热搜股票 百度'), index=False)

# 盘口异动 https://akshare.akfamily.xyz/data/stock/stock.html#id376
# stock_changes_em_df = ak.stock_changes_em(symbol="大笔买入")
# stock_changes_em_df.to_csv(generate_file_name('盘口异动  东财'), index=False)


# 涨停股池 https://akshare.akfamily.xyz/data/stock/stock.html#id378  会剔除ST股
# stock_zt_pool_em_df = ak.stock_zt_pool_em(date='20250207')
# stock_zt_pool_em_df.to_csv(generate_file_name('涨停股池  东财'), index=False)

# 昨日涨停股池    https://akshare.akfamily.xyz/data/stock/stock.html#id380
# stock_zt_pool_previous_em_df = ak.stock_zt_pool_previous_em(date='20250207')
# stock_zt_pool_previous_em_df.to_csv(generate_file_name('昨日涨停股池  东财'), index=False)
