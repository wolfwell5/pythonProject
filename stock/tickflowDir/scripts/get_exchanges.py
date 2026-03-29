import requests
import json
import os

# API 配置
url = 'https://api.tickflow.org/v1/exchanges'
headers = {
    'x-api-key': 'tk_70e08101458040caa8fe082bf28587ac'
}

try:
    # 发送 GET 请求
    response = requests.get(url, headers=headers)

    # 检查响应状态
    response.raise_for_status()

    # 解析 JSON 数据
    data = response.json()

    # 动态获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 数据保存到上级目录的 data 文件夹
    data_dir = os.path.join(os.path.dirname(script_dir), 'data\\basic_info')
    output_file = os.path.join(data_dir, 'exchanges', 'exchanges.json')

    # 保存到 JSON 文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✓ 数据获取成功！")
    print(f"✓ 已保存到：{output_file}")
    print(f"\n数据预览:")
    print(json.dumps(data, ensure_ascii=False, indent=2)[:500] + "...")

except requests.exceptions.RequestException as e:
    print(f"✗ 请求失败：{e}")
except json.JSONDecodeError as e:
    print(f"✗ JSON 解析失败：{e}")
except Exception as e:
    print(f"✗ 发生错误：{e}")
