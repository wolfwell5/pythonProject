"""
删除前 34 只股票在指定日期之后的所有 K 线数据
"""
import os
import sys
import pandas as pd
from datetime import datetime

# 添加 stock 目录到 Python 路径
script_dir = os.path.dirname(os.path.abspath(__file__))  # util 目录
scripts_dir = os.path.dirname(script_dir)  # scripts 目录
tickflow_dir = os.path.dirname(scripts_dir)  # tickflowDir 目录
stock_dir = os.path.dirname(tickflow_dir)  # stock 目录
sys.path.insert(0, stock_dir)

# 现在可以从 tickflowDir 导入
from tickflowDir.scripts.SingleKlineFetcher import get_default_data_dir


def load_stock_codes_from_csv():
    """从 CSV 文件加载股票代码列表"""
    csv_path = os.path.join(
        tickflow_dir,  # 使用 tickflowDir 目录
        'data',
        'basic_info',
        'all_stock_codes.csv'
    )

    if not os.path.exists(csv_path):
        print(f"错误：CSV 文件不存在：{csv_path}")
        return None

    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    all_stock_codes = df['股票代码'].tolist()

    return all_stock_codes


def delete_after_date(code, cutoff_date):
    """
    删除某只股票在指定日期之后的所有数据
    
    Args:
        code: 股票代码
        cutoff_date: 截止日期字符串 'YYYY-MM-DD'（保留这一天及之前的数据）
    """
    data_dir = get_default_data_dir(code)

    # 查找所有 CSV 文件
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv') and code in f]

    if not csv_files:
        print(f"  ⊘ {code}: 未找到 CSV 文件")
        return 0

    deleted_count = 0

    for csv_file in csv_files:
        file_path = os.path.join(data_dir, csv_file)

        try:
            # 读取 CSV
            df = pd.read_csv(file_path)

            if df.empty or 'trade_date' not in df.columns:
                continue

            # 记录原始行数
            original_rows = len(df)

            # 过滤：只保留 cutoff_date 及之前的数据
            df_filtered = df[df['trade_date'] <= cutoff_date]

            # 如果有数据被删除
            if len(df_filtered) < original_rows:
                deleted = original_rows - len(df_filtered)
                deleted_count += deleted

                # 保存回 CSV
                df_filtered.to_csv(file_path, index=False)
                print(f"  ✓ {code}: 从 {csv_file} 删除 {deleted} 条记录 (保留 {cutoff_date} 及之前)")

        except Exception as e:
            print(f"  ✗ {code}: 处理 {csv_file} 失败 - {str(e)}")

    return deleted_count


def main():
    """主函数"""
    print("=" * 70)
    stock_num_to_delete = 60
    print("删除前  只股票在指定日期之后的所有数据")
    print("=" * 70)

    cutoff_date = '2026-03-24'

    # 验证日期格式
    try:
        datetime.strptime(cutoff_date, '%Y-%m-%d')
    except ValueError:
        print(f"错误：日期格式不正确，应为 YYYY-MM-DD")
        return

    print(f"\n截止日期：{cutoff_date} (保留该日期及之前的数据)")

    # 加载前 34 只股票
    all_codes = load_stock_codes_from_csv()
    if all_codes is None:
        return

    target_codes = all_codes[:stock_num_to_delete]
    print(f"目标股票数量：{len(target_codes)}\n")

    # 统计信息
    total_deleted = 0
    processed_count = 0

    # 遍历每只股票
    for idx, code in enumerate(target_codes, 1):
        print(f"[{idx}/{len(target_codes)}] 处理：{code}")
        deleted = delete_after_date(code, cutoff_date)
        if deleted > 0:
            total_deleted += deleted
            processed_count += 1
        else:
            print(f"  ⊘ {code}: 无数据可删除")

    # 汇总报告
    print("\n" + "=" * 70)
    print("删除完成！")
    print("=" * 70)
    print(f"处理股票数：{processed_count}/{len(target_codes)}")
    print(f"总计删除记录数：{total_deleted}")
    print(f"保留数据范围：<= {cutoff_date}")
    print("=" * 70)


if __name__ == '__main__':
    main()
    # 明确退出程序
    sys.exit(0)
