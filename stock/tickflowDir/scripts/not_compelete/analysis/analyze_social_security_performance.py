"""
分析社保基金进入十大流通股东后的股票表现

统计社保基金首次出现在某只股票十大流通股东后，
该股票在 3 个月、半年、1 年后的涨跌幅情况
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import akshare as ak


def load_all_holders_data(data_dir):
    """加载所有报告期的股东数据"""
    all_data = []
    
    # 读取所有 CSV 文件
    csv_files = sorted(Path(data_dir).glob('*_holders.csv'))
    
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            # 提取报告期
            report_date = file.stem.split('_')[-1]  # 如 20241231
            df['数据来源文件'] = file.name
            df['报告期'] = report_date
            all_data.append(df)
            print(f"✓ 加载 {file.name}: {len(df)} 条记录")
        except Exception as e:
            print(f"✗ 加载失败 {file.name}: {e}")
    
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return pd.DataFrame()


def find_social_security_entries(holders_df):
    """
    找出社保基金进入十大流通股东的记录
    
    Returns:
        DataFrame: 包含社保基金新进股票的记录
    """
    # 筛选社保基金相关股东
    social_security_keywords = [
        '社保', '社会保险', '全国社保', '基本养老保险', '社会保障'
    ]
    
    # 创建布尔索引
    is_social_security = holders_df['股东名称'].str.contains(
        '|'.join(social_security_keywords), 
        regex=True, 
        na=False
    )
    
    ss_holders = holders_df[is_social_security].copy()
    print(f"\n📊 共找到 {len(ss_holders)} 条社保基金持股记录")
    
    # 按股票代码和报告期排序
    ss_holders = ss_holders.sort_values(['股票代码', '报告期'])
    
    # 找出"新进"的记录
    new_entries = ss_holders[ss_holders['期末持股 - 持股变动'] == '新进'].copy()
    print(f"📈 其中社保基金新进的记录：{len(new_entries)} 条")
    
    return new_entries


def get_stock_price_after_days(stock_code, base_date, days_after):
    """
    获取股票在指定日期后若干天的收盘价
    
    Args:
        stock_code: 股票代码（带市场标识）
        base_date: 基准日期（字符串，格式 YYYY-MM-DD）
        days_after: 之后多少天
        
    Returns:
        tuple: (日期，收盘价，涨跌幅) 或 (None, None, None)
    """
    try:
        # 将基础日期转换为 datetime
        base_dt = datetime.strptime(base_date, '%Y-%m-%d')
        
        # 计算目标日期（考虑交易日，简单处理为自然日 + 额外天数）
        target_dt = base_dt + timedelta(days=int(days_after * 1.5))  # 考虑交易日因素
        
        # 获取历史行情
        end_date = target_dt.strftime('%Y%m%d')
        start_date = base_dt.replace('-', '')
        
        # 使用 akshare 获取日线数据 2026-03-31-09-01_20231231_holders.csv
        df = ak.stock_zh_a_hist(
            symbol=stock_code,
            period="daily",
            start_date=start_date,
            end_date=end_date,
            adjust="qfq"  # 前复权
        )
        
        if df.empty or len(df) < 2:
            return None, None, None
        
        # 获取基期收盘价（公告日后的第一个交易日）
        base_close = df.iloc[0]['收盘']
        
        # 获取目标日期附近的收盘价
        # 找到最接近目标日期的记录
        df['日期'] = pd.to_datetime(df['日期'])
        target_row = df[df['日期'] <= target_dt].iloc[-1]
        target_close = target_row['收盘']
        target_date = target_row['日期'].strftime('%Y-%m-%d')
        
        # 计算涨跌幅
        change_pct = ((target_close - base_close) / base_close) * 100
        
        return target_date, target_close, change_pct
        
    except Exception as e:
        # print(f"获取 {stock_code} 数据失败：{e}")
        return None, None, None


def analyze_performance(new_entries_df):
    """
    分析社保基金进入后的股票表现
    
    Args:
        new_entries_df: 社保基金新进记录
    """
    print("\n" + "="*80)
    print("开始分析社保基金进入后的股票表现...")
    print("="*80)
    
    results = []
    
    # 去重：同一股票在同一报告期可能有多只社保基金
    unique_entries = new_entries_df.drop_duplicates(subset=['股票代码', '报告期'])
    
    print(f"\n需要分析 {len(unique_entries)} 只股票...")
    
    for idx, row in unique_entries.iterrows():
        stock_code = row['股票代码']
        stock_name = row['股票简称']
        report_date = row['报告期']
        holder_name = row['股东名称']
        hold_quantity = row['期末持股 - 数量']
        market_value = row['期末持股 - 流通市值']
        
        # 将报告期转换为日期格式
        # 报告期通常是季度末：0331, 0630, 0930, 1231
        report_date_str = f"{report_date[:4]}-{report_date[4:6]}-{report_date[6:]}"
        
        print(f"\n[{idx+1}/{len(unique_entries)}] 分析 {stock_code} {stock_name} (报告期：{report_date})")
        
        # 获取 3 个月后的表现
        date_3m, price_3m, change_3m = get_stock_price_after_days(
            stock_code, report_date_str, 90
        )
        
        # 获取 6 个月后的表现
        date_6m, price_6m, change_6m = get_stock_price_after_days(
            stock_code, report_date_str, 180
        )
        
        # 获取 1 年后的表现
        date_1y, price_1y, change_1y = get_stock_price_after_days(
            stock_code, report_date_str, 365
        )
        
        result = {
            '股票代码': stock_code,
            '股票简称': stock_name,
            '报告期': report_date,
            '社保基金名称': holder_name,
            '持股数量': hold_quantity,
            '持股市值': market_value,
            '3 个月后日期': date_3m,
            '3 个月后价格': price_3m,
            '3 个月涨跌幅 (%)': round(change_3m, 2) if change_3m else None,
            '6 个月后日期': date_6m,
            '6 个月后价格': price_6m,
            '6 个月涨跌幅 (%)': round(change_6m, 2) if change_6m else None,
            '1 年后日期': date_1y,
            '1 年后价格': price_1y,
            '1 年涨跌幅 (%)': round(change_1y, 2) if change_1y else None,
        }
        
        results.append(result)
        
        # 打印进度
        if change_3m is not None:
            print(f"  3 个月：{change_3m:+.2f}%")
        if change_6m is not None:
            print(f"  6 个月：{change_6m:+.2f}%")
        if change_1y is not None:
            print(f"  1 年：  {change_1y:+.2f}%")
        
        # 添加延迟，避免请求过快
        import time
        time.sleep(1)
    
    return pd.DataFrame(results)


def calculate_statistics(results_df):
    """
    计算统计数据
    
    Args:
        results_df: 分析结果 DataFrame
    """
    print("\n" + "="*80)
    print("📊 统计结果")
    print("="*80)
    
    periods = ['3 个月', '6 个月', '1 年']
    columns = ['3 个月涨跌幅 (%)', '6 个月涨跌幅 (%)', '1 年涨跌幅 (%)']
    
    stats = []
    
    for period, col in zip(periods, columns):
        valid_data = results_df[col].dropna()
        
        if len(valid_data) > 0:
            count = len(valid_data)
            mean_return = valid_data.mean()
            median_return = valid_data.median()
            std_return = valid_data.std()
            positive_count = (valid_data > 0).sum()
            negative_count = (valid_data < 0).sum()
            win_rate = positive_count / count * 100
            
            # 最好和最差表现
            best_stock_idx = valid_data.idxmax()
            worst_stock_idx = valid_data.idxmin()
            best_stock = results_df.loc[best_stock_idx, '股票简称']
            worst_stock = results_df.loc[worst_stock_idx, '股票简称']
            best_return = valid_data.max()
            worst_return = valid_data.min()
            
            stats.append({
                '时间段': period,
                '样本数量': count,
                '平均收益率 (%)': round(mean_return, 2),
                '中位数收益率 (%)': round(median_return, 2),
                '标准差': round(std_return, 2),
                '上涨家数': positive_count,
                '下跌家数': negative_count,
                '胜率 (%)': round(win_rate, 2),
                '最好表现股票': best_stock,
                '最好收益率 (%)': round(best_return, 2),
                '最差表现股票': worst_stock,
                '最差收益率 (%)': round(worst_return, 2),
            })
        else:
            stats.append({
                '时间段': period,
                '样本数量': 0,
                '平均收益率 (%)': None,
                '中位数收益率 (%)': None,
                '标准差': None,
                '上涨家数': 0,
                '下跌家数': 0,
                '胜率 (%)': None,
                '最好表现股票': None,
                '最好收益率 (%)': None,
                '最差表现股票': None,
                '最差收益率 (%)': None,
            })
    
    stats_df = pd.DataFrame(stats)
    
    # 打印统计结果
    print("\n" + "="*80)
    print("社保基金进入后股票表现统计")
    print("="*80)
    print(stats_df.to_string(index=False))
    print("="*80)
    
    return stats_df


def main():
    """主函数"""
    
    print("="*80)
    print("社保基金进入十大流通股东后的股票表现分析")
    print("="*80)
    
    # 1. 加载数据
    data_dir = r'/akShare/十大流通股东/fetched_datasource'
    print(f"\n正在加载数据 from {data_dir}...")
    
    holders_df = load_all_holders_data(data_dir)
    
    if holders_df.empty:
        print("❌ 未找到股东数据")
        return
    
    print(f"\n✅ 共加载 {len(holders_df)} 条股东数据")
    
    # 2. 找出社保基金新进记录
    new_entries = find_social_security_entries(holders_df)
    
    if new_entries.empty:
        print("❌ 未找到社保基金新进记录")
        return
    
    # 3. 分析股票表现（这里只分析前 10 只作为测试）
    # 实际运行时可以去掉 .head(10)
    sample_entries = new_entries.head(10)  # 测试用，去掉 head 可以分析全部
    results_df = analyze_performance(sample_entries)
    
    # 4. 保存详细结果
    output_file = r'E:\Develop\Repos\pythonProject\stock\analysis\社保基金进入后股票表现分析.csv'
    results_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n💾 详细结果已保存到：{output_file}")
    
    # 5. 计算统计数据
    stats_df = calculate_statistics(results_df)
    
    # 6. 保存统计结果
    stats_file = r'E:\Develop\Repos\pythonProject\stock\analysis\社保基金表现统计.csv'
    stats_df.to_csv(stats_file, index=False, encoding='utf-8-sig')
    print(f"\n💾 统计结果已保存到：{stats_file}")
    
    print("\n" + "="*80)
    print("分析完成！")
    print("="*80)


if __name__ == "__main__":
    main()
