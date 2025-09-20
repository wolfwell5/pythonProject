import akshare as ak
from stock.akShare.util.csv import generate_csv

# generate_csv(ak.stock_individual_info_em(symbol="sh600000"), '内外盘')
# spot_data = ak.stock_zh_a_spot()
# print(spot_data[['内盘', '外盘']])


# spot_data = ak.stock_zh_a_spot()
# filtered_data = spot_data[spot_data['代码'] == '300600']
# # print(filtered_data[['内盘', '外盘']])
# generate_csv(filtered_data, '内外盘')


# 获取实时行情数据
# stock_zh_a_spot_df = ak.stock_zh_a_spot()
# generate_csv(stock_zh_a_spot_df.head(), '实时行情数据 head')

# 获取特定股票的详细数据（内外盘等）
# stock_individual_info_em_df = ak.stock_individual_info_em(symbol="sh300600")
# generate_csv(stock_individual_info_em_df, '内外盘数据')


# stock_info = ak.stock_individual_info_em(symbol="300600")
# print(stock_info[['内盘', '外盘']])


# 获取所有 A 股代码与名称的映射
# stock_list = ak.stock_info_a_code_name()
# generate_csv(stock_list, '所有A股代码与名称映射')

# 查找包含 "300600" 的股票（例如创业板股）
# target_stock = stock_list[stock_list['code'] == '300600']
# print(target_stock)
#
# # 使用正确的 symbol 查询个股信息
# symbol = f"{target_stock['market'].values[0]}.{target_stock['code'].values[0]}"
# stock_info = ak.stock_individual_info_em(symbol=symbol)
# print(stock_info[['内盘', '外盘']])


# stock_bid_ask_em_df = ak.stock_bid_ask_em("300600")  --拿不到数据
# generate_csv(stock_bid_ask_em_df, "内外盘")

