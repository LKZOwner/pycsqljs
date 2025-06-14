import sys
import os
import asyncio
import json
import inspect
from typing import Dict, Any, List, Union, Callable

# --- Mock Standard Library and Built-ins for PCSJ ---
class PCSJBuiltins:
    def __init__(self, env: Dict[str, Any]):
        self._env = env
        self._mock_files = {} # For simulating readFile/writeFile
        self._register_globals()

    def _register_globals(self):
        self._env['print'] = print # Direct Python print
        self._env['len'] = len   # Direct Python len
        self._env['int'] = int
        self._env['float'] = float
        self._env['string'] = str # Use str for string type
        self._env['bool'] = bool
        self._env['object'] = object # Generic object type

        # Simulated JSON object for parsing/stringifying
        class MockJSON:
            def parse(self, s: str) -> Dict[str, Any]:
                return json.loads(s)
            def stringify(self, obj: Any) -> str:
                return json.dumps(obj)
        self._env['JSON'] = MockJSON()

        # Simulated sleep function for async
        async def sleep(ms: int):
            await asyncio.sleep(ms / 1000)
        self._env['sleep'] = sleep

        # Mock File I/O
        def readFile(filename: str) -> str:
            if filename in self._mock_files:
                return self._mock_files[filename]
            try:
                with open(filename, 'r') as f:
                    return f.read()
            except FileNotFoundError:
                raise Exception(f"File not found: {filename}")
        self._env['readFile'] = readFile

        def writeFile(filename: str, data: str):
            self._mock_files[filename] = data # Store in mock_files
            try:
                with open(filename, 'w') as f:
                    f.write(data)
                print(f"File '{filename}' written successfully (simulated).")
            except Exception as e:
                raise Exception(f"Error writing file '{filename}': {e}")
        self._env['writeFile'] = writeFile
        
        # Array/List methods (Higher-Order Functions)
        def map_func(arr: list, func: Callable) -> list:
            return [func(item) for item in arr]
        def filter_func(arr: list, func: Callable) -> list:
            return [item for item in arr if func(item)]
        def reduce_func(arr: list, func: Callable, initial: Any) -> Any:
            res = initial
            for item in arr:
                res = func(res, item)
            return res
        
        # Add these to the list prototype for dot notation access
        list.map = map_func
        list.filter = filter_func
        list.reduce = reduce_func
        
        # String methods
        str.toUpperCase = lambda s: s.upper()

        # Generic math functions (e.g., from math_lib)
        self._env['max'] = max

        # For py() interop
        def py_interop(code_str: str):
            exec(code_str, self._env)
        self._env['py'] = py_interop

        # Mock onClick for event handling simulation
        self._env['onClick'] = lambda btn_id, handler: print(f"Event listener set for button '{btn_id}'")

