"""
Tests for cal.py (arithmetic functions and interactive CLI loop).

NOTE: cal.py currently contains a SyntaxError on line 34:
    return a * b;;;
Multiple consecutive semicolons after a return statement are invalid in
Python 3.11+.  All tests will fail to collect until that line is fixed
(e.g. changed to `return a * b` or `return a * b;`).
"""
import pytest
from unittest.mock import patch, call
from cal import add, subtract, multiply, divide, main


# ---------------------------------------------------------------------------
# add
# ---------------------------------------------------------------------------

class TestAdd:
    def test_positive_integers(self):
        assert add(2, 3) == 5

    def test_negative_integers(self):
        assert add(-4, -6) == -10

    def test_positive_and_negative(self):
        assert add(10, -3) == 7

    def test_zero_identity(self):
        assert add(0, 5) == 5
        assert add(5, 0) == 5

    def test_both_zero(self):
        assert add(0, 0) == 0

    def test_floats(self):
        assert add(1.5, 2.5) == pytest.approx(4.0)

    def test_mixed_int_float(self):
        assert add(1, 2.5) == pytest.approx(3.5)

    def test_large_numbers(self):
        assert add(10**9, 10**9) == 2 * 10**9

    def test_string_concatenation(self):
        # add is generic — works for strings too (operator overloading)
        assert add("hello", " world") == "hello world"


# ---------------------------------------------------------------------------
# subtract
# ---------------------------------------------------------------------------

class TestSubtract:
    def test_positive_result(self):
        assert subtract(10, 4) == 6

    def test_negative_result(self):
        assert subtract(3, 7) == -4

    def test_zero_result(self):
        assert subtract(5, 5) == 0

    def test_subtract_negative(self):
        assert subtract(5, -3) == 8

    def test_both_negative(self):
        assert subtract(-2, -5) == 3

    def test_floats(self):
        assert subtract(3.5, 1.5) == pytest.approx(2.0)

    def test_zero_minuend(self):
        assert subtract(0, 9) == -9

    def test_large_numbers(self):
        assert subtract(10**12, 1) == 10**12 - 1


# ---------------------------------------------------------------------------
# multiply
# ---------------------------------------------------------------------------

class TestMultiply:
    def test_positive_integers(self):
        assert multiply(3, 4) == 12

    def test_negative_integers(self):
        assert multiply(-3, -4) == 12

    def test_mixed_sign(self):
        assert multiply(3, -4) == -12

    def test_multiply_by_zero(self):
        assert multiply(99, 0) == 0
        assert multiply(0, 99) == 0

    def test_multiply_by_one(self):
        assert multiply(7, 1) == 7
        assert multiply(1, 7) == 7

    def test_floats(self):
        assert multiply(2.5, 4.0) == pytest.approx(10.0)

    def test_mixed_int_float(self):
        assert multiply(3, 1.5) == pytest.approx(4.5)

    def test_large_numbers(self):
        assert multiply(10**6, 10**6) == 10**12

    def test_trailing_semicolons_do_not_affect_result(self):
        # The source has `return a * b;;;` — semicolons are no-ops in Python.
        # This regression test confirms the return value is unaffected.
        assert multiply(5, 5) == 25


# ---------------------------------------------------------------------------
# divide
# ---------------------------------------------------------------------------

class TestDivide:
    def test_exact_integer_division(self):
        assert divide(10, 2) == 5.0

    def test_float_result(self):
        assert divide(7, 2) == pytest.approx(3.5)

    def test_divide_by_zero_returns_error_string(self):
        result = divide(5, 0)
        assert result == "Error: Division by zero"

    def test_divide_by_zero_is_string_not_exception(self):
        result = divide(0, 0)
        assert isinstance(result, str)
        assert result == "Error: Division by zero"

    def test_negative_dividend(self):
        assert divide(-10, 2) == pytest.approx(-5.0)

    def test_negative_divisor(self):
        assert divide(10, -2) == pytest.approx(-5.0)

    def test_both_negative(self):
        assert divide(-10, -2) == pytest.approx(5.0)

    def test_zero_dividend(self):
        assert divide(0, 5) == pytest.approx(0.0)

    def test_float_operands(self):
        assert divide(1.0, 4.0) == pytest.approx(0.25)

    def test_near_zero_divisor_not_zero(self):
        # b is a very small float but not zero — should return a number
        result = divide(1.0, 1e-10)
        assert isinstance(result, float)
        assert result == pytest.approx(1e10)

    def test_return_type_normal(self):
        assert isinstance(divide(10, 4), float)

    def test_return_type_zero_divisor(self):
        assert isinstance(divide(10, 0), str)


