# openaisdk调用

首先创建一个Openai实例对象,然后在对这个实例对象调用方法

client.chat.completions.create()方法

在SDK调用中,数据流向如下:

我给大模型的:

client.chat.completions.create方法里面的参数如:model,message等



大模型返回给我的:

该方法的返回值,即response变量



## message变量的角色

system:设定模型行为,人设

user:用户的输入

asistant:模型的回复或工具调用

tool:返回工具执行结果



## 核心参数temperature,top_p,max_token



### temperature

默认值为1,控制生成文本的随机性和创造性,取值范围0-2数字越低,表示输出跟准确,聚焦

数字越大,代表输出更加随机,创造性更强,但是幻觉问题更加严重



### top_p

通过概率来控制待选词的范围,temperature的备选方案,默认为1

通过概率来考虑待选词作为输出

0.1时,只从概率最高的前10%的候选词选择,输出稳定

0.9时,从概率最高的前90%中的候选词选择,保留主要逻辑的同时允许多样

1时.不限制,考虑所有的待选词



temperat和top_p的区别,其中temperature可以让低概率的词取到,而top_p取不到低概率的词



## 流式输出

在client.chat.completions.create()方法里面指定fluent = True

不使用流式输出的输出

print(response.choices[0].message.content)

使用流式输出的时候的输出不能使用上面的输出,需要使用一个循环遍历每一个数据块



```
for chunk in response:
    delta = chunk.choices[0].delta
    # delta表示返回的增量,上面一行指的是从当前数据块中提取增量信息
    # 流式输出采用的是增量返回机制
    if delta.content:
        print(delta.content,end="")
```

