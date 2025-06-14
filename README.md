# PyCppSQLJS

A modern, multi-paradigm programming language that combines the best features of C++, Python, SQL, and JavaScript.

## 🌟 Features

- **Hybrid Language Design**: Seamlessly combines features from C++, Python, SQL, and JavaScript
- **Multi-Paradigm Support**: Object-oriented, functional, and procedural programming
- **SQL Integration**: Native SQL-like query syntax
- **Async/Await**: Modern asynchronous programming support
- **Type System**: Optional static typing with dynamic type inference
- **Cross-Platform**: Runs on Windows, Linux, and macOS
- **Modern Tooling**: VS Code/Cursor integration with syntax highlighting

## 🚀 Quick Start

1. **Installation**:
   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/PyCppSQLJS.git
   cd PyCppSQLJS

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Run Your First Program**:
   Create a file `hello.pcsj`:
   ```pcsj
   // Hello World in PyCppSQLJS
   print("Hello, World!");

   // Using SQL-like syntax
   query users = SELECT name, age FROM users WHERE age > 18;

   // Async example
   async function fetchData() {
       const data = await http.get("https://api.example.com/data");
       return data;
   }
   ```

   Run it:
   ```bash
   python pcsj_interpreter.py hello.pcsj
   ```

## 📚 Documentation

- [Language Specification](SPEC.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Changelog](CHANGELOG.md)

## 🛠️ Development

### Prerequisites

- Python 3.8+
- Git
- VS Code or Cursor IDE

### Project Structure

```
PyCppSQLJS/
├── pcsj_interpreter.py    # Main interpreter
├── examples/             # Example programs
├── tests/               # Test suite
├── docs/                # Documentation
└── .vscode/            # VS Code/Cursor settings
```

### Running Tests

```bash
python -m pytest tests/
```

## 🤝 Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by C++, Python, SQL, and JavaScript
- Built with Python
- Thanks to all contributors and the open-source community

## 📞 Contact

For questions, suggestions, or collaborations, feel free to reach out:

- **GitHub**: [LKZOwner](https://github.com/LKZOwner)
- **Email**: [linn72827@gmail.com](mailto:linn72827@gmail.com)

## 🌟 Star the Project

If you find this project useful, please give it a star on GitHub!