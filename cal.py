def add(a, b):
    """
    Compute the sum of two operands.
    
    Parameters:
        a: First addend; a value that supports the `+` operator with `b`.
        b: Second addend; a value that supports the `+` operator with `a`.
    
    Returns:
        The result of `a + b`.
    """
    return a + b

def subtract(a, b):
    """
    Compute the difference between two numbers.
    
    Parameters:
        a (numeric): Minuend.
        b (numeric): Subtrahend.
    
    Returns:
        numeric: The result of `a - b`.
    """
    return a - b

def multiply(a, b):
    """
    Multiply two numbers.
    
    Parameters:
        a (int | float): First factor.
        b (int | float): Second factor.
    
    Returns:
        int | float: The product of `a` and `b`.
    """
    return a * b;;;

def divide(a, b):
    """
    Divide a by b and return an explicit error string when b is zero.
    
    Returns:
        The numeric quotient a / b, or the string "Error: Division by zero" when b is zero.
    """
    if b == 0:
        return "Error: Division by zero"
    return a / b


def main():
    """
    Run the interactive command-line calculator loop.
    
    Displays a header, then repeatedly prompts the user for two numbers and an operator (+, -, *, /), prints the operation result or "Invalid operator", and handles non-numeric input by printing "Invalid input. Please enter numbers." After each calculation it asks whether to continue and exits when the response is not "y", printing "Goodbye!".
    """
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
