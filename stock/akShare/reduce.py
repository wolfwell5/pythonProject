import akshare as ak

from stock.akShare.util.file_name import generate_file_name

"stock_hold_management_person_em"  # 东方财富网-数据中心-特色数据-高管持股-人员增减持股变动明细

stock_hold_management_person_em = ak.stock_hold_management_person_em('600769', '东财')
stock_hold_management_person_em.to_csv(generate_file_name('增减持股变动明细  东财'), index=False)
