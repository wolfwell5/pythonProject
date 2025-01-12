from openpyxl import Workbook
from openpyxl.chart import Reference, LineChart

wb = Workbook()
ws = wb.active

rows = [
    ['月份', '桃子', '西瓜', '龙眼'],
    [1, 38, 28, 29],
    [2, 52, 21, 35],
    [3, 39, 20, 69],
    [4, 51, 29, 41],
    [5, 29, 39, 31],
    [6, 30, 41, 39]
]

for row in rows:
    ws.append(row)

c1 = LineChart()
c1.title = '果果销量'
c1.style = 13
c1.x_axis.title = '月份'
c1.y_axis.title = '销量'

data = Reference(ws, min_row=1, max_row=7, min_col=2, max_col=4)
c1.add_data(data, titles_from_data=True)

s0 = c1.series[0]
s0.marker.symbol = 'triangle'
s0.marker.graphicalProperties.solidFill = 'FF0000'
s0.marker.graphicalProperties.line.solidFill = '0000FF'

s1 = c1.series[1]
s1.graphicalProperties.line.solidFill = '0000AA'
s1.graphicalProperties.line.dashStyle = 'sysDot'
s1.graphicalProperties.line.width = 80000

s2 = c1.series[2]
s2.smooth = True

ws.add_chart(c1, 'a10')

wb.save("8 图表.xlsx")
