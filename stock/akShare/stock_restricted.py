import akshare as ak

from stock.akShare.util.file_name import generate_file_name

# 解禁数据不对啊？  详情参考 .csv file

# "stock_restricted_release_queue_sina"  # 限售解禁-新浪
# "stock_restricted_release_summary_em"  # 东方财富网-数据中心-特色数据-限售股解禁
# "stock_restricted_release_detail_em"  # 东方财富网-数据中心-限售股解禁-解禁详情一览
# "stock_restricted_release_queue_em"  # 东方财富网-数据中心-个股限售解禁-解禁批次
# "stock_restricted_release_stockholder_em"  # 东方财富网-数据中心-个股限售解禁-解禁股东

# stock_restricted_release_summary_em_df = ak.stock_restricted_release_summary_em('全部股票', '20250101', '20251231')
# stock_restricted_release_summary_em_df.to_csv(generate_file_name('解禁总计  东财'), index=False)

stock_restricted_release_detail_em = ak.stock_restricted_release_detail_em('20250101', '20251231')
stock_restricted_release_detail_em.to_csv(generate_file_name('解禁详情  东财'), index=False)

stock_restricted_release_queue_em = ak.stock_restricted_release_queue_em('301469')
stock_restricted_release_queue_em.to_csv(generate_file_name('解禁批次  东财'), index=False)

# stock_restricted_release_stockholder_em = ak.stock_restricted_release_stockholder_em('600769', '20250101')
# stock_restricted_release_stockholder_em.to_csv(generate_file_name('解禁股东  东财'), index=False)
