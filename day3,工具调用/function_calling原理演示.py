


def get_weather(city:str) -> str:
    fake_db = {"北京":"晴,12°","上海":"雨,18°"}
    return fake_db.get(city,"未知城市")

TOOL_FUNCS = {"get_weather":get_weather}

# tools参数,给模型看的说明书

TOOLS = [{
    "name":"get_weather",
    "description":"查询某城市当前天气,用户询问天气时调用",

    # 定义的接收参数类型
    "input_schema":{
    "type":"object",#表明参数是一个对象
    "properties":{"city":{"type":"string","description":"城市中文名"}},
        # 列出每一个参数的名字类型和说明
    "required":["city"]
        # 列出必填项
},
}]


def fake_model(messages):
    last = messages[-1]
    has_tool_result = (isinstance(last["content"], list)
                       and last["content"][0].get("type") == "tool_result")
    if not has_tool_result:  # 第一轮: 模型决定调用工具,只输出结构化意图
        return {"stop_reason": "tool_use", "content": [{
            "type": "tool_use", "id": "toolu_01",
            "name": "get_weather", "input": {"city": "北京"}}]}
    # 第二轮: 模型读到工具结果后,生成自然语言回答
    result = last["content"][0]["content"]
    return {"stop_reason": "end_turn", "content": [{
        "type": "text", "text": f"北京现在的天气是:{result}"}]}

def run(user_text):
    messages = [{"role":"user","content":user_text}]
    while True:
        resp = fake_model(messages)
        messages.append({"role":"assistant","content":resp["content"]})
        if resp["stop_reason"] != "tool_use":
            return next(b['text'] for b in resp["content"] if b["type"] == "text")
        tool_result = []
        for block in resp["content"]:
            if block["type"] != "tool_use":
                continue
            func = TOOL_FUNCS.get(block["name"])
            try:
                out = func(**block["input"]) if func else f"错误:未知工具{block['name']}"
            except Exception as e:
                out = f"执行出错:{e}"

            tool_result.append({"type":"tool_result",
                                "tool_use_id":block["id"],
                                "content":out})
        messages.append({"role":"user","content":tool_result})

if __name__ =="__main__":
    print(run("上海今天天气怎么样?"))