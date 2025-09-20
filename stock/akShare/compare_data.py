import pandas as pd


def read_xls_file(file_path):
    """
    读取XLS文件并返回DataFrame
    """
    # 尝试多种编码方式读取文件
    encodings = ['utf-8', 'gbk', 'gb2312', 'latin1']

    content = None
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            print(f"成功使用 {encoding} 编码读取文件")
            break
        except UnicodeDecodeError:
            print(f"使用 {encoding} 编码读取失败")
            continue

    if content is None:
        # 如果所有编码都失败，使用二进制模式读取并忽略错误
        with open(file_path, 'rb') as f:
            content = f.read().decode('utf-8', errors='ignore')
        print("使用utf-8编码并忽略错误的方式读取文件")

    # 按行分割内容
    lines = content.splitlines()

    # 解析数据
    data = []
    for line in lines[1:]:  # 跳过标题行
        parts = line.strip().split('\t')
        if len(parts) >= 4:
            code = parts[0]
            name = parts[1]
            price = parts[2]
            market_value = parts[3]
            data.append([code, name, price, market_value])

    df = pd.DataFrame(data, columns=['代码', '名称', '最新价', '总市值'])
    return df


def read_csv_file(file_path):
    """
    读取CSV文件并返回DataFrame
    """
    df = pd.read_csv(file_path)
    return df


def compare_data(xls_df, csv_df):
    """
    比较两个DataFrame中的数据
    """
    print("XLS文件中的数据条数:", len(xls_df))
    print("CSV文件中的数据条数:", len(csv_df))

    # 找出在XLS中但不在CSV中的股票
    # only_in_xls = []
    # for _, xls_row in xls_df.iterrows():
    #     xls_code = pd.to_numeric(xls_row['代码'], errors='coerce')
    #
    #     found = False
    #     # 在CSV中查找相同代码的行
    #     for _, csv_row in csv_df.iterrows():
    #         csv_code = csv_row['代码']
    #         if xls_code == csv_code:
    #             found = True
    #             break
    #     if not found:
    #         only_in_xls.append(xls_row)
    #
    # if only_in_xls:
    #     print("\n仅在XLS文件中存在的股票:")
    #     only_in_xls_df = pd.DataFrame(only_in_xls)
    #     print(only_in_xls_df[['代码', '名称']])
    # else:
    #     print("\nXLS文件中的所有股票都在CSV文件中找到")

    # 找出在CSV中但不在XLS中的股票
    only_in_csv = []
    for _, csv_row in csv_df.iterrows():
        csv_code = csv_row['代码']
        found = False
        # 在XLS中查找相同代码的行
        for _, xls_row in xls_df.iterrows():
            xls_code = pd.to_numeric(xls_row['代码'], errors='coerce')
            if csv_code == xls_code:
                found = True
                break
        if not found:
            only_in_csv.append(csv_row)

    if only_in_csv:
        print("\n仅在CSV文件中存在的股票:")
        only_in_csv_df = pd.DataFrame(only_in_csv)
        print(only_in_csv_df[['代码', '名称']])
    else:
        print("\nCSV文件中的所有股票都在XLS文件中找到")

    # 找出两个文件中都存在的股票并比较数据

    # common_differences = []
    # for _, xls_row in xls_df.iterrows():
    #     xls_code = xls_row['代码']
    #     for _, csv_row in csv_df.iterrows():
    #         csv_code = csv_row['代码']
    #         if xls_code == csv_code:
    #             # 找到匹配的行，比较数据
    #             # 比较名称
    #             if xls_row['名称'] != csv_row['名称']:
    #                 common_differences.append({
    #                     '代码': xls_code,
    #                     '字段': '名称',
    #                     'XLS值': xls_row['名称'],
    #                     'CSV值': csv_row['名称']
    #                 })
    #
    #             # 比较总市值
    #             if str(xls_row['总市值']) != str(csv_row['总市值']):
    #                 common_differences.append({
    #                     '代码': xls_code,
    #                     '字段': '总市值',
    #                     'XLS值': xls_row['总市值'],
    #                     'CSV值': csv_row['总市值']
    #                 })
    #             break  # 找到匹配项后跳出内层循环
    #
    # if common_differences:
    #     print("\n两个文件中共同股票的数据差异:")
    #     diff_df = pd.DataFrame(common_differences)
    #     for _, row in diff_df.iterrows():
    #         print(f"代码: {row['代码']}, 字段: {row['字段']}")
    #         print(f"  XLS值: {row['XLS值']}")
    #         print(f"  CSV值: {row['CSV值']}")
    #         print()
    # else:
    #     print("\n两个文件中共同股票的数据完全一致。")

    # return only_in_xls, only_in_csv, common_differences
    return only_in_csv


def main():
    # 文件路径
    xls_file = r'E:\Develop\Repos\pythonProject\stock\akShare\sample_data\北交所\Table.xls'
    csv_file = r'E:\Develop\Repos\pythonProject\stock\akShare\sample_data\北交所\2025-09-20-17-02_北交所-总市值正序.csv'

    # 读取数据
    print("正在读取XLS文件...")
    xls_df = read_xls_file(xls_file)

    print("正在读取CSV文件...")
    csv_df = read_csv_file(csv_file)

    # 显示基本信息
    # print("\nXLS文件前5行:")
    # print(xls_df.head())
    #
    # print("\nCSV文件前5行:")
    # print(csv_df.head())

    # 比较数据
    print("\n开始比较数据...")
    compare_data(xls_df, csv_df)


if __name__ == "__main__":
    main()
