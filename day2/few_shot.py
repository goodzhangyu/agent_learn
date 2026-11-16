from email import message

from openai import OpenAI, base_url
import os

api_key=os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(
    api_key=api_key,
    base_url = "https://api.deepseek.com"
)
messages = [
    {
        "role":"system","content":"你是一个情感分析助手,只能判断正面,负面,中性"
    },
    # 示例一
    {
        "role":"user","content":"评论:这家餐厅太棒了"
    },
    {
        "role":"assistant","content":"正面"
    },
    # 示例二
    {
        "role":"user","content":"评论:服务太差了,再也不来了"
    },
    {
        "role":"assistant","content":"负面"
    },
    # 示例三
    {
        "role":"user","content":"评论:环境不错,但是价格有点贵"
    },
    {
        "role":"assistant","content":"中性"
    },
    {
        "role":"user","content":"评论:这家酒店的服务非常周到,房间=也干净"
    },
]

response = client.chat.completions.create(
    model="deepseek-flash",
    messages=messages,
    temperature=0
)

print(response.choices[0].message.content)

