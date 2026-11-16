from openai import OpenAI
import os

api_key = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key=api_key,
)
messages = [
    {"role": "system", "content": "你是一个python专家,精通python"}
]

question = str(input("请输入问题:(输入exit退出)"))
while question != "exit":
    messages.append({"role": "user", "content": question})
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=messages,
    )
    answer = response.choices[0].message.content
    print(answer)
    messages.append({"role": "assistant", "content": answer})
    question = str(input("请输入问题:(输入exit退出)"))

print("调用结束")





