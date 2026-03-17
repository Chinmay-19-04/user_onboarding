def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a / b


def main():
    print("Simple Calculator")
    print("Operations: +  -  *  /")

    while True:
        try:
            num1 = float(input("Enter first number: "))
            op = input("Enter operator (+, -, *, /): ")
            num2 = float(input("Enter second number: "))

            if op == "+":
                print("Result:", add(num1, num2))
            elif op == "-":
                print("Result:", subtract(num1, num2))
            elif op == "*":
                print("Result:", multiply(num1, num2))
            elif op == "/":
                print("Result:", divide(num1, num2))
            else:
                print("Invalid operator")

        except ValueError:
            print("Invalid input. Please enter numbers.")

        cont = input("Do another calculation? (y/n): ").lower()
        if cont != "y":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
