# Getting Started with PyCppSQLJS

This guide will help you get started with PyCppSQLJS, from installation to writing your first program.

## Installation

1. **Prerequisites**
   - Python 3.8 or higher
   - Git
   - A code editor (VS Code or Cursor recommended)

2. **Installation Steps**
   ```bash
   # Clone the repository
   git clone https://github.com/LKZ_Owner/PyCppSQLJS.git
   cd PyCppSQLJS

   # Create a virtual environment (recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

## Your First Program

1. **Create a new file** named `hello.pcsj`:
   ```pcsj
   // Hello World in PyCppSQLJS
   print("Hello, World!");

   // Variables and type inference
   name = "PyCppSQLJS";
   age = 1;
   print(`Welcome to ${name} version ${age}!`);
   ```

2. **Run the program**:
   ```bash
   python pcsj_interpreter.py hello.pcsj
   ```

## Basic Syntax

### Variables and Types
```pcsj
// Type inference
x = 10;          // int
y = 3.14;        // float
name = "John";   // string
isActive = true; // boolean

// Explicit typing (optional)
int count = 5;
string message = "Hello";
```

### Control Flow
```pcsj
// If statements
if (age >= 18) {
    print("Adult");
} else if (age >= 13) {
    print("Teenager");
} else {
    print("Child");
}

// Loops
for (let i = 0; i < 5; i++) {
    print(i);
}

while (count > 0) {
    print(count);
    count--;
}
```

### Functions
```pcsj
// Function definition
function greet(name) {
    return `Hello, ${name}!`;
}

// Arrow function
const add = (a, b) => a + b;

// Async function
async function fetchData() {
    const data = await http.get("https://api.example.com/data");
    return data;
}
```

### SQL Integration
```pcsj
// Create a table
table users {
    id: int,
    name: string,
    age: int
};

// Insert data
INSERT INTO users VALUES (1, "John", 25);

// Query data
query result = SELECT name, age FROM users WHERE age > 20;
```

## Next Steps

1. **Explore Examples**
   - Check out the `examples/` directory for more code samples
   - Try modifying the examples to learn different features

2. **Read Documentation**
   - [Language Specification](SPEC.md)
   - [API Reference](docs/api_reference.md)
   - [Best Practices](docs/best_practices.md)

3. **Join the Community**
   - Report bugs or request features on [GitHub Issues](https://github.com/LKZ_Owner/PyCppSQLJS/issues)
   - Contribute to the project (see [CONTRIBUTING.md](CONTRIBUTING.md))

## Common Issues

1. **Interpreter not found**
   - Make sure you're in the correct directory
   - Verify that `pcsj_interpreter.py` exists
   - Check Python installation

2. **Syntax errors**
   - Use proper semicolons at the end of statements
   - Check for matching braces and parentheses
   - Verify string quotes are properly closed

3. **Runtime errors**
   - Check variable names for typos
   - Verify function parameters
   - Ensure proper error handling

## Getting Help

- Check the [FAQ](docs/faq.md)
- Search [GitHub Issues](https://github.com/LKZ_Owner/PyCppSQLJS/issues)
- Email: linn72827@gmail.com 