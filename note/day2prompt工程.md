# prompt工程

## few-shot

在prompt里面提供几个输入和输出的示例

具体写法:

```
你是一个感情分析助手,请判断用户评论的情感

示例一:
输入:这家餐厅真的太棒了,下次还来!
输出:负面

示例二:
输入:服务态度非常差,饭菜也不好吃!
输出:负面

示例三:
输入:环境不错,但是价格有点贵
输出:中性

现在请判断:
输入:这家酒店的服务非常周到,房间也干净
输出:
```

可以直接把示例作为历史对话放进messages



## CoT

思维链提示:

让模型按照一定的步骤分析问题,然后在给出最终答案

```
你是一名数学老师:
请按照以下步骤解决问题:
1.提取题目中的已知条件
2.分析计算顺序
3.逐步列出计算过程
4.检查计算结果
5.给出最终答案



```





## JSON Mode

返回json格式让计算机读得懂

```
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
```

注意:

json.load()将json字符串转为python对象

json.dumps()将python对象转为json字符串