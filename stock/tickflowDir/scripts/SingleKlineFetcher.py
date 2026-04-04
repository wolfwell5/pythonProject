"""
单只股票 K 线数据获取器

提供两种使用方式：
1. 直接使用工具函数（简单场景）
2. 使用 SingleKlineFetcher 类（复杂场景，需要状态管理）
"""

import os
import sys
import time
from datetime import datetime, timedelta

# 添加 stock 目录到 Python 路径
script_dir = os.path.dirname(os.path.abspath(__file__))
stock_dir = os.path.dirname(os.path.dirname(script_dir))  # stock 目录
sys.path.insert(0, stock_dir)

import pandas as pd
from akShare.util.csv_utils import generate_csv
from tickflow import TickFlow


# ============================================================
# 工具函数 - 简单、纯粹、可复用
# ============================================================

def get_kline_data(code, api_key=None, count=10000, period="1d", adjust='forward_additive'):
    """
    获取单只股票 K 线数据
    
    Args:
        code: 股票代码，如 '300164.SZ'
        api_key: TickFlow API 密钥，默认使用内置密钥
        count: 获取数据条数，默认 10000
        period: K 线周期，默认 '1d' (日 K)
        adjust: 复权类型，默认 'forward_additive' (前复权)
        
    Returns:
        DataFrame: K 线数据
    """
    api_key = api_key or "tk_70e08101458040caa8fe082bf28587ac"
    tf = TickFlow(api_key=api_key, max_retries=5, timeout=60.0)
    return tf.klines.get(code, period=period, adjust=adjust, count=count, as_dataframe=True)


def filter_by_date(df, start_date, end_date=None):
    """
    按日期过滤数据
    
    Args:
        df: DataFrame，原始数据
        start_date: 开始日期字符串 'YYYY-MM-DD'
        end_date: 结束日期字符串 'YYYY-MM-DD'，默认今天
        
    Returns:
        DataFrame: 过滤后的数据
    """
    if df.empty:
        return df

    end_date = end_date or datetime.now().strftime('%Y-%m-%d')

    # 转换为字符串比较（避免 Timestamp 类型错误）
    df['trade_date_str'] = pd.to_datetime(df['trade_date']).dt.strftime('%Y-%m-%d')
    mask = (df['trade_date_str'] >= start_date) & (df['trade_date_str'] <= end_date)
    result = df[mask].copy()
    result.drop('trade_date_str', axis=1, inplace=True)

    return result


def format_numeric_columns(df):
    """
    格式化数值列为两位小数
    
    Args:
        df: DataFrame
        
    Returns:
        DataFrame: 格式化后的数据（原地修改）
    """
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_columns:
        df[col] = df[col].apply(lambda x: round(x, 2) if pd.notna(x) else x)
    return df


def save_to_csv(df, code, data_dir=None):
    """
    保存数据到 CSV 文件
    
    Args:
        df: DataFrame，要保存的数据
        code: 股票代码
        data_dir: 数据保存目录，默认在 tickflowDir/data/single_stock/{code}
    """
    if data_dir is None:
        data_dir = get_default_data_dir(code)

    # 格式化数值
    format_numeric_columns(df)

    # 保存
    generate_csv(df, f'{code}_1d_line', specific_folder=data_dir)
    print(f"✓ 已保存 {len(df)} 条记录到：{data_dir}")


