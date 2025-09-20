import akshare as ak
from stock.akShare.util.csv import generate_csv

# A股龙虎榜 新浪
# "stock_lhb_detail_daily_sina"  # 龙虎榜-每日详情
# "stock_lhb_ggtj_sina"  # 龙虎榜-个股上榜统计
# "stock_lhb_yytj_sina"  # 龙虎榜-营业上榜统计
# "stock_lhb_jgzz_sina"  # 龙虎榜-机构席位追踪
# "stock_lhb_jgmx_sina"  # 龙虎榜-机构席位成交明细
# 东方财富-股票数据-龙虎榜

"stock_lhb_detail_em"  # 东方财富网-数据中心-龙虎榜单-龙虎榜详情
"stock_lhb_stock_statistic_em"  # 东方财富网-数据中心-龙虎榜单-个股上榜统计
"stock_lhb_stock_detail_em"  # 东方财富网-数据中心-龙虎榜单-个股龙虎榜详情
"stock_lhb_jgmmtj_em"  # 东方财富网-数据中心-龙虎榜单-机构买卖每日统计
"stock_lhb_hyyyb_em"  # 东方财富网-数据中心-龙虎榜单-每日活跃营业部
"stock_lhb_yybph_em"  # 东方财富网-数据中心-龙虎榜单-营业部排行
"stock_lhb_jgstatistic_em"  # 东方财富网-数据中心-龙虎榜单-机构席位追踪
"stock_lhb_traderstatistic_em"  # 东方财富网-数据中心-龙虎榜单-营业部统计

generate_csv(ak.stock_lhb_detail_em('20250101', '20250226'), '龙虎榜详情')

# generate_csv(ak.stock_lhb_stock_statistic_em(), '个股上榜统计')
# # 没在龙虎榜，会报错
# generate_csv(ak.stock_lhb_stock_detail_em('000818', '20250225', '卖出'), '个股龙虎榜详情')
# generate_csv(ak.stock_lhb_jgmmtj_em('20250101', '20250224'), '机构买卖每日统计')
# generate_csv(ak.stock_lhb_hyyyb_em('20250101', '20250224'), '每日活跃营业部')
# generate_csv(ak.stock_lhb_yybph_em('近三月'), '营业部排行')
# generate_csv(ak.stock_lhb_jgstatistic_em('近三月'), '机构席位追踪')
# generate_csv(ak.stock_lhb_traderstatistic_em('近三月'), '营业部统计')