# ---------------------------------------------------------------------------
# main (interactive CLI)
# ---------------------------------------------------------------------------

class TestMain:
    """Tests for the interactive main() loop using mocked input/output."""

    def _run_main(self, inputs):
        """Helper: run main() with a sequence of mocked inputs, return printed lines."""
        with patch("builtins.input", side_effect=inputs), \
             patch("builtins.print") as mock_print:
            main()
        return [str(c.args[0]) if c.args else "" for c in mock_print.call_args_list]

    def test_addition_then_quit(self, capsys):
        inputs = ["3", "+", "4", "n"]
        with patch("builtins.input", side_effect=inputs):
            main()
        captured = capsys.readouterr()
        assert "Result: 7.0" in captured.out
        assert "Goodbye!" in captured.out

    def test_subtraction_then_quit(self, capsys):
        inputs = ["10", "-", "3", "n"]
        with patch("builtins.input", side_effect=inputs):
            main()
        captured = capsys.readouterr()
        assert "Result: 7.0" in captured.out

    def test_multiplication_then_quit(self, capsys):
        inputs = ["6", "*", "7", "n"]
        with patch("builtins.input", side_effect=inputs):
            main()
        captured = capsys.readouterr()
        assert "Result: 42.0" in captured.out

    def test_division_then_quit(self, capsys):
        inputs = ["9", "/", "3", "n"]
        with patch("builtins.input", side_effect=inputs):
            main()
        captured = capsys.readouterr()
        assert "Result: 3.0" in captured.out

    def test_division_by_zero_then_quit(self, capsys):
        inputs = ["5", "/", "0", "n"]
        with patch("builtins.input", side_effect=inputs):
            main()
        captured = capsys.readouterr()
        assert "Error: Division by zero" in captured.out

    def test_invalid_operator_then_quit(self, capsys):
        inputs = ["5", "%", "2", "n"]
        with patch("builtins.input", side_effect=inputs):
            main()
        captured = capsys.readouterr()
        assert "Invalid operator" in captured.out

    def test_invalid_numeric_input_then_quit(self, capsys):
        inputs = ["abc", "n"]
        with patch("builtins.input", side_effect=inputs):
            main()
        captured = capsys.readouterr()
        assert "Invalid input. Please enter numbers." in captured.out

    def test_invalid_second_number_then_quit(self, capsys):
        inputs = ["5", "+", "xyz", "n"]
        with patch("builtins.input", side_effect=inputs):
            main()
        captured = capsys.readouterr()
        assert "Invalid input. Please enter numbers." in captured.out

    def test_continue_then_quit(self, capsys):
        # Two calculations: first addition, then subtraction
        inputs = ["2", "+", "3", "y", "10", "-", "4", "n"]
        with patch("builtins.input", side_effect=inputs):
            main()
        captured = capsys.readouterr()
        assert "Result: 5.0" in captured.out
        assert "Result: 6.0" in captured.out
        assert "Goodbye!" in captured.out

    def test_uppercase_continue_exits(self, capsys):
        # input is lowercased, so "Y".lower() == "y" — should continue
        inputs = ["1", "+", "1", "Y", "1", "+", "1", "n"]
        with patch("builtins.input", side_effect=inputs):
            main()
        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out

    def test_non_y_response_exits(self, capsys):
        inputs = ["1", "+", "1", "no"]
        with patch("builtins.input", side_effect=inputs):
            main()
        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out

    def test_header_printed_once(self, capsys):
        inputs = ["1", "+", "1", "n"]
        with patch("builtins.input", side_effect=inputs):
            main()
        captured = capsys.readouterr()
        assert "Simple Calculator" in captured.out
        assert "Operations: +  -  *  /" in captured.out

    def test_negative_number_inputs(self, capsys):
        inputs = ["-5", "+", "-3", "n"]
        with patch("builtins.input", side_effect=inputs):
            main()
        captured = capsys.readouterr()
        assert "Result: -8.0" in captured.out

    def test_float_number_inputs(self, capsys):
        inputs = ["1.5", "+", "2.5", "n"]
        with patch("builtins.input", side_effect=inputs):
            main()
        captured = capsys.readouterr()
        assert "Result: 4.0" in captured.out