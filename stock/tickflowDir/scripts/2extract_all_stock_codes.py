"""
从 JSON 文件提取所有股票代码和名称，生成 CSV 文件

功能：
1. 读取 SH/SZ/BJ 三个 JSON 文件
2. 提取股票代码和名称
3. 生成 all_stock_codes.csv 文件
"""

import os
import json
import pandas as pd


def extract_stock_codes_from_json():
    """
    从三个交易所的 JSON 文件中提取股票代码和名称
    
    Returns:
        list: 包含 (code, name) 元组的列表
    """
    # JSON 文件所在目录
    json_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '../data',
        'basic_info',
        'stocks'
    )
    
    # 三个交易所的 JSON 文件
    json_files = [
        os.path.join(json_dir, '1_SH_stocks.json'),
        os.path.join(json_dir, '2_SZ_stocks.json'),
        os.path.join(json_dir, '3_BJ_stocks.json'),
    ]
    
    all_stocks = []
    
    for file_path in json_files:
        if not os.path.exists(file_path):
            print(f"⚠ 文件不存在：{file_path}")
            continue
        
        print(f"读取文件：{file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 提取股票代码和名称
        stocks_count = 0
        for stock in data.get('data', []):
            symbol = stock.get('symbol', '')
            name = stock.get('name', '')
            
            if symbol and name:
                all_stocks.append({
                    '股票代码': symbol,
                    '股票名称': name
                })
                stocks_count += 1
        
        print(f"  ✓ 从 {os.path.basename(file_path)} 提取到 {stocks_count} 个股票")
    
    return all_stocks


def save_to_csv(stocks, output_path):
    """
    保存股票数据到 CSV 文件
    
    Args:
        stocks: 股票数据列表
        output_path: 输出 CSV 文件路径
    """
    df = pd.DataFrame(stocks)
    
    # 按股票代码排序
    df = df.sort_values('股票代码').reset_index(drop=True)
    
    # 保存到 CSV
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print(f"\n✓ 成功保存 {len(df)} 个股票到：{output_path}")
    return df


def main():
    """主函数"""
    print("=" * 70)
    print("开始提取股票代码...")
    print("=" * 70)
    
    # 提取股票代码
    all_stocks = extract_stock_codes_from_json()
    
    if not all_stocks:
        print("\n错误：未提取到任何股票代码！")
        return
    
    # 去重
    unique_stocks = []
    seen_codes = set()
    for stock in all_stocks:
        code = stock['股票代码']
        if code not in seen_codes:
            unique_stocks.append(stock)
            seen_codes.add(code)
    
    print(f"\n去重后总计：{len(unique_stocks)} 个唯一的股票代码")
    
    # 输出路径
    output_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '../data',
        'basic_info'
    )
    
    # 确保目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'all_stock_codes.csv')
    
    # 保存到 CSV
    df = save_to_csv(unique_stocks, output_path)
    
    # 显示前几行和后几行
    print("\n前 5 行数据:")
    print(df.head())
    print("\n后 5 行数据:")
    print(df.tail())
    
    print("\n" + "=" * 70)
    print("完成！")
    print("=" * 70)


if __name__ == '__main__':
    main()
