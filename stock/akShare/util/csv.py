import os
import sys

import pandas as pd

# 添加 akShare 目录到路径， 否则tickflow 使用不了gen csv方法
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from file_name import generate_file_name


# 生成 csv 文件 到当前执行程序的同一目录下
def generate_csv(data_frame, file_name, specific_folder):
    full_path_csv = generate_file_name(file_name, specific_folder)

    # 对数值列进行四舍五入，保留两位小数
    df_formatted = data_frame.copy()
    numeric_columns = df_formatted.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_columns:
        df_formatted[col] = df_formatted[col].apply(lambda x: round(x, 2) if pd.notna(x) else x)

    df_formatted.to_csv(full_path_csv, index=False)
    print(f'生成 csv 文件完毕，路径：{full_path_csv}')

# append 数据到 csv 文件中 todo
