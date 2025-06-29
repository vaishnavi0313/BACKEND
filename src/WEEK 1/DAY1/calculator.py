def add(numbers):
    return sum(numbers)

def subtract(numbers):
    result = numbers[0]
    for num in numbers[1:]:
        result -= num 
    return result

def multiply(numbers):
    result = 1
    for num in numbers:
        result *= num
    return result

def divide(numbers):
    result = numbers[0]
    try:
        for num in numbers[1:]:
            result /= num
        return result
    except ZeroDivisionError:
        return "Error!: Division by Zero!"

def calculator():
    while True:
        print("\nOptions:")
        print("1: Add")
        print("2: Subtract")
        print("3: Multiply")
        print("4: Divide")
        print("5: Exit")

        choice = input("Choose an operation (1/2/3/4/5): ")

        if choice == '5':
            print("Exiting calculator. Goodbye!")
            break

        numbers_input = input("Enter numbers separated by space: ")
        try:
            numbers = list(map(float, numbers_input.strip().split()))
            if len(numbers) < 2:
                print("Please enter at least two numbers.")
                continue
        except ValueError:
            print("Invalid input! Please enter numeric values only.")
            continue

        if choice == '1':
            print("Result:", add(numbers))
        elif choice == '2':
            print("Result:", subtract(numbers))
        elif choice == '3':
            print("Result:", multiply(numbers))
        elif choice == '4':
            print("Result:", divide(numbers))
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    calculator()