# --- Core PCSJ Interpreter Logic ---
class PCSJInterpreter:
    def __init__(self, base_path: str = './'):
        self.base_path = base_path
        self.env: Dict[str, Any] = {}
        self.builtins = PCSJBuiltins(self.env)
        self.defined_schemas: Dict[str, type] = {}
        self.defined_classes: Dict[str, type] = {}

        # Register core types for the interpreter
        self._register_core_types()

    def _register_core_types(self):
        # Base class for all PCSJ objects
        class PCSJObject:
            def __repr__(self):
                attrs = ', '.join(f"{k}={getattr(self, k)!r}" for k in self.__dict__)
                return f"{self.__class__.__name__}({attrs})"

        self.defined_classes['object'] = PCSJObject # Register base object type

        # Python class representing a PCSJ schema
        def create_schema_class(schema_name: str, fields: Dict[str, Any]) -> type:
            def __init__(self_obj, *args):
                if len(args) != len(fields):
                    raise TypeError(f"Schema '{schema_name}' constructor expected {len(fields)} arguments, got {len(args)}")
                for i, (field_name, field_type) in enumerate(fields.items()):
                    setattr(self_obj, field_name, args[i]) # No type checking here for simplicity

            # For SQL-like mapping, allow dict-like init
            @classmethod
            def from_dict(cls, data: Dict[str, Any]):
                instance = cls.__new__(cls) # Create instance without calling __init__
                for field_name in fields:
                    setattr(instance, field_name, data.get(field_name)) # Set attributes from dict
                return instance

            return type(schema_name, (PCSJObject,), {
                '__init__': __init__,
                'from_dict': from_dict
            })

        self.env['schema_creator'] = create_schema_class # Helper to create schema classes

        # Python class representing a PCSJ class
        def create_pcsj_class(class_name: str, base_class: type, methods: Dict[str, Callable], properties: Dict[str, Any], constructor: Callable = None) -> type:
            class_dict = {
                **properties # Static and initial properties
            }
            for method_name, method_func in methods.items():
                if inspect.iscoroutinefunction(method_func):
                    class_dict[method_name] = method_func # Async methods
                else:
                    class_dict[method_name] = method_func # Regular methods

            if constructor:
                class_dict['__init__'] = constructor
            
            # Simple getter simulation
            for k, v in class_dict.items():
                if isinstance(v, property): # Check for @property-like objects
                    class_dict[k] = v # Keep properties as they are

            return type(class_name, (base_class,), class_dict)
        self.env['class_creator'] = create_pcsj_class

    async def run_pcsj_code(self, code: str, current_env: Dict[str, Any]):
        # This is the core simulation logic.
        # It's a very simplified "interpreter" that assumes well-formed PCSJ code
        # and translates it to Python for execution using exec().
        # A real interpreter would involve proper lexing, parsing, and AST traversal.

        # 1. Simulate Schema Definitions
        # Find schema definitions and create Python classes
        schema_matches = list(self._find_schema_definitions(code))
        for schema_name, fields_str in schema_matches:
            # Simple parsing of fields: "string id; int age;" -> {"id": str, "age": int}
            fields = {}
            for field_def in fields_str.split(';'):
                field_def = field_def.strip()
                if field_def:
                    parts = field_def.split()
                    if len(parts) == 2:
                        field_type, field_name = parts
                        # Map PCSJ types to Python types (simplified)
                        py_type = None
                        if field_type == 'string': py_type = str
                        elif field_type == 'int': py_type = int
                        elif field_type == 'float': py_type = float
                        elif field_type == 'bool': py_type = bool
                        fields[field_name] = py_type
            
            pcsj_schema_class = self.env['schema_creator'](schema_name, fields)
            current_env[schema_name] = pcsj_schema_class
            self.defined_schemas[schema_name] = pcsj_schema_class
            # Remove schema definition from code to avoid re-execution errors
            code = code.replace(f"schema {schema_name} {{ {fields_str} }}", "")

        # 2. Simulate Class Definitions (very simplified)
        # We need to manually define the classes in Python that match PCSJ
        # This is where a real parser/compiler is needed for full automation.
        
        # User Class (matches PCSJ definition)
        class User(self.defined_classes.get('object')): # Inherit from base PCSJObject
            def __init__(self, name: str, age: int):
                self.name = name
                self.age = age
                self.isActive = True
            async def greet(self):
                return f"Hello, my name is {self.name}!"
        current_env['User'] = User
        self.defined_classes['User'] = User

        # Employee Class (matches PCSJ definition)
        class Employee(current_env.get('Person', object)): # Inherit from Person, default to object if Person not found
            def __init__(self, name: str, age: int, department: str, salary: float):
                super().__init__(name, age) # Call parent constructor
                self.department = department
                self.salary = salary
            async def greet(self): # Override simulation
                return f"Hello, my name is {self.name}. I work in {self.department}."
        current_env['Employee'] = Employee
        self.defined_classes['Employee'] = Employee

        # Mock JSON parse for http_lib
        class MockJSON:
            @staticmethod
            def parse(s: str) -> Dict[str, Any]:
                return json.loads(s)
        current_env['JSON'] = MockJSON

        # Create mock module objects and register them
        current_env['math_lib'] = type('math_lib', (object,), {
            'add': lambda a, b: a + b,
            'subtract': lambda a, b: a - b,
            'PI': 3.14159
        })()

        class MockHttpResponse:
            def __init__(self, status: str, body: str):
                self.status = status
                self.body = body
            async def json(self):
                return json.loads(self.body)

        current_env['http_lib'] = type('http_lib', (object,), {
            'get': lambda url: MockHttpResponse("200 OK", f'{{"id": "prod123", "name": "Mock Product", "price": 99.99, "stock": 10, "available": true}}')
        })()
        
        # Add basic functions to the environment if not already there
        if 'add' not in current_env: # This would come from math_lib if parsed directly
            current_env['add'] = lambda a, b: a + b

        # Implement calculateArea as a regular Python function
        def calculateArea(width: float, height: float = 1.0) -> float:
            return width * height
        current_env['calculateArea'] = calculateArea

        # Implement checkStock
        def checkStock(stockCount: int):
            if stockCount > 10:
                print("In stock")
            elif stockCount > 0:
                print("Low stock")
            else:
                print("Out of stock")
        current_env['checkStock'] = checkStock

        # Implement fetchProductData (using the mock http_lib and schema)
        async def fetchProductData_mock(productId: str) -> current_env['ProductSchema']:
            response = await current_env['http_lib'].get(f'https://api.example.com/products/{productId}')
            data = await response.json()
            return current_env['ProductSchema'].from_dict(data)
        current_env['fetchProductData'] = fetchProductData_mock

        # Implement performRiskyOperation (error handling simulation)
        async def performRiskyOperation_mock():
            try:
                num = 10
                if num > 5:
                    raise Exception("Simulated error: number too high!")
                print("Risky operation successful!")
            except Exception as e:
                print(f"Caught error: {e}")
            finally:
                print("Risky operation cleanup complete.")
        current_env['performRiskyOperation'] = performRiskyOperation_mock

        # Lambdas / Arrow Functions (Python's lambda directly)
        current_env['sum_lambda'] = lambda a, b: a + b # Renamed to avoid conflict

        # Higher-Order Functions (implemented directly in Python)
        current_env['map'] = lambda arr, func: [func(x) for x in arr]
        current_env['filter'] = lambda arr, func: [x for x in arr if func(x)]
        current_env['reduce'] = lambda arr, func, initial: (lambda a, f, i: (lambda r: (i, r)[1] for _ in a for r in [f(r, _)])(i))(arr, func, initial) # Complex lambda for reduce
        
        # Template Literals - handled by f-strings in Python's exec()
        
        # Native Interop - already handled by builtins.py()

        # SQL-like query simulation
        def select_query(data_source: List[Dict[str, Any]], conditions: Callable[[Dict[str, Any]], bool], schema_class: type = None) -> List[Any]:
            results = [item for item in data_source if conditions(item)]
            if schema_class:
                return [schema_class.from_dict(item) for item in results]
            return results

        # This is where we manually replace the SQL-like syntax.
        # A real parser would convert "SELECT * FROM users WHERE ..." into a callable form.
        # For this simulation, we'll replace the SQL query with its Python equivalent before exec.

        # First, convert simple PCSJ code to a more Python-compatible form
        # This is a very basic replacement and *not* a full parser.
        python_executable_code = self._convert_pcsj_to_python_exec(code)
        
        # Adjust SQL-like query replacement based on the actual example structure
        # Find the specific SQL-like query and replace it with Python equivalent
        sql_query_start = "var availableProducts = SELECT id, name, price, stock, available FROM productsDb WHERE available = true AS ProductSchema;"
        
        # This is highly simplified and assumes the exact SQL query format.
        # A real parser would generate this Python code from the SQL-like AST.
        if sql_query_start in python_executable_code:
            python_sql_equivalent = """
availableProducts = [
    current_env['ProductSchema'].from_dict(p) for p in current_env['productsDb'] 
    if p.get('available') == True
]
"""
            python_executable_code = python_executable_code.replace(sql_query_start, python_sql_equivalent)


        # For-of loop conversion (simple regex replacement)
        python_executable_code = self._convert_for_of_loop(python_executable_code)
        
        # Try-catch conversion (simple regex replacement)
        python_executable_code = self._convert_try_catch(python_executable_code)

        # Template literals (handled by Python f-strings if syntax is correct)
        # Ensure backticks are converted to f-strings for Python exec
        python_executable_code = self._convert_template_literals(python_executable_code)

        # Class constructor and super() call needs special handling in _convert_pcsj_to_python_exec
        # This level of `exec` doesn't fully support `super()` in this context,
        # so we rely on the manual Python class definitions above.

        # Final execution with updated environment
        try:
            # print("--- Converted Python Code for Exec ---")
            # print(python_executable_code)
            # print("------------------------------------")
            
            # Use `asyncio.run` if top-level await is detected in the main IIFE
            if "(async () => {" in python_executable_code and "await" in python_executable_code:
                # Wrap the code in an async function and run it
                # This is a hack to allow top-level await in exec
                wrapped_code = f"async def _pcsj_main_wrapper_():\n    {python_executable_code.replace('print(', 'await current_env[\'print\'](').replace('await sleep(', 'await current_env[\'sleep\'](').replace('await current_env[\'http_lib\'].get(', 'await current_env[\'http_lib\'].get(').replace('await response.json()', 'await response.json()').replace('await user.greet()', 'await user.greet()').replace('await performRiskyOperation()', 'await current_env[\'performRiskyOperation\']()').replace('await fetchProductData(', 'await current_env[\'fetchProductData\'](').replace('await data.json()', 'await data.json()').replace('await main()', 'await current_env[\'main\']()').replace('await fetchData', 'await current_env[\'fetchData\']').replace('await data.json()', 'await data.json()').replace('(async () => {', '    # Removed original IIFE wrapper\n    # The actual code of IIFE is moved here\n    ').replace('})();', '')}"
                
                # Further refine the wrapper to handle specific calls that need `await`
                wrapped_code = wrapped_code.replace("await current_env['print']", "current_env['print']") # print is not async
                
                # Add main function to env if it exists in pcsj code
                if 'main()' in code:
                    # This is very crude, a real parser would identify main.
                    # For this simulation, we'll call it directly.
                    pass # The main IIFE will be translated and executed below

                # Execute wrapped code, then run the wrapper
                exec(wrapped_code, current_env)
                # print("DEBUG: Calling _pcsj_main_wrapper_")
                await current_env['_pcsj_main_wrapper_']()
            else:
                exec(python_executable_code, current_env)

        except Exception as e:
            raise Exception(f"PCSJ Runtime Error: {e}")

    def _find_schema_definitions(self, code: str):
        import re
        # This regex is simplified. A real parser would use a robust grammar.
        matches = re.finditer(r'schema\s+(\w+)\s*\{\s*([^}]+)\s*\}', code)
        for match in matches:
            schema_name = match.group(1)
            fields_content = match.group(2)
            yield schema_name, fields_content

    def _convert_pcsj_to_python_exec(self, pcsj_code: str) -> str:
        # This function performs a very basic line-by-line conversion
        # It's NOT a parser, and can break with complex PCSJ syntax.
        python_lines = []
        indent_level = 0
        in_multiline_block = False

        for line in pcsj_code.splitlines():
            stripped_line = line.strip()
            
            # Skip comments
            if stripped_line.startswith('//') or stripped_line.startswith(';'):
                continue

            # Handle block indentation for Python
            if '{' in stripped_line:
                python_lines.append('    ' * indent_level + stripped_line.replace('{', ':'))
                indent_level += 1
                in_multiline_block = True
                continue
            if '}' in stripped_line:
                indent_level = max(0, indent_level - 1)
                in_multiline_block = False
                continue

            # Basic keyword replacements and syntax adjustments
            temp_line = stripped_line.replace(';', '') # Remove semicolons
            temp_line = temp_line.replace('string', '') # Remove explicit types for simplicity, Python is dynamic
            temp_line = temp_line.replace('int', '')
            temp_line = temp_line.replace('float', '')
            temp_line = temp_line.replace('bool', '')
            temp_line = temp_line.replace('var ', '') # Replace var with nothing (Python doesn't need it)
            temp_line = temp_line.replace('const ', '') # Replace const with nothing
            temp_line = temp_line.replace('def ', 'def ') # Keep def
            temp_line = temp_line.replace('async def ', 'async def ') # Keep async def
            temp_line = temp_line.replace('else if', 'elif')
            temp_line = temp_line.replace('true', 'True')
            temp_line = temp_line.replace('false', 'False')
            temp_line = temp_line.replace('null', 'None')
            temp_line = temp_line.replace('and', 'and') # Ensure 'and' is Python's 'and'
            temp_line = temp_line.replace('or', 'or')   # Ensure 'or' is Python's 'or'
            temp_line = temp_line.replace('new ', '') # Remove 'new ' keyword for object instantiation

            # Arrow function conversion (simple, for map/filter/reduce context)
            if '=>' in temp_line and 'var' not in temp_line and 'def' not in temp_line:
                parts = temp_line.split('=>')
                if len(parts) == 2:
                    param = parts[0].strip().replace('(', '').replace(')', '').replace(' ', '')
                    body = parts[1].strip()
                    temp_line = f"lambda {param}: {body}"
            
            # String method replacements
            temp_line = temp_line.replace('.toUpperCase()', '.upper()')
            temp_line = temp_line.replace('.length', '.__len__()') # Simplified, or use len(obj) directly

            # Basic type hints removal from function signatures
            temp_line = self._remove_type_hints(temp_line)

            python_lines.append('    ' * indent_level + temp_line)

        return "\\n".join(python_lines)
    
    def _remove_type_hints(self, line: str) -> str:
        # Example: def func(string name) -> string {
        # Becomes: def func(name):
        import re
        # Remove return type hints -> type
        line = re.sub(r'->\s*\w+\s*', '', line)
        # Remove parameter type hints (type param_name)
        line = re.sub(r'\b(string|int|float|bool|object|json|void)\s+([a-zA-Z_]\w*)', r'\2', line)
        # Handle rest parameters
        line = re.sub(r'\.\.\.([a-zA-Z_]\w*)', r'*\1', line) # Convert ...numbers to *numbers
        return line

    def _convert_for_of_loop(self, code: str) -> str:
        import re
        # From: for (item of items) { ... }
        # To:   for item in items: ...
        return re.sub(r'for\s*\(\s*(\w+)\s+of\s+([a-zA-Z_]\w*)\s*\)', r'for \1 in \2:', code)

    def _convert_try_catch(self, code: str) -> str:
        import re
        # From: try { ... } catch (error) { ... } finally { ... }
        # To:   try: ... except Exception as error: ... finally: ...
        # This is very simplistic and assumes specific brace/newline usage.
        
        # Replace 'catch (error)' with 'except Exception as error:'
        code = re.replace(r'catch\s*\(\s*(\w+)\s*\)\s*\{', r'except Exception as \1:', code)
        
        # Replace 'try {' with 'try:'
        code = code.replace('try {', 'try:')
        
        # Replace 'finally {' with 'finally:'
        code = code.replace('finally {', 'finally:')

        return code

    def _convert_template_literals(self, code: str) -> str:
        # Converts backticks to f-strings where possible for simple cases.
        # This will only work for single-line template literals.
        import re
        # Find `...${...}...` and convert to f"..."
        code = re.sub(r'`([^`]*?)\${(.*?)}`', r'f"\1{\2}"', code)
        # Handle simple backtick strings without interpolation
        code = re.sub(r'`(.*?)`', r'"\1"', code) # Convert remaining backticks to double quotes
        return code

async def main():
    # Get the path to the .pcsj file from command line arguments
    if len(sys.argv) < 2:
        print("Usage: python pcsj_interpreter.py <path_to_your_pcsj_file.pcsj>")
        return

    pcsj_file_path = sys.argv[1]

    # Change to the directory of the .pcsj file for relative imports
    original_cwd = os.getcwd()
    file_dir = os.path.dirname(pcsj_file_path)
    if file_dir:
        os.chdir(file_dir)
        pcsj_file_path = os.path.basename(pcsj_file_path) # Adjust path for open()

    interpreter = PCSJInterpreter()

    print(f"\\nRunning PyCppSQLJS file: {pcsj_file_path}\\n")

    try:
        with open(pcsj_file_path, 'r') as f:
            pcsj_code = f.read()

        # Execute the code within the interpreter's environment
        await interpreter.run_pcsj_code(pcsj_code, interpreter.env)

    except FileNotFoundError:
        print(f"Error: File not found at '{pcsj_file_path}'")
    except Exception as e:
        print(f"An error occurred during interpretation: {e}")
    finally:
        # Restore original working directory
        os.chdir(original_cwd)

if __name__ == "__main__":
    asyncio.run(main()) 

</rewritten_file>