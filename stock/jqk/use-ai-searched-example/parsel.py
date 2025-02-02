import parsel

# 假设这是你的 HTML 文档（实际上，这通常是一个更大的字符串）
html_doc = '''
   <table>
       <tr>
           <th style="width:4%">序号</th>
           <!-- 其他表头元素 -->
       </tr>
       <!-- 其他行 -->
   </table>
   '''

# 创建一个 Selector 对象
selector1 = parsel.Selector(html_doc)

# 使用 CSS 选择器定位到 <th> 元素
# 这里我们使用 th[style*="width:4%"] 来选择 style 属性中包含 "width:4%" 的 <th> 元素
th_selector = selector1.css('th[style*="width:4%"]')

# 提取文本内容
text = th_selector.css('th::text').get()

# 打印结果
print(text)  # 输出: 序号

