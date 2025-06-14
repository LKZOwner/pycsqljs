import pytest
from pcsj_interpreter import run_pcsj_file, ValidationError

def test_validation_error():
    result = run_pcsj_file("examples/05_error_handling.pcsj")
    assert "Validation failed: Age must be a number" in result

def test_custom_error_class():
    with pytest.raises(ValidationError) as exc_info:
        run_pcsj_file("""
        class ValidationError extends Error {
            constructor(message) {
                super(message);
                this.name = "ValidationError";
            }
        }
        throw new ValidationError("Test error");
        """)
    assert "Test error" in str(exc_info.value)

def test_async_error_handling():
    result = run_pcsj_file("""
    async function test() {
        try {
            throw new Error("Test error");
        } catch (error) {
            return error.message;
        }
    }
    print(test());
    """)
    assert "Test error" in result

def test_finally_block():
    result = run_pcsj_file("""
    let finallyExecuted = false;
    try {
        throw new Error("Test error");
    } catch (error) {
        print(error.message);
    } finally {
        finallyExecuted = true;
        print("Finally block executed");
    }
    print(finallyExecuted);
    """)
    assert "Test error" in result
    assert "Finally block executed" in result
    assert "true" in result 