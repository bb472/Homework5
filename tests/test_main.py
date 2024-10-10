from unittest.mock import patch
import pytest
from decimal import Decimal
from main import calculate_and_print, OperationCommand, main, repl
import sys
from io import StringIO


@pytest.mark.parametrize("a_input, b_input, operation, expected_output", [
    ("5", "3", 'add', "The result of 5 add 3 is 8"),
    ("10", "2", 'subtract', "The result of 10 subtract 2 is 8"),
    ("4", "5", 'multiply', "The result of 4 multiply 5 is 20"),
    ("20", "4", 'divide', "The result of 20 divide 4 is 5"),
    ("a", "3", 'add', "Invalid number input: a or 3 is not a valid number."),
    ("10", "0", 'divide', "Error: Division by zero."), 
    ("5", None, 'unknown', "Unknown operation: unknown"),
])
def test_calculate_and_print(capsys, a_input, b_input, operation, expected_output):
    calculate_and_print(a_input, b_input, operation, use_multiprocessing=False)
    captured = capsys.readouterr()
    assert expected_output in captured.out

def test_calculate_and_print_multiprocessing(capsys):
    calculate_and_print("5", "3", "add", use_multiprocessing=True)
    captured = capsys.readouterr()
    assert "The result of 5 add 3 is 8" in captured.out


def test_repl_exit(mocker):
    mocker.patch('builtins.input', side_effect=["exit"])
    mocker.patch('sys.stdout', new_callable=StringIO)
    repl()
    assert "Exiting the calculator. Goodbye!" in sys.stdout.getvalue()

def test_repl_menu():

    with patch('builtins.input', side_effect=['menu', 'exit']):
        with patch('builtins.print') as mock_print:
            repl()
            mock_print.assert_any_call("Available commands:", "add, subtract, multiply, divide, cube, square")


def test_repl_multiprocessing(mocker):
    mocker.patch('builtins.input', side_effect=["5 3 add", "exit"])
    mocker.patch('sys.stdout', new_callable=StringIO)
    repl(use_multiprocessing=True)
    assert "The result of 5 add 3 is 8" in sys.stdout.getvalue()
    assert "Running with multiprocessing enabled." in sys.stdout.getvalue()


def test_main_with_multiprocessing_argument(mocker):
    mocker.patch('builtins.input', side_effect=["5 3 add", "exit"])
    mocker.patch('sys.stdout', new_callable=StringIO)
    sys.argv = ["main.py", "mp"]
    main()
    assert "The result of 5 add 3 is 8" in sys.stdout.getvalue()
    assert "Running with multiprocessing enabled." in sys.stdout.getvalue()

def test_invalid_input_handling(mocker):
    mocker.patch('builtins.input', side_effect=["invalid input", "exit"])
    mocker.patch('sys.stdout', new_callable=StringIO)
    repl()
    assert "Invalid number input: invalid or None is not a valid number." in sys.stdout.getvalue()


def test_repl_invalid_input():
    with patch('builtins.input', side_effect=['invalid command', 'exit']):
        with patch('builtins.print') as mock_print:
            repl()
            mock_print.assert_any_call("Invalid number input: invalid or None is not a valid number.")

def test_main(mocker):
    mocker.patch.object(sys, 'argv', ['main.py', '3', '2', 'add'])
    with patch('builtins.print') as mock_print:
        main()
        mock_print.assert_any_call("The result of 3 add 2 is 5")