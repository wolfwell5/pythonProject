"""
对比 akShare 和 Tickflow 的股票数据
找出缺失的股票代码和名称
"""
import json
import csv
import os
import glob
import re
from pathlib import Path
from datetime import datetime


def get_latest_akshare_csv(directory):
    """获取目录下日期最新的 akShare CSV 文件"""
    pattern = os.path.join(directory, '2026-*_stocks.csv')
    csv_files = glob.glob(pattern)
    
    if not csv_files:
        raise FileNotFoundError(f"在 {directory} 目录下未找到匹配的 CSV 文件")
    
    # 从文件名中提取日期并排序
    def extract_date(filepath):
        filename = os.path.basename(filepath)
        match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
        if match:
            return datetime.strptime(match.group(1), '%Y-%m-%d')
        return datetime.min
    
    # 按日期排序，返回最新的文件
    latest_file = max(csv_files, key=extract_date)
    return latest_file


def load_akshare_stocks(csv_file):
    """加载 akShare 的股票数据"""
    stocks = {}
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            code = row['code'].strip()
            name = row['name'].strip()
            stocks[code] = name
    return stocks


def load_tickflow_stocks(json_dir):
    """加载 Tickflow 的股票数据（从所有 JSON 文件中）"""
    stocks = {}
    
    # 遍历目录下所有 JSON 文件
    for file in Path(json_dir).glob('*.json'):
        if 'not sort' in file.name:  # 跳过未排序的文件
            continue
            
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if 'data' in data and isinstance(data['data'], list):
                for item in data['data']:
                    code = item.get('code', '').strip()
                    name = item.get('name', '').strip()
                    if code:  # 确保代码不为空
                        stocks[code] = name
                        
        except Exception as e:
            print(f"读取文件 {file.name} 时出错：{e}")
    
    return stocks


def compare_stocks(akshare_stocks, tickflow_stocks):
    """对比两个数据源"""
    akshare_codes = set(akshare_stocks.keys())
    tickflow_codes = set(tickflow_stocks.keys())
    
    # 找出在 akShare 中存在但在 Tickflow 中不存在的股票
    missing_in_tickflow = akshare_codes - tickflow_codes
    
    # 找出在 Tickflow 中存在但在 akShare 中不存在的股票
    missing_in_akshare = tickflow_codes - akshare_codes
    
    # 找出代码相同但名称不同的股票
    name_differs = {}
    common_codes = akshare_codes & tickflow_codes
    for code in common_codes:
        if akshare_stocks[code] != tickflow_stocks[code]:
            name_differs[code] = {
                'akshare': akshare_stocks[code],
                'tickflow': tickflow_stocks[code]
            }
    
    return missing_in_tickflow, missing_in_akshare, name_differs


def save_missing_stocks(missing_codes, all_stocks, output_file):
    """保存缺失的股票列表到 CSV"""
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['code', 'name'])
        for code in sorted(missing_codes):
            writer.writerow([code, all_stocks[code]])


def main():
    # 文件路径
    akshare_dir = r'/akShare/data/basic_info/stocks'
    tickflow_dir = r'/tickflowDir/data/basic_info/stocks'
    output_dir = r'/tickflowDir/data/stock_comparison_result'
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("开始对比股票数据...")
    print("=" * 60)
    
    # 1. 加载 akShare 数据（自动获取最新CSV）
    akshare_csv = get_latest_akshare_csv(akshare_dir)
    print(f"\n1. 加载 akShare 数据：{akshare_csv}")
    akshare_stocks = load_akshare_stocks(akshare_csv)
    print(f"   ✓ akShare 共有 {len(akshare_stocks)} 只股票")
    
    # 2. 加载 Tickflow 数据
    print(f"\n2. 加载 Tickflow 数据：{tickflow_dir}")
    tickflow_stocks = load_tickflow_stocks(tickflow_dir)
    print(f"   ✓ Tickflow 共有 {len(tickflow_stocks)} 只股票")
    
    # 3. 对比数据
    print("\n3. 对比分析...")
    missing_in_tickflow, missing_in_akshare, name_differs = compare_stocks(
        akshare_stocks, tickflow_stocks
    )
    
    # 4. 输出结果
    print("\n" + "=" * 60)
    print("对比结果:")
    print("=" * 60)
    
    print(f"\n📊 统计信息:")
    print(f"   - akShare 有但 Tickflow 缺失：{len(missing_in_tickflow)} 只")
    print(f"   - Tickflow 有但 akShare 缺失：{len(missing_in_akshare)} 只")
    print(f"   - 代码相同但名称不同：{len(name_differs)} 只")
    
    # 5. 保存缺失的股票
    if missing_in_tickflow:
        output_file = os.path.join(output_dir, 'missing_in_tickflow.csv')
        save_missing_stocks(missing_in_tickflow, akshare_stocks, output_file)
        print(f"\n❌ Tickflow 缺失的股票已保存到：{output_file}")
        
        # 显示前 20 只缺失的股票
        print(f"\n   前 20 只缺失的股票:")
        for i, code in enumerate(sorted(missing_in_tickflow)[:20]):
            print(f"      {i+1}. {code} - {akshare_stocks[code]}")
        if len(missing_in_tickflow) > 20:
            print(f"      ... 还有 {len(missing_in_tickflow) - 20} 只")
    
    if missing_in_akshare:
        output_file = os.path.join(output_dir, 'missing_in_akshare.csv')
        save_missing_stocks(missing_in_akshare, tickflow_stocks, output_file)
        print(f"\n⚠️  akShare 缺失的股票已保存到：{output_file}")
    
    if name_differs:
        # 保存名称不同的股票
        output_file = os.path.join(output_dir, 'name_differs.csv')
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['code', 'akshare_name', 'tickflow_name'])
            for code in sorted(name_differs.keys()):
                writer.writerow([
                    code, 
                    name_differs[code]['akshare'], 
                    name_differs[code]['tickflow']
                ])
        print(f"\n🔄 名称不同的股票已保存到：{output_file}")
        
        # 显示前 10 只名称不同的股票
        print(f"\n   前 10 只名称不同的股票:")
        for i, (code, names) in enumerate(list(name_differs.items())[:10]):
            print(f"      {i+1}. {code}")
            print(f"         akShare:  {names['akshare']}")
            print(f"         Tickflow: {names['tickflow']}")
    
    print("\n" + "=" * 60)
    print("对比完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
