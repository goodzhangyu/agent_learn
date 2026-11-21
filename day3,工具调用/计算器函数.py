def calculator(expression:str) -> str:
    while True:

        if "(" in expression:
            a = expression[expression.find("(")+1:expression.find(")")]
            for i in a :
