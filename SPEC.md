# PyCppSQLJS Language Specification (SPEC)

This document outlines the core features and design principles of the PyCppSQLJS programming language.

## 1. Introduction

PyCppSQLJS is a multi-paradigm programming language designed to combine the strengths of C++ (performance, low-level control), Python (readability, rapid development), SQL (data manipulation), and JavaScript (web interactivity, asynchronous programming). It aims to provide a versatile environment for various applications, from system-level programming to web development and data management.

## 2. Core Principles

*   **Hybridity:** Seamless integration of features from its parent languages.
*   **Readability & Expressiveness:** Prioritizing clear and concise code.
*   **Performance (Targeted):** Allowing for performance-critical sections while maintaining ease of use.
*   **Data-Centric:** Strong support for data storage and retrieval.
*   **Concurrency:** Robust asynchronous programming capabilities.

## 3. Lexical Structure

### 3.1. Identifiers

-   Follows Python-like rules: alphanumeric characters and underscores, cannot start with a digit.
-   Case-sensitive.

### 3.2. Keywords

-   Reserved words from C++, Python, SQL, and JavaScript where applicable.
-   Examples: `class`, `def`, `if`, `else`, `while`, `for`, `select`, `from`, `where`, `async`, `await`, `var`, `const`.

### 3.3. Literals

-   **Integers:** `123`, `-45`
-   **Floating-point:** `3.14`, `-0.5`
-   **Strings:** Single (`'hello'`) and double (`"world"`) quotes, template literals (` `This is a ${variable}``).
-   **Booleans:** `true`, `false` (JavaScript-style).
-   **Null:** `null` (JavaScript-style).

### 3.4. Comments

-   Single-line: `// This is a C++-style comment`
-   Multi-line: `/* This is a multi-line comment */`
-   Python-style `#` comments for scripting sections.

## 4. Types

-   **Static Typing (C++ influence):** Optional explicit type declarations for performance-critical sections (e.g., `int x = 10;`).
-   **Dynamic Typing (Python/JavaScript influence):** Default behavior where types are inferred (e.g., `x = 10;`).
-   **Primitive Types:** `int`, `float`, `string`, `bool`, `null`, `void`.
-   **User-Defined Types:** Classes (see Section 6).

## 5. Variables and Scoping

-   **Declaration:** `var`, `const` (JavaScript-style for block-scoping), or implicit assignment (Python-style).
-   **Scope:** Block-scoped for `var`/`const`, function-scoped for Python-style assignments.

## 6. Expressions and Operators

-   Standard arithmetic, comparison, logical operators.
-   Operator precedence largely follows Python/C++ conventions.
-   **Lambda expressions:** `(params) => { ... }` (JavaScript-style).

## 7. Control Flow

-   **Conditional Statements:** `if`, `else if`, `else` (C++/JavaScript-style with curly braces).
-   **Looping Constructs:** `for`, `while` (C++/JavaScript-style).
-   **Exception Handling:** `try`, `catch`, `finally` (JavaScript-style).

## 8. Functions

-   **Definition:** `def function_name(params):` (Python-style) or `function functionName(params) { ... }` (JavaScript-style for async/web contexts).
-   **Return Types:** Optional explicit return types (C++-style).
-   **Anonymous Functions:** See Lambda expressions.

## 9. Classes and Objects

-   **Class Definition:** `class ClassName { ... }` (C++/JavaScript-style).
-   **Constructors:** `constructor() { ... }` (JavaScript-style).
-   **Methods:** Defined within class body.
-   **Inheritance:** Single inheritance using `extends` (JavaScript-style).
-   **Access Modifiers (Simulated):** Public by default. Private/protected via conventions.

## 10. Modules and Imports

-   **Import Mechanism:** `import module_name` or `from module_name import item` (Python-style).
-   Modules represent `.pcsj` files.

## 11. SQL-like Queries

-   **Embedded SQL:** Direct SQL-like syntax within PyCppSQLJS code.
-   **Keywords:** `SELECT`, `FROM`, `WHERE`, `INSERT`, `UPDATE`, `DELETE`.
-   **Examples:**
    ```pcsj
    query result = SELECT name, age FROM users WHERE age > 25;
    ```

## 12. Asynchronous Programming (JavaScript Influence)

-   **Keywords:** `async`, `await`.
-   **Event Loop:** Conceptual event loop for handling non-blocking operations.
-   **Promises/Futures:** Simulated in the interpreter.

## 13. Native Interoperability (C++ Influence)

-   **External Function Calls:** Mechanisms to call functions from C++ libraries (simulated).
-   **DLL/Shared Library Loading:** Conceptual support.

## 14. Error Handling

-   **Exceptions:** `throw` (C++/JavaScript-style).
-   **Try-Catch Blocks:** See Section 7.

## 15. The Interpreter/Simulator

-   The initial implementation is a Python-based simulator (`pcsj_interpreter.py`).
-   Translates and executes `.pcsj` code by mapping PyCppSQLJS constructs to Python equivalents.

## 16. Future Considerations

-   Just-In-Time (JIT) compilation for performance.
-   Garbage collection optimization.
-   Formal grammar definition.
-   Standard library expansion. 