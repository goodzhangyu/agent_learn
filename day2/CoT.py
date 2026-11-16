import os
from openai import OpenAI, base_url

api_key = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(
    api_key=api_key,
    base_url = "https://api.deepseek.com"
    )

question = """
小明有100元,买了一个原价80的商品,
先打八折,在使用10元优惠卷,
最后还剩多少
"""
messages = [
    {
        "role":"system","content":"""
        你是一名严谨的数学老师。

        请按照以下步骤解决问题：
        1. 提取已知条件
        2. 分析计算顺序
        3. 逐步列出计算过程
        4. 检查计算结果
        5. 给出最终答案

        请输出必要的解题步骤和关键依据，
        不需要输出冗长的内部思考过程。
        """
    },
    {"role":"user","content":question}
]
response = client.chat.completions.create(
    messages=messages,
    model="deepseek-flash",
)
print(response.choices[0].message.content)