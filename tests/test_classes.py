import pytest
from pcsj_interpreter import run_pcsj_file

def test_class_inheritance():
    result = run_pcsj_file("examples/04_classes.pcsj")
    assert "Generic is a Unknown" in result
    assert "Generic makes a sound" in result
    assert "Buddy is a Dog" in result
    assert "Buddy barks!" in result
    assert "Buddy fetches the ball" in result

def test_static_methods():
    result = run_pcsj_file("examples/04_classes.pcsj")
    assert "8" in result  # Both add(5,3) and multiply(4,2) should output 8

def test_class_instantiation():
    code = """
    class Test {
        constructor(value) {
            this.value = value;
        }
        getValue() {
            return this.value;
        }
    }
    const test = new Test("test");
    print(test.getValue());
    """
    result = run_pcsj_file(code)
    assert "test" in result 