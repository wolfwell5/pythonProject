"""
使用 requests 直接调用 Tickflow 的 /v1/klines/batch API

注意：这个 API 在 Python SDK 中没有封装，需要使用 requests 直接调用
"""

import pandas as pd
import requests

# API 配置
API_KEY = 'tk_70e08101458040caa8fe082bf28587ac'
BASE_URL = 'https://api.tickflow.org/v1/klines/batch'

headers = {
    'x-api-key': API_KEY,
    'Content-Type': 'application/json'
}


def get_klines_batch(symbols, period='1d', count=100, adjust='forward_additive'):
    """
    批量获取多只股票的 K 线数据

    Args:
        symbols: 股票代码列表，如 ["600000.SH", "000001.SZ", "600519.SH"]
        period: K 线周期，可选值：
                - '1m': 1 分钟
                - '5m': 5 分钟
                - '15m': 15 分钟
                - '30m': 30 分钟
                - '60m': 60 分钟
                - '1d': 日线
                - '1w': 周线
                - '1mon': 月线
        count: 每只股票获取的数据条数，默认 100
        adjust: 复权类型，可选值：
                - 'forward_additive': 前复权（默认）
                - 'backward_additive': 后复权
                - 'none': 不复权

    Returns:
        dict: 字典格式，key 为股票代码，value 为 DataFrame
    """
    # 构建请求参数
    params = {
        'symbols': symbols,
        'period': period,
        'count': count,
        'adjust': adjust
    }

    try:
        # 发送 POST 请求
        response = requests.post(BASE_URL, json=params, headers=headers)

        # 检查响应状态
        response.raise_for_status()

        # 解析 JSON 数据
        data = response.json()

        print(f"✓ 成功获取 {len(data)} 只股票的 K 线数据")

        # 转换为 DataFrame 字典
        result = {}
        for symbol, klines in data.items():
            if klines and len(klines) > 0:
                # 将 K 线数据转换为 DataFrame
                df = pd.DataFrame(klines)
                result[symbol] = df
                print(f"  - {symbol}: {len(df)} 条记录")
            else:
                print(f"  - {symbol}: 无数据")

        return result

    except requests.exceptions.RequestException as e:
        print(f"✗ 请求失败：{e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"  响应内容：{e.response.text}")
        return None
    except Exception as e:
        print(f"✗ 发生错误：{e}")
        return None


def main():
    """使用示例"""
    print("=" * 70)
    print("Tickflow Batch K-line API 使用示例")
    print("=" * 70)

    # 定义要获取的股票列表
    symbols = ["600000.SH", "000001.SZ", "600519.SH"]

    print(f"\n📊 获取以下股票的日线数据:")
    for s in symbols:
        print(f"   - {s}")

    # 调用 API
    print(f"\n⏳ 正在获取数据...")
    result = get_klines_batch(
        symbols=symbols,
        period='1d',  # 日线
        count=100,  # 每只股票 100 条
        adjust='forward_additive'  # 前复权
    )

    if result:
        print("\n✅ 数据获取成功！")

        # 查看某只股票的数据
        if "600000.SH" in result:
            df = result["600000.SH"]
            print(f"\n📈 600000.SH (浦发银行) 数据预览:")
            print(df.tail())

            # 查看列名
            print(f"\n数据列：{list(df.columns)}")
    else:
        print("\n❌ 数据获取失败！")


if __name__ == '__main__':
    main()
