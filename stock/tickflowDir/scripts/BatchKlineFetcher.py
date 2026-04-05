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
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import pandas as pd

# 添加 stock 目录到 Python 路径
script_dir = os.path.dirname(os.path.abspath(__file__))
stock_dir = os.path.dirname(os.path.dirname(script_dir))
sys.path.insert(0, stock_dir)

from tickflowDir.scripts.SingleKlineFetcher import (
    SingleKlineFetcher,
)


def load_stock_codes_from_csv():
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


def _get_log_dir():
    """
    获取日志文件目录

    Returns:
        str: 日志目录路径
    """
    log_dir = os.path.join(
        os.path.dirname(script_dir),
        'logs'
    )
    # 自动创建日志目录
    os.makedirs(log_dir, exist_ok=True)
    return log_dir


class BatchKlineFetcher:

    def __init__(self, api_keys=None, delay_range=(6, 6)):
        """
        初始化批量获取器
        
        Args:
            api_keys: TickFlow API 密钥列表，如 ["key1", "key2"]，默认使用内置密钥
            delay_range: 请求间隔随机延迟范围（秒），如 (2, 4) 表示 2-4 秒随机延迟
        """
        # 支持单个 key 或 key 列表
        if api_keys is None:
            self.api_keys = ["tk_70e08101458040caa8fe082bf28587ac"]
        elif isinstance(api_keys, str):
            self.api_keys = [api_keys]
        else:
            self.api_keys = api_keys

        self.delay_range = delay_range

        # API key 轮询索引
        self._api_key_index = 0

        # 为每个 API key 预创建 SingleKlineFetcher 实例（避免重复创建）
        self._fetchers = {}
        for idx, key in enumerate(self.api_keys):
            self._fetchers[key] = SingleKlineFetcher(key)

        # 统计信息
        self.success_count = 0
        self.fail_count = 0
        self.no_update_count = 0  # 日期为最新，无需更新
        self.total_count = 0

        # 失败详情记录
        self.failed_codes = []  # [(code, error_msg), ...]

    def _get_next_api_key(self):
        api_key = self.api_keys[self._api_key_index % len(self.api_keys)]
        self._api_key_index += 1
        return api_key

    def _random_delay(self):
        return random.uniform(*self.delay_range)

    def generate_log_file(self, exec_start_time=None, exec_end_time=None, exec_duration=None):
        """
        生成日志文件

        Args:
            exec_start_time: 开始执行时间 (datetime)
            exec_end_time: 结束执行时间 (datetime)
            exec_duration: 总计耗时 (秒)

        Returns:
            str: 日志文件路径
        """
        # 获取日志目录
        log_dir = _get_log_dir()

        # 生成带时间戳的日志文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(log_dir, f'batch_fetch_{timestamp}.log')

        # 写入日志内容
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("批量获取股票 K 线数据 - 执行报告\n")
            f.write("=" * 70 + "\n")
            f.write(f"执行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"API Key 数量：{len(self.api_keys)}\n")
            f.write(f"请求间隔：{self.delay_range[0]}-{self.delay_range[1]} 秒\n")
            f.write("=" * 70 + "\n\n")

            # 执行时间信息
            if exec_start_time and exec_end_time and exec_duration is not None:
                f.write("执行时间详情:\n")
                f.write("-" * 70 + "\n")
                f.write(f"开始执行时间：{exec_start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"结束执行时间：{exec_end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"总计耗时：{exec_duration:.2f} 秒, 折合{exec_duration / 60:.2f} 分钟")
                f.write(f"平均速度：{self.total_count / exec_duration:.1f} 只/秒\n")
                f.write("-" * 70 + "\n\n")

            f.write("统计信息:\n")
            f.write("-" * 70 + "\n")
            f.write(f"总数：{self.total_count}\n")
            f.write(f"成功：{self.success_count}\n")
            if self.no_update_count > 0:
                f.write(f"无需更新：{self.no_update_count}\n")
            f.write(f"失败：{self.fail_count}\n")
            if self.total_count > 0:
                success_rate = self.success_count / self.total_count * 100
                f.write(f"成功率：{success_rate:.1f}%\n")
            f.write("-" * 70 + "\n\n")

            # 打印失败详情
            if self.failed_codes:
                f.write("失败详情:\n")
                f.write("-" * 70 + "\n")
                f.write(f"{'序号':<6} {'股票代码':<12} {'失败原因'}\n")
                f.write("-" * 70 + "\n")
                for idx, (code, error_msg) in enumerate(self.failed_codes, 1):
                    f.write(f"{idx:<6} {code:<12} {error_msg}\n")
                f.write("-" * 70 + "\n")
                f.write(f"共计 {len(self.failed_codes)} 只股票失败\n")

            f.write("=" * 70 + "\n")
            f.write("CSV 文件保存在：tickflowDir/data/single_stock/{股票代码}/\n")
            f.write("=" * 70 + "\n")

        return log_file

    def _single_thread_fetch(self, code, incremental, count, api_key=None):
        """
        单只股票获取方法（用于多线程调用）
        
        Args:
            code: 股票代码
            incremental: 是否增量更新
            count: 获取数据条数
            api_key: 指定使用的 API key
            
        Returns:
            tuple: (股票代码，DataFrame, status, error_msg)
                   status: 'success' | 'empty_no_update' | 'failed'
                   error_msg: 错误信息（失败时）或 None（成功时）
        """
        # 使用预创建的 fetcher 实例（避免重复创建）
        thread_fetcher = self._fetchers.get(api_key)
        if thread_fetcher is None:
            # 如果没有预创建，则临时创建一个
            thread_fetcher = SingleKlineFetcher(api_key)

        try:
            # 添加延迟，避免请求过快
            delay = self._random_delay()
            time.sleep(delay)

            df = thread_fetcher.fetch(
                code=code,
                count=count,
                incremental=incremental,
                save=True
            )

            # 判断状态
            if df is not None and not df.empty:
                return code, df, 'success', None
            elif incremental and df is not None and df.empty:
                # 增量更新返回空数据，说明日期为最新，无需更新
                return code, df, 'empty_no_update', None
            else:
                # 其他情况返回空数据，视为失败
                error_msg = "API 返回空数据"
                return code, None, 'failed', error_msg
        except Exception as e:
            error_msg = str(e)
            print(f"✗ 异常：{code}，错误：{error_msg}")
            return code, None, 'failed', error_msg

    def fetch_batch_multithread(self, stock_codes, incremental=True, count=10000, max_workers=2):
        """
        多线程并行批量获取股票 K 线数据
        
        Args:
            stock_codes: 股票代码列表
            incremental: 是否启用增量更新
            count: 每只股票获取的数据条数
            max_workers: 最大线程数，默认 2
            
        Returns:
            dict: {股票代码：DataFrame} 成功获取的数据
        """
        results = {}
        self.total_count = len(stock_codes)
        self.success_count = 0
        self.fail_count = 0
        self.no_update_count = 0

        print("=" * 70)
        print(f"开始多线程批量获取 {self.total_count} 只股票的 K 线数据")
        print(f"增量更新模式：{'启用' if incremental else '禁用'}")
        print(f"线程数：{max_workers}")
        print(f"API Key 数量：{len(self.api_keys)}")
        print(f"请求间隔：{self.delay_range[0]}-{self.delay_range[1]} 秒")
        print("=" * 70)
        stock_code_groups = [[] for _ in range(max_workers)]
        for idx, code in enumerate(stock_codes):
            thread_idx = idx % max_workers
            stock_code_groups[thread_idx].append(code)

        print(f"\n任务分配:")
        for i, codes in enumerate(stock_code_groups):
            print(f"  线程 {i + 1}: {len(codes)} 只股票")
        print()

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 为每个线程提交一批股票
            future_to_code = {}

            # 快速提交所有任务到线程池（不延迟）
            for code in stock_codes:
                # 每个请求轮换 API key（避免同一 IP 频繁请求）
                api_key = self._get_next_api_key()

                future = executor.submit(
                    self._single_thread_fetch,
                    code,
                    incremental,
                    count,
                    api_key  # 传入指定的 API key
                )
                future_to_code[future] = code
            # 处理完成的任务
            completed = 0
            for future in as_completed(future_to_code):
                completed += 1
                code = future_to_code[future]

                try:
                    code_result, df, status, error_msg = future.result()
                    results[code] = df

                    if status == 'success':
                        self.success_count += 1
                        print(f"[{completed}/{self.total_count}] ✓ 完成：{code}，共 {len(df)} 条记录")
                    elif status == 'empty_no_update':
                        self.no_update_count += 1
                        print(f"[{completed}/{self.total_count}] ⊘ 跳过：{code}，日期为最新，无需更新")
                    else:  # failed
                        self.fail_count += 1
                        self.failed_codes.append((code_result, error_msg))  # 使用实际的 code_result
                        print(f"[{completed}/{self.total_count}] ✗ 失败：{code_result}，{error_msg}")

                except Exception as e:
                    self.fail_count += 1
                    error_msg = str(e)
                    self.failed_codes.append((code, error_msg))  # 使用 code 变量
                    print(f"[{completed}/{self.total_count}] ✗ 异常：{code}，错误：{error_msg}")
                    results[code] = None

        return results


def incremental_update_multithread():
    """增量更新示例 - 多线程版本"""
    print("\n" + "=" * 70)
    print("示例：增量更新（多线程并行）")
    print("=" * 70)

    # 记录开始时间
    func_start_time = datetime.now()

    # 定义 4 个不同的 API key
    api_keys = [
        "tk_70e08101458040caa8fe082bf28587ac",  # API Key 1
        "tk_b05eb63de7d442d49a836d717f93b69b",  # API Key 2
        'tk_b655f2d64511468c9b9a5cf62315d1ef',
        "tk_2a3fc59f9c1341e69c4b9fcd9dec9b61",
        'tk_5ea1d5bbce4a478faad1ec5a92c7fc94',
        'tk_1e671c5ca3934f16b63561d40f3119d5',
        "tk_fca640b707cc4fe49ae998f2deec8527",
        'tk_438fcddc60d24641859f2cdf18e4755f',
        'tk_909d86a1e4464cef8a7f025d90ba9069',
    ]

    batch = BatchKlineFetcher(
        api_keys=api_keys,  # 使用多个 API key
    )

    # 从 CSV 文件读取所有股票代码
    all_stock_codes = load_stock_codes_from_csv()
    # all_stock_codes = load_stock_codes_from_csv()[:50]

    if all_stock_codes is None:
        print("错误：未找到任何股票代码！")
        return

    # 使用多线程并行获取（每个线程使用不同的 API key）
    batch.fetch_batch_multithread(
        all_stock_codes,
        incremental=True,  # 启用增量更新
        count=20,  # 获取最近 20 天数据
        max_workers=len(api_keys)  # 9 个线程
    )

    # batch.fetch_batch_multithread(
    #     all_stock_codes,
    #     incremental=False,  # 全量模式
    #     count=10000
    # )

    # 记录结束时间并生成日志
    func_end_time = datetime.now()
    func_duration = (func_end_time - func_start_time).total_seconds()

    # 生成带执行时间的日志文件
    log_file = batch.generate_log_file(
        exec_start_time=func_start_time,
        exec_end_time=func_end_time,
        exec_duration=func_duration
    )
    print(f"\n日志文件已生成：{log_file}")


if __name__ == '__main__':
    # 增量更新（多线程并行）- 推荐
    start_time = datetime.now()
    incremental_update_multithread()
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print(f"\n开始执行时间：{start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"结束执行时间：{end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"总计耗时：{duration:.2f} 秒, 折合{duration / 60:.2f} 分钟")
    print("CSV 文件保存在：tickflowDir/data/single_stock/{股票代码}/")
