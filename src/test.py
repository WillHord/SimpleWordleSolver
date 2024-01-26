def waitForInput(default=0):
    def decorator(func):
        def wrapper(*args, **kwargs):
            wrapper.var = [default]  # Use a list to hold the variable
            while True:
                continue_loop = func(*args, var=wrapper.var, **kwargs)
                if not continue_loop:
                    break
            return wrapper.var[0]  # Return the modified value
        return wrapper
    return decorator

@waitForInput(default=0)
def my_function(some_arg, var):
    print("var: ", var[0])
    var[0] += 1  # Modify the first element of the list
    if var[0] == 5:
        return False  # Stop the loop
    return True  # Continue the loop

# Example usage
final_value = my_function("Hello")
print("Final value:", final_value)
