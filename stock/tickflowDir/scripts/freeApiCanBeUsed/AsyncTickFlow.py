import asyncio

from tickflow import AsyncTickFlow


async def fetch_stock_data(tf: AsyncTickFlow, symbol: str) -> dict:
    """获取单只股票数据并进行分析"""
    df = await tf.klines.get(symbol, period="1d", count=60, as_dataframe=True)

    df["ma20"] = df["close"].rolling(20).mean()
    latest = df.iloc[-1]

    return {
        "symbol": symbol,
        "price": latest["close"],
        "ma20": latest["ma20"],
        "above_ma20": latest["close"] > latest["ma20"]
    }


async def main():
    async with AsyncTickFlow(api_key="tk_70e08101458040caa8fe082bf28587ac") as tf:
        symbols = ["600000.SH", "600519.SH", "000001.SZ", "000858.SZ", "601318.SH"]

        tasks = [fetch_stock_data(tf, s) for s in symbols]
        results = await asyncio.gather(*tasks)

        for r in results:
            status = "📈 站上" if r["above_ma20"] else "📉 跌破"
            print(f"{r['symbol']}: {r['price']:.2f} ({status} MA20: {r['ma20']:.2f})")


asyncio.run(main())
