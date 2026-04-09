from datetime import datetime

import akshare as ak

from akShare.util.anti_ban import human_like_wait
from akShare.util.csv_utils import save_csv_with_name
from stock.akShare.util.time import generate_quarter_report_dates


def fetch_data(date):
    start_dt = datetime.now()
    stock_gdfx_free_holding_detail_em_df = ak.stock_gdfx_free_holding_detail_em(date=date)
    fetch_end_dt = datetime.now()
    print(f"数据抓取耗时：{(fetch_end_dt - start_dt).total_seconds():.4f} 秒")

    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    file_name = f"{date}_{timestamp}_holders.csv"

    save_csv_with_name(stock_gdfx_free_holding_detail_em_df, file_name, specific_folder='fetched_datasource')


def main():
    quarter_report_dates = generate_quarter_report_dates(2019, 2020)
    for date in quarter_report_dates:
        fetch_data(date)
        human_like_wait()


if __name__ == "__main__":
    main()
    # fetch_data("20251231")