def get_default_data_dir(code):
    """
    获取默认数据目录
    
    Args:
        code: 股票代码
        
    Returns:
        str: 数据目录路径
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tickflow_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(tickflow_dir, 'data', 'single_stock', code)
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def cleanup_old_files(data_dir, code, keep_count=2):
    """
    清理旧文件，只保留最新的 keep_count 个
    
    Args:
        data_dir: 数据目录
        code: 股票代码
        keep_count: 保留文件数量，默认 2 个
    """
    csv_files = [f for f in os.listdir(data_dir)
                 if f.endswith('.csv') and code in f]

    if len(csv_files) > keep_count:
        print(f"发现 {len(csv_files)} 个 CSV 文件，开始清理...")
        csv_files.sort(reverse=True)
        files_to_delete = csv_files[keep_count:]

        for file in files_to_delete:
            try:
                os.remove(os.path.join(data_dir, file))
                print(f"✓ 删除旧文件：{file}")
            except Exception as e:
                print(f"删除文件失败 {file}: {e}")

        print(f"✓ 清理完成，保留 {keep_count} 个文件")


def find_latest_csv(data_dir, code):
    """
    查找目录下最新的 CSV 文件
    
    Args:
        data_dir: 数据目录
        code: 股票代码
        
    Returns:
        tuple: (最新文件路径，CSV 文件列表) 或 (None, [])
    """
    csv_files = [f for f in os.listdir(data_dir)
                 if f.endswith('.csv') and code in f]

    if not csv_files:
        return None, []

    csv_files.sort(reverse=True)
    latest_file = os.path.join(data_dir, csv_files[0])

    return latest_file, csv_files


def get_last_update_date(data_dir, code):
    """
    获取某只股票上次更新的日期（从现有文件中读取）
    
    Args:
        data_dir: 数据目录
        code: 股票代码
        
    Returns:
        str: 最新日期字符串 'YYYY-MM-DD'，如果没有文件则返回 None
    """
    latest_file, _ = find_latest_csv(data_dir, code)

    if latest_file is None:
        return None

    df = pd.read_csv(latest_file)
    if df.empty or 'trade_date' not in df.columns:
        return None

    return df['trade_date'].max()


# ============================================================
# 类 - 封装完整流程，提供高级 API
# ============================================================

class SingleKlineFetcher:

    def __init__(self, api_key=None):
        """
        初始化股票 K 线获取器
        
        Args:
            api_key: TickFlow API 密钥，默认使用内置密钥
        """
        self.api_key = api_key or "tk_70e08101458040caa8fe082bf28587ac"

    def fetch(self, code, start_date=None, end_date=None, count=10000,
              period="1d", adjust='forward_additive', save=True,
              data_dir=None, incremental=False, cleanup=True):
        """
        获取 K 线数据并可选保存到 CSV
        
        Args:
            code: 股票代码
            start_date: 开始日期 'YYYY-MM-DD'，用于增量更新
            end_date: 结束日期 'YYYY-MM-DD'，默认今天
            count: 获取数据条数，默认 10000
            period: K 线周期，默认 '1d'
            adjust: 复权类型，默认 'forward_additive'
            save: 是否保存，默认 True
            data_dir: 数据目录，默认使用默认目录
            incremental: 是否启用增量更新，默认 False
            cleanup: 是否清理旧文件，默认 True
            
        Returns:
            DataFrame: K 线数据
        """
        # 如果是增量更新，自动获取上次更新日期
        if incremental and start_date is None:
            if data_dir is None:
                data_dir = get_default_data_dir(code)
            start_date = get_last_update_date(data_dir, code)

            if start_date is None:
                print("未找到历史数据，将执行全量获取")
                incremental = False
            else:
                # 从下次日开始
                last_date = datetime.strptime(start_date, '%Y-%m-%d')
                start_date = (last_date + timedelta(days=1)).strftime('%Y-%m-%d')

        # 获取数据
        df = get_kline_data(code, self.api_key, count, period, adjust)

        # 日期过滤
        if start_date:
            df = filter_by_date(df, start_date, end_date)
            print(f"过滤后剩余 {len(df)} 条记录")

        # 保存数据
        if save:
            if data_dir is None:
                data_dir = get_default_data_dir(code)

            if incremental:
                # 增量更新模式：追加到现有文件
                self._save_incremental(df, code, data_dir)
            else:
                # 全量模式：新文件
                save_to_csv(df, code, data_dir)

            # 清理旧文件
            if cleanup and incremental:
                cleanup_old_files(data_dir, code, keep_count=2)

        return df

    @staticmethod
    def _save_incremental(df_new, code, data_dir):
        """
        增量保存：合并现有数据和新数据
        
        Args:
            df_new: 新获取的数据
            code: 股票代码
            data_dir: 数据目录
        """
        latest_file, _ = find_latest_csv(data_dir, code)

        if latest_file is None:
            # 没有现有文件，直接保存
            save_to_csv(df_new, code, data_dir)
            return

        # 读取现有数据
        df_existing = pd.read_csv(latest_file)

        # 合并数据
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_sorted = df_combined.sort_values('trade_date').reset_index(drop=True)

        # 去重（防止重复数据）
        df_unique = df_sorted.drop_duplicates(subset=['trade_date'], keep='last')

        # 格式化并保存
        format_numeric_columns(df_unique)
        df_unique.to_csv(latest_file, index=False)

        print(f"✓ 已追加 {len(df_new)} 条记录到：{latest_file}")
