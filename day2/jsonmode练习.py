import json
import os
from openai import OpenAI

api_key = os.getenv('DEEPSEEK_API_KEY')

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)
messages = [
    {
        "role":"system","content":"""
        你是一个信息提取助手,请从输入中提取:
        1.姓名
        2.年龄
        3.所在地
        4.学习技能
        必须返回合法的json格式,不需要其他的输出,如果提取不到信息返回NULL
        """
    },
    {"role":"user","content":"我今年22岁，来自安徽，正在学习Python"}
]
response = client.chat.completions.create(
    model="deepseek-flash",
    messages=messages,
    temperature=0,
    response_format={
        "type":"json_object",
    }
)

result = response.choices[0].message.content
data = json.loads(result)
print("姓名",data["姓名"])
print("年龄",data["年龄"])
print("所在地",data["所在地"])
print("学习技能",data["学习技能"])



