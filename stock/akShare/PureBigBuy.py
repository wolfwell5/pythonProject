import akshare as ak
from stock.akShare.util.csv import generate_csv

#  排序 大单 小单 涨幅 排名表
"stock_fund_flow_big_deal"  # 同花顺-数据中心-资金流向-大单追踪

generate_csv(ak.stock_fund_flow_big_deal(), '大单追踪')
