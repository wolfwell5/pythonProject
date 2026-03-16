import random
import time


def gen_year_period_list(start_year, end_year):
    years = []
    for year in range(start_year, end_year):
        years.append(year)
    return years


def generate_quarter_report_dates(start_year, end_year):
    """
    生成股票季报日期列表，格式为年份后两位+季度末日期，如250331表示2025年第一季度末
    
    :param start_year: 开始年份
    :param end_year: 结束年份（不包含）
    :return: 季报日期列表
    """
    quarter_dates = []
    for year in range(start_year, end_year):
        # 年份后两位
        year = str(year)
        # 四个季度的月末日期
        quarters = [year + '0331', year + '0630',
                    year + '0930', year + '1231']
        quarter_dates.extend(quarters)
    return quarter_dates


def random_wait():
    print('开始等待...')
    wait_time = random.uniform(3, 10)  # 随机等待 3~10 秒
    print(f"等待 {wait_time:.1f} 秒后继续...")
    time.sleep(wait_time)
    print(f"等待 end.")


def main():
    print('开始 执行...')
    random_wait()


if __name__ == "__main__":
    main()
