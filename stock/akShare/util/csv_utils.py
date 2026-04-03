"""
CSV 文件生成工具

提供 DataFrame 格式化和 CSV 文件保存功能
"""

import os
import sys

import pandas as pd

# 添加 akShare 目录到路径，以便导入 file_name 模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from file_name import (
    generate_file_name,
    build_folder_path,
    ensure_directory_exists,
    get_akshare_base_path
)


def format_numeric_columns(data_frame, decimal_places=2):
    """
    对 DataFrame 的数值列进行四舍五入处理
    
    Args:
        data_frame: DataFrame 数据
        decimal_places: 保留小数位数，默认 2 位
        
    Returns:
        DataFrame: 格式化后的 DataFrame
    """
    df_formatted = data_frame.copy()
    numeric_columns = df_formatted.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_columns:
        df_formatted[col] = df_formatted[col].apply(
            lambda x: round(x, decimal_places) if pd.notna(x) else x
        )
    return df_formatted


def _save_dataframe(data_frame, full_path, encoding='utf-8-sig', index=False):
    """
    内部方法：保存 DataFrame 到 CSV 文件
    
    Args:
        data_frame: DataFrame 数据
        full_path: 完整文件路径
        encoding: 文件编码（默认 utf-8-sig）
        index: 是否保存索引（默认 False）
    """
    # 确保目录存在
    ensure_directory_exists(os.path.dirname(full_path))
    
    # 格式化数值列
    df_formatted = format_numeric_columns(data_frame)
    
    # 保存到文件
    df_formatted.to_csv(full_path, index=index, encoding=encoding)
    print(f'生成 CSV 文件完毕，路径：{full_path}')


# 生成 csv 文件 到当前执行程序的同一目录下
def generate_csv(data_frame, file_name, specific_folder):
    """
    生成 CSV 文件（自动添加时间戳）
    
    Args:
        data_frame: DataFrame 数据
        file_name: 文件名（不含扩展名，会自动添加时间戳）
        specific_folder: 子文件夹名称
    """
    full_path_csv = generate_file_name(file_name, specific_folder, add_timestamp=True)
    _save_dataframe(data_frame, full_path_csv, encoding='utf-8')


def save_csv_with_name(data_frame, file_name, specific_folder):
    """
    生成 CSV 文件（使用指定文件名，不添加时间戳）
    
    Args:
        data_frame: DataFrame 数据
        file_name: 完整文件名（含 .csv 扩展名）
        specific_folder: 子文件夹名称
    
    Returns:
        str: 生成的文件完整路径
    """
    # 确保文件名以 .csv 结尾
    if not file_name.lower().endswith('.csv'):
        file_name += '.csv'
    
    # 使用 generate_file_name 来构建路径（会追溯到调用者目录）
    full_path_csv = generate_file_name(file_name, specific_folder, add_timestamp=False)
    
    # 保存文件
    _save_dataframe(data_frame, full_path_csv)
    
    return full_path_csv

