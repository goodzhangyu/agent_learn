"""
Function Calling 最小原理演示(无需 API Key)
流程: tools 声明 -> 模型返回 tool_use -> 本地执行 -> tool_result 回传 -> 模型给出最终回答
"""
import json


# 1) 真正执行的工具(普通 Python 函数)
def get_weather(city: str) -> str:
    fake_db = {"北京": "晴, 12°C", "上海": "雨, 18°C"}
    return fake_db.get(city, "未知城市")


TOOL_FUNCS = {"get_weather": get_weather}


# 2) tools 参数: 给模型看的"说明书"(name / description / JSON Schema)
TOOLS = [{
    "name": "get_weather",
    "description": "查询某城市当前天气。用户询问天气时调用。",
    "input_schema": {
        "type": "object",
        "properties": {"city": {"type": "string", "description": "城市中文名"}},
        "required": ["city"],
    },
}]


# 3) 模拟模型。真实场景这里是:
#    client.messages.create(model=..., tools=TOOLS, messages=messages)
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


# 4) Agent 循环: 模型不执行任何东西,执行和回传都由我们的代码完成
def run(user_text):
    messages = [{"role": "user", "content": user_text}]
    while True:
        resp = fake_model(messages)  # 每轮都要带上完整历史(模型本身无状态)
        messages.append({"role": "assistant", "content": resp["content"]})

        if resp["stop_reason"] != "tool_use":
            return next(b["text"] for b in resp["content"] if b["type"] == "text")

        tool_results = []
        for block in resp["content"]:
            if block["type"] != "tool_use":
                continue
            func = TOOL_FUNCS.get(block["name"])
            try:
                out = func(**block["input"]) if func else f"错误: 未知工具 {block['name']}"
            except Exception as e:  # 出错也要回传,让模型有机会自我修正
                out = f"执行出错: {e}"
            tool_results.append({"type": "tool_result",
                                 "tool_use_id": block["id"],  # 必须与 tool_use 的 id 对应
                                 "content": out})
        messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    print(run("北京今天天气怎么样?"))
