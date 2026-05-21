def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "错误：除数不能为 0"
    return a / b

def main():
    print("=== 简单计算器 ===")
    print("支持运算：+ (加), - (减), * (乘), / (除)")
    print("输入 q 退出")

    while True:
        expr = input("\n请输入表达式（如 3 + 5）：").strip()
        if expr.lower() == 'q':
            break

        parts = expr.split()
        if len(parts) != 3:
            print("格式错误，请按「数字 运算符 数字」格式输入")
            continue

        a_str, op, b_str = parts
        try:
            a = float(a_str)
            b = float(b_str)
        except ValueError:
            print("数字格式错误")
            continue

        if op == '+':
            result = add(a, b)
        elif op == '-':
            result = subtract(a, b)
        elif op == '*':
            result = multiply(a, b)
        elif op == '/':
            result = divide(a, b)
        else:
            print("不支持的运算符")
            continue

        print(f"结果：{result}")

if __name__ == "__main__":
    main()
