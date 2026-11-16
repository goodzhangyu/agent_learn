import os
from openai import OpenAI
api_key = os.getenv('DEEPSEEK_API_KEY')

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {"role":"user","content":"写一个200字左右的故事"}
    ],
    stream = True
)
# 指定了stream,返回的response是一个可迭代数据流
for chunk in response:
    delta = chunk.choices[0].delta
    # delta表示返回的增量,上面一行指的是从当前数据块中提取增量信息
    # 流式输出采用的是增量返回机制
    if delta.content:
        print(delta.content,end="")