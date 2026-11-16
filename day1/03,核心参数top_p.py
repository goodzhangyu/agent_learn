import os
from openai import OpenAI
from torch.cuda import temperature

api_key = os.getenv('DEEPSEEK_API_KEY')

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {"role":"user","content":"写一个故事大概50字左右"}
    ],
    top_p=0.6
)

print(response.choices[0].message.content)
print("++++++++++++++++++++++++++++++++")
response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {"role":"user","content":"写一个故事大概50字左右"}
    ],
    top_p=1
)

print(response.choices[0].message.content)