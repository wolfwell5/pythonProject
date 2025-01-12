# from openpyxl import Workbook

# wb = Workbook()
# ws = wb.active
#
# rows = [
#     ['月份', '桃子', '西瓜', '芒果'],
#     ['1', '2', '3', '4'],
#     ['2', '3', '4', '5'],
#     ['3', '6', '7', '8'],
# ]

# for row in rows:
#     ws.append(row)
#
# ws.auto_filter.ref = 'a1:d4'
# ws.auto_filter.add_filter_column(1, ['3'])
# # ws.auto_filter.add_sort_condition('a1:a4', 'asc')
#
# wb.save("7 过滤排序.xlsx")

import pandas as pds

df = pds.read_excel('7 过滤排序.xlsx', sheet_name='Sheet')
df_value = df.sort_values(by=['桃子', '西瓜'], ascending=False)  # 先按桃子排序，相同的话再按西瓜排序

writer = pds.ExcelWriter('7 过滤排序2.xlsx')
df_value.to_excel(writer, sheet_name='Sheet2', index=False)

print(df_value)

writer._save()
