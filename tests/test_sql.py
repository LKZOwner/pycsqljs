import pytest
from pcsj_interpreter import run_pcsj_file

def test_table_creation():
    code = """
    table test_table {
        id: int PRIMARY KEY,
        name: string,
        value: float
    };
    INSERT INTO test_table VALUES (1, "test", 42.5);
    query result = SELECT * FROM test_table WHERE id = 1;
    print(result[0].name);
    """
    result = run_pcsj_file(code)
    assert "test" in result

def test_foreign_key():
    code = """
    table parent {
        id: int PRIMARY KEY,
        name: string
    };
    table child {
        id: int PRIMARY KEY,
        parent_id: int FOREIGN KEY REFERENCES parent(id),
        value: string
    };
    INSERT INTO parent VALUES (1, "parent1");
    INSERT INTO child VALUES (1, 1, "child1");
    query result = SELECT c.value FROM child c JOIN parent p ON c.parent_id = p.id;
    print(result[0].value);
    """
    result = run_pcsj_file(code)
    assert "child1" in result

def test_complex_query():
    code = """
    table employees {
        id: int PRIMARY KEY,
        name: string,
        salary: float,
        dept_id: int
    };
    INSERT INTO employees VALUES 
        (1, "John", 50000, 1),
        (2, "Jane", 60000, 1),
        (3, "Bob", 45000, 2);
    query result = 
        SELECT dept_id, AVG(salary) as avg_salary
        FROM employees
        GROUP BY dept_id
        HAVING AVG(salary) > 50000;
    print(result[0].dept_id);
    """
    result = run_pcsj_file(code)
    assert "1" in result

def test_transaction():
    code = """
    table accounts {
        id: int PRIMARY KEY,
        balance: float
    };
    INSERT INTO accounts VALUES (1, 1000), (2, 500);
    
    async function transfer(fromId, toId, amount) {
        BEGIN TRANSACTION;
        UPDATE accounts SET balance = balance - amount WHERE id = fromId;
        UPDATE accounts SET balance = balance + amount WHERE id = toId;
        COMMIT;
    }
    
    await transfer(1, 2, 200);
    query result = SELECT balance FROM accounts WHERE id = 2;
    print(result[0].balance);
    """
    result = run_pcsj_file(code)
    assert "700" in result

def test_window_functions():
    code = """
    table scores {
        id: int PRIMARY KEY,
        student: string,
        score: int
    };
    INSERT INTO scores VALUES 
        (1, "Alice", 85),
        (2, "Bob", 92),
        (3, "Charlie", 78),
        (4, "David", 85);
    query result = 
        SELECT student, score,
               RANK() OVER (ORDER BY score DESC) as rank
        FROM scores;
    print(result[1].student);  // Should be Alice (tied for 2nd)
    """
    result = run_pcsj_file(code)
    assert "Alice" in result

def test_cte():
    code = """
    table sales {
        id: int PRIMARY KEY,
        product: string,
        amount: float,
        date: datetime
    };
    INSERT INTO sales VALUES 
        (1, "A", 100, "2023-01-01"),
        (2, "B", 200, "2023-01-02"),
        (3, "A", 150, "2023-01-03");
    
    WITH product_totals AS (
        SELECT product, SUM(amount) as total
        FROM sales
        GROUP BY product
    )
    query result = 
        SELECT product, total
        FROM product_totals
        WHERE total > 200;
    print(result[0].product);
    """
    result = run_pcsj_file(code)
    assert "A" in result

def test_error_handling():
    code = """
    table test {
        id: int PRIMARY KEY
    };
    try {
        INSERT INTO test VALUES (1), (1);  // Duplicate key
    } catch (error) {
        print("Error caught");
    }
    """
    result = run_pcsj_file(code)
    assert "Error caught" in result 