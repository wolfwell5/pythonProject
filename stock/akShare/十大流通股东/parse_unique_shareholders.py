import inspect
import os
from collections import OrderedDict

import pandas as pd


def parse_all_shareholders_from_directory(input_directory, output_file_path):
    """
    遍历目录下所有CSV文件，提取并去重股东名称
    
    Args:
        input_directory (str): 输入CSV文件目录路径
        output_file_path (str): 输出CSV文件路径
    """
    try:
        # 获取目录下所有CSV文件
        csv_files = [f for f in os.listdir(input_directory) if f.endswith('.csv')]
        
        if not csv_files:
            print(f"错误: 目录 {input_directory} 中没有找到CSV文件")
            return False
            
        print(f"找到 {len(csv_files)} 个CSV文件")
        
        # 存储所有股东名称
        all_shareholders = []
        
        # 遍历所有CSV文件
        for csv_file in csv_files:
            file_path = os.path.join(input_directory, csv_file)
            print(f"正在处理文件: {csv_file}")
            
            try:
                # 读取CSV文件
                df = pd.read_csv(file_path, encoding='utf-8')
                
                # 检查必要的列是否存在
                if '股东名称' not in df.columns:
                    print(f"警告: 文件 {csv_file} 中没有找到'股东名称'列，跳过该文件")
                    continue
                
                # 提取股东名称列并添加到总列表
                shareholder_names = df['股东名称'].tolist()
                all_shareholders.extend(shareholder_names)
                print(f"  从 {csv_file} 提取了 {len(shareholder_names)} 个股东名称")
                
            except Exception as e:
                print(f"警告: 处理文件 {csv_file} 时出错: {str(e)}，跳过该文件")
                continue

        # 去重并保持原有顺序
        unique_shareholders = list(OrderedDict.fromkeys(all_shareholders))

        # 创建新的DataFrame
        result_df = pd.DataFrame({
            '序号': range(1, len(unique_shareholders) + 1),
            '股东名称': unique_shareholders
        })

        # if not os.path.exists(output_file_path):
        #     os.makedirs(output_file_path)

        # 确保输出目录存在
        output_dir = os.path.dirname(output_file_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"创建输出目录: {output_dir}")

        # 保存到新的CSV文件
        result_df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

        print(f"解析完成!")
        print(f"总共处理了 {len(csv_files)} 个CSV文件")
        print(f"累计原始数据行数: {len(all_shareholders)}")
        print(f"去重后股东数量: {len(unique_shareholders)}")
        print(f"结果已保存到: {output_file_path}")

        # 显示前10个股东名称作为示例
        print("\n前10个去重后的股东名称:")
        for i, name in enumerate(unique_shareholders[:10], 1):
            print(f"{i:2d}. {name}")

        return True

    except FileNotFoundError:
        print(f"错误: 找不到目录 {input_directory}")
        return False
    except Exception as e:
        print(f"处理过程中出现错误: {str(e)}")
        return False


def main():
    # 动态获取当前文件所在目录
    current_file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
    script_dir = os.path.dirname(current_file_path)
    
    print(f"脚本所在目录: {script_dir}")
    
    # 输入目录路径
    input_directory = os.path.join(script_dir, 'fetched_datasource')
    
    # 输出文件路径
    output_file = os.path.join(script_dir, 'parsed_datasource', 'unique_share_holders.csv')
    
    # 执行解析
    success = parse_all_shareholders_from_directory(input_directory, output_file)

    if success:
        print("\n✅ 处理成功完成!")
        print(f"输入目录路径: {input_directory}")
        print(f"输出文件路径: {output_file}")
    else:
        print("\n❌ 处理失败!")


if __name__ == "__main__":
    main()
