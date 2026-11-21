def get_weather(city:str) -> str:
    db = {"北京":"晴,12°","上海":"小雨,17°","深圳":"多云,22°"}
    if city not in db:
        print(f"暂不支持{city}")
    return db[city]


# 下面的是计算器函数
import ast
import operator

_BIN_OPS = {ast.Add: operator.add, ast.Sub: operator.sub,
            ast.Mult: operator.mul, ast.Div: operator.truediv}
_UNARY_OPS = {ast.USub: operator.neg, ast.UAdd: operator.pos}


def _eval_node(node):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN_OPS:
        return _BIN_OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return _UNARY_OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError("表达式包含不允许的内容")


def calculator(expression: str) -> str:
    tree = ast.parse(expression, mode="eval")
    return str(_eval_node(tree))


# tools的声名
TOOLS = [
    {
        "name":"get_weather",
        "description":"查询数据库中的城市天气,用户查询天气时使用",
        "input_schema":{
            "type":"object",
            "properties":{
                "city":{"type":"string","description":"城市中文名"},
            },
            "required":["city"],
        },
    },
    {
        "name":"calculator",
        "description":"计算四则运算",
        "input_schema":{
            "type":"object",
            "properties":{
                "expression":{"type":"string","description":"数字运算表达式例如(12+5)*3"},
            },
            "required":["expression"],
        },
    },
]

TOOL_FUNCS = {"get_weather":get_weather,"calculator":calculator}


