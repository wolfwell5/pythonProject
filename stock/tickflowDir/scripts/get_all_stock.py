from time import sleep

import requests
import json
import os

# API 配置
base_url = 'https://api.tickflow.org/v1/exchanges/{exchange}/instruments'
headers = {
    'x-api-key': 'tk_70e08101458040caa8fe082bf28587ac'
}
market_list = [
    'SH',
    'SZ',
    'BJ',
    'HK',
]


def filter_and_sort_stocks(stock_data):
    """
    筛选股票数据并排序：
    1. 只保留 type 为 stock 的数据。去除 etf，index 2 种类型的，暂不需要
    2. 按照 code 升序排序
    
    Args:
        stock_data: 原始股票数据（包含 data, count 等字段）
    
    Returns:
        dict: 处理后的数据，包含 data, count, real_count 字段
    """
    
    if 'data' in stock_data and isinstance(stock_data['data'], list):
        # 1. 过滤：只保留 type 为 stock 的数据
        stocks_only = [item for item in stock_data['data'] if item.get('type') == 'stock']
        
        # 2. 排序：按照 code 升序排序
        stocks_only.sort(key=lambda x: x.get('code', ''))
        
        # 3. 构建返回结果
        return {
            # 保留原始数据的其他字段（除了 data 和 count）
            **{k: v for k, v in stock_data.items() if k not in ['data', 'count']},
            'count': stock_data.get('count'),      # 原始总数
            'real_count': len(stocks_only),        # 过滤后的真实股票数量
            'data': stocks_only,                   # 过滤并排序后的股票列表
        }
    
    return stock_data


try:
    for idx, market in enumerate(market_list, 1):
        print(f"[{idx}/{len(market_list)}] 正在获取 {market} 市场数据...")

        # 构建当前市场的 URL
        request_url = base_url.format(exchange=market)

        # 获取所有 A 股代码与名称的映射
        raw_stock_list = requests.get(request_url, headers=headers).json()
                
        # 筛选并排序，返回完整的结果
        stock_list = filter_and_sort_stocks(raw_stock_list)

        # 动态获取当前脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # 数据保存到上级目录的 data 文件夹
        data_dir = os.path.join(os.path.dirname(script_dir), 'data')
        stocks_dir = os.path.join(data_dir, 'basic_info', 'stocks')

        # 确保目录存在
        os.makedirs(stocks_dir, exist_ok=True)

        output_file = os.path.join(stocks_dir, f'{idx}_{market}_stocks.json')

        # 保存到 JSON 文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(stock_list, f, ensure_ascii=False, indent=2)

        print(f"✓ 已保存到：{output_file}")
        sleep(3)

except requests.exceptions.RequestException as e:
    print(f"✗ 请求失败：{e}")
except json.JSONDecodeError as e:
    print(f"✗ JSON 解析失败：{e}")
except Exception as e:
    print(f"✗ 发生错误：{e}")
