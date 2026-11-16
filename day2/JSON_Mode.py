import json
from unittest import result

from openai import OpenAI
import os

api_key = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key=api_key,
)
message = [
    {"role":"system","content":"""
    你是一个商品信息提取助手,
    请从用户的输入中提取:
    1.商品名称
    2.预算
    3.内存大小
    必须返回合法的json格式,不要输出其他文字
    """
     },
    {"role":"user","content":"我想买一个价格在3000元左右的笔记本电脑,内存是16g的"}
]

response = client.chat.completions.create(
    model="deepseek-flash",
    messages=message,
#     开启json模式
    response_format={
        "type":"json_object"
    },
    temperature=0
)

result = response.choices[0].message.content
print(result)


# 将json字符串转化为python字典
data = json.loads(result)
print("商品名称:",data["商品名称"])
print("预算:",data["预算"])
print("内存:",data["内存大小"])