import akshare as ak
import pandas as pd

from stock.akShare.util.csv import generate_csv


def get_bjse_stocks_by_market_value():
    """
    获取北交所所有股票的名称、股价、总市值，并按市值大小正序排列
    """
    try:
        # 使用北交所专门的接口
        bjse_stocks_df = ak.stock_bj_a_spot_em()

        # 如果没有数据，提示错误
        if bjse_stocks_df is None or bjse_stocks_df.empty:
            print("未找到北交所股票数据，请检查akshare版本或尝试其他接口")
            return None

        # 查找需要的列（列名可能因版本而异）
        columns = bjse_stocks_df.columns.tolist()
        print(f"可用的列名: {columns}")

        # 尝试匹配需要的列
        code_col = None
        name_col = None
        price_col = None
        market_value_col = None

        for col in columns:
            if any(keyword in col for keyword in ['代码', '股票代码']):
                code_col = col
            elif any(keyword in col for keyword in ['名称', '股票名称', '简称']):
                name_col = col
            elif any(keyword in col for keyword in ['最新价', '现价', '收盘价']):
                price_col = col
            # elif any(keyword in col for keyword in ['总市值', '市值']):
            elif any(keyword in col for keyword in ['总市值']):
                market_value_col = col

        # 如果找不到确切的列名，使用常见的默认列名
        if not all([code_col, name_col, price_col, market_value_col]):
            # 北交所数据通常有这些列
            code_col = '代码' if '代码' in columns else columns[0] if len(columns) > 0 else None
            name_col = '名称' if '名称' in columns else columns[1] if len(columns) > 1 else None
            price_col = '最新价' if '最新价' in columns else columns[2] if len(columns) > 2 else None
            market_value_col = '总市值' if '总市值' in columns else columns[6] if len(columns) > 6 else None

        # 提取需要的数据
        result_df = bjse_stocks_df[[code_col, name_col, price_col, market_value_col]].copy()
        result_df.columns = ['代码', '名称', '最新价', '总市值']

        # 筛选真正的北交所股票（排除股转系统股票）
        # 北交所正式上市股票名称不含"定转"字样
        result_df = result_df[~result_df['名称'].str.contains('定转', na=False)]

        # 数据清洗和排序
        # 将总市值转换为数值类型
        result_df['总市值数值'] = pd.to_numeric(
            result_df['总市值'].astype(str).str.replace(',', '').str.replace('亿', 'e8').str.replace('万', 'e4').str.replace(
                '元', ''),
            errors='coerce'
        )

        # 去除空值并按市值排序
        result_df = result_df.dropna(subset=['总市值数值'])
        result_df = result_df.sort_values(by='总市值数值', ascending=True)

        # 返回最终结果
        final_result = result_df[['代码', '名称', '最新价', '总市值']].reset_index(drop=True)

        # 数据写到csv
        generate_csv(final_result, '北交所-总市值正序')

        return final_result

    except Exception as e:
        print(f"获取北交所股票数据时出错: {e}")
        print("请尝试更新akshare库: pip install akshare --upgrade")
        return None


# 另一种尝试方法：列出所有可能的接口
def list_available_stock_functions():
    """
    列出akshare中所有与股票相关的函数
    """
    import inspect
    stock_functions = []
    for name, obj in inspect.getmembers(ak):
        if inspect.isfunction(obj) and 'stock' in name.lower():
            stock_functions.append(name)

    print("可用的股票相关函数:")
    for func in stock_functions:
        if any(keyword in func for keyword in ['bj', 'bh', 'beijing', '北交']):
            print(f"  - {func} (可能与北交所相关)")


# 执行函数
if __name__ == "__main__":
    # 首先列出可能相关的函数
    # list_available_stock_functions()
    # generate_csv("", 'test1-test2')

    # 尝试获取数据
    result = get_bjse_stocks_by_market_value()
    if result is not None and not result.empty:
        print("\n北交所股票按总市值正序排列:")
        print(result)
    else:
        print("\n未能获取数据，请检查:")
        print("1. akshare版本是否为最新: pip install akshare --upgrade")
        print("2. 网络连接是否正常")
        print("3. 北交所接口是否已变更")

