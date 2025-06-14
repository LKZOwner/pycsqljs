import math

def run_pcsj():
    # Create environment for variables and functions
    env = {}
    
    # Simulate import
    env['math'] = math
    
    # Define the add function
    def add(a, b):
        return a + b
    env['add'] = add
    
    # Execute variable declarations
    env['x'] = 5
    env['y'] = env['add'](env['x'], 3)
    
    # Execute if/else
    if env['y'] > 5:
        print("y is greater than 5")
    else:
        print("y is not greater than 5")
    
    # Execute for loop
    for i in range(3):
        print(i)
    
    # Execute SQL-like query
    users = [
        {"name": "Alice", "age": 22},
        {"name": "Bob", "age": 17},
        {"name": "Carol", "age": 19}
    ]
    env['users'] = users
    
    # Simulate SQL query
    adults = [user for user in env['users'] if user['age'] >= 18]
    print("\nAdults from SQL query:")
    print(adults)

if __name__ == "__main__":
    print("Running .pcsj file simulation...\n")
    run_pcsj() 