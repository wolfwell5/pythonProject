"""
批量股票 K 线数据获取器

功能：
1. 批量获取多只股票的 K 线数据
2. 自动为每只股票生成独立的 CSV 文件
3. 支持增量更新模式
4. 支持请求间隔控制（避免被封 IP）
5. 复用 SingleKlineFetcher 的工具函数和类
"""

import os
import random
import sys
import time

import pandas as pd

# 添加 stock 目录到 Python 路径
script_dir = os.path.dirname(os.path.abspath(__file__))
stock_dir = os.path.dirname(os.path.dirname(script_dir))
sys.path.insert(0, stock_dir)

from tickflowDir.scripts.SingleKlineFetcher import (
    SingleKlineFetcher,
    get_default_data_dir
)


def load_stock_codes_from_csv():
    """
    从 CSV 文件加载股票代码列表
    
    Returns:
        list: 股票代码列表，如果文件不存在或为空则返回 None
    """
    # CSV 文件路径（由 extract_stock_codes.py 生成）
    csv_path = os.path.join(
        os.path.dirname(script_dir),  # tickflowDir 目录
        'data',
        'basic_info',
        'all_stock_codes.csv'
    )
    
    if not os.path.exists(csv_path):
        print(f"错误：CSV 文件不存在：{csv_path}")
        print("请先运行：python stock/tickflowDir/extract_stock_codes.py")
        return None
    
    print(f"读取文件：{csv_path}")
    
    # 读取 CSV 文件
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    
    # 提取股票代码列
    all_stock_codes = df['股票代码'].tolist()
    
    if not all_stock_codes:
        print("错误：未找到任何股票代码！")
        return None
    
    print(f"总计读取到 {len(all_stock_codes)} 个股票代码")
    
    return all_stock_codes


