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
        {"role":"user","content":"你好请用一句话介绍一下你自己"},
        {"role":"assistant","content":"我是deepseek"}
    ]
)

print(response.choices[0].message.content)