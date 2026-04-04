import akshare as ak

# 获取所有A 股代码与名称的映射
from akShare.util.csv_utils import generate_csv

stock_list = ak.stock_info_a_code_name()
# print(stock_list)

generate_csv(stock_list, 'stocks', specific_folder='')