class BatchKlineFetcher:
    """
    批量股票 K 线数据获取器
    
    示例:
        >>> batch = BatchKlineFetcher()
        >>> 
        >>> # 方式 1：使用股票代码列表
        >>> codes = ["300164.SZ", "600000.SH", "000001.SZ"]
        >>> results = batch.fetch_batch(codes)
        >>> 
        >>> # 方式 2：从文件读取股票代码
        >>> results = batch.fetch_from_file("stocks.txt")
    """
    
    def __init__(self, api_key=None, delay_range=(2, 4)):
        """
        初始化批量获取器
        
        Args:
            api_key: TickFlow API 密钥，默认使用内置密钥
            delay_range: 请求间隔随机延迟范围（秒），如 (2, 4) 表示 2-4 秒随机延迟
        """
        self.api_key = api_key or "tk_70e08101458040caa8fe082bf28587ac"
        self.delay_range = delay_range
        self.fetcher = SingleKlineFetcher(self.api_key)
        
        # 统计信息
        self.success_count = 0
        self.fail_count = 0
        self.total_count = 0
    
    def fetch_batch(self, stock_codes, incremental=True, count=10000):
        """
        批量获取股票 K 线数据
        
        Args:
            stock_codes: 股票代码列表，如 ['300164.SZ', '600000.SH']
            incremental: 是否启用增量更新，默认 True
            count: 每只股票获取的数据条数，默认 10000
            
        Returns:
            dict: {股票代码：DataFrame} 成功获取的数据，失败的为 None
        """
        results = {}
        self.total_count = len(stock_codes)
        self.success_count = 0
        self.fail_count = 0
        
        print("=" * 70)
        print(f"开始批量获取 {self.total_count} 只股票的 K 线数据")
        print(f"增量更新模式：{'启用' if incremental else '禁用'}")
        print(f"请求间隔：{self.delay_range[0]}-{self.delay_range[1]} 秒")
        print("=" * 70)
        
        for idx, code in enumerate(stock_codes, 1):
            try:
                print(f"\n[{idx}/{self.total_count}] 正在处理：{code}")
                
                # 调用 SingleKlineFetcher
                df = self.fetcher.fetch(
                    code=code,
                    count=count,
                    incremental=incremental,
                    save=True
                )
                
                results[code] = df
                
                if df is not None and not df.empty:
                    self.success_count += 1
                    print(f"✓ 完成：{code}，共 {len(df)} 条记录")
                else:
                    self.fail_count += 1
                    print(f"✗ 失败：{code}，返回空数据")
                
                # 添加延迟，避免请求过快（最后一只股票不需要延迟）
                if idx < self.total_count:
                    delay = self._random_delay()
                    print(f"等待 {delay:.1f} 秒...")
                    time.sleep(delay)
                    
            except Exception as e:
                self.fail_count += 1
                print(f"✗ 异常：{code}，错误：{str(e)}")
                results[code] = None
        
        # 打印汇总报告
        self._print_summary()
        
        return results
    
    def fetch_from_file(self, file_path, incremental=True, count=10000):
        """
        从文件读取股票代码并批量获取
        
        Args:
            file_path: 股票代码文件路径，每行一个股票代码
            incremental: 是否启用增量更新
            count: 每只股票获取的数据条数
            
        Returns:
            dict: 获取结果
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在：{file_path}")
        
        # 读取股票代码
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 清理股票代码（去除空白字符和注释）
        stock_codes = []
        for line in lines:
            line = line.strip()
            # 跳过空行和注释
            if line and not line.startswith('#'):
                stock_codes.append(line)
        
        print(f"从文件读取到 {len(stock_codes)} 个股票代码")
        
        return self.fetch_batch(stock_codes, incremental, count)
    
    def _random_delay(self):
        """生成随机延迟"""
        return random.uniform(*self.delay_range)
    
    def _print_summary(self):
        """打印汇总报告"""
        print("\n" + "=" * 70)
        print("批量获取完成！")
        print("=" * 70)
        print(f"总数：{self.total_count}")
        print(f"成功：{self.success_count} ✓")
        print(f"失败：{self.fail_count} ✗")
        print(f"成功率：{self.success_count / self.total_count * 100:.1f}%")
        print("=" * 70)


def init_all_stocks_day_kline():
    """基础使用示例 - 从 CSV 文件读取股票代码并全量更新"""
    print("\n" + "=" * 70)
    print("示例：从 CSV 文件读取股票代码并全量更新")
    print("=" * 70)
    
    # 加载股票代码
    all_stock_codes = load_stock_codes_from_csv()
    
    if all_stock_codes is None:
        print("错误：未找到任何股票代码！")
        return
    
    batch = BatchKlineFetcher(delay_range=(6, 6))
    
    # 批量全量获取
    results = batch.fetch_batch(
        all_stock_codes,
        incremental=False,  # 全量更新
        count=10000  # 获取全部历史数据
    )
    
    # 查看结果
    print("\n结果摘要:")
    for code, df_result in results.items():
        if df_result is not None and not df_result.empty:
            data_dir = get_default_data_dir(code)
            csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
            print(f"{code}: {len(df_result)} 条记录，CSV 文件数：{len(csv_files)}")


def incremental_update():
    """增量更新示例"""
    print("\n" + "=" * 70)
    print("示例：增量更新")
    print("=" * 70)
    
    batch = BatchKlineFetcher(delay_range=(6, 6))
    
    # 只对特定股票进行增量更新
    # stock_codes = ["300164.SZ"]
    all_stock_codes = load_stock_codes_from_csv()

    batch.fetch_batch(
        all_stock_codes,
        incremental=True,  # 启用增量更新
        count=20  # 只获取最近 100 天
    )


def example_custom_stock_list():
    """自定义股票列表示例"""
    print("\n" + "=" * 70)
    print("示例：自定义股票池")
    print("=" * 70)
    
    # 可以定义自己的股票池
    my_stocks = [
        # 石油板块
        "300164.SZ",  # 通源石油
        "600028.SH",  # 石化油服
        
        # 银行板块
        "600000.SH",  # 浦发银行
        "601398.SH",  # 工商银行
        
        # 科技板块
        "000001.SZ",  # 平安银行
        "002594.SZ",  # 比亚迪
    ]
    
    batch = BatchKlineFetcher(delay_range=(1, 2))
    results = batch.fetch_batch(my_stocks, incremental=True)


if __name__ == '__main__':
    # 运行示例
    
    # 示例 1：全量更新
    init_all_stocks_day_kline()
    
    # 示例 2：增量更新
    # incremental_update()
    
    # 示例 3：自定义股票池
    # example_custom_stock_list()
    
    print(f"\n所有示例运行完成！, 结束时间： {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
    print("\n提示：")
    print("1. 修改 delay_range 可以调整请求间隔")
    print("2. 设置 incremental=False 可以强制全量更新")
    print("3. CSV 文件保存在：tickflowDir/data/single_stock/{股票代码}/")
