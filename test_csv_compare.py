from io import StringIO
import pytest

from csv_compare import load_rows, join_files, comparison_results_as_csv, BadColumnException


def test_load_empty_rows():
    csv_file = iter([])
    key_column = 1
    comparable_column = 3
    fields_dict = load_rows(csv_file, key_column, comparable_column)
    assert len(fields_dict) == 0


def test_load_rows():
    csv_file = iter(["a,b,c", "b,c,d", "e,f,g"])
    key_column = 1
    comparable_column = 3
    rows = load_rows(csv_file, key_column, comparable_column)
    assert rows["a"] == "c"
    assert rows["b"] == "d"
    assert rows["e"] == "g"


def test_join_files():
    csv_file1 = iter(["a,b,c", "b,c,d", "e,f,g"])
    csv_file2 = iter(["a,n,x", "e,m,f"])
    key_column = 1
    comparable_column = 3
    rows = join_files(csv_file1, csv_file2, key_column, comparable_column)
    assert len(rows) == 2
    assert rows["a"] == ("c", "x")
    assert rows["e"] == ("g", "f")


def test_compare_files():
    csv_file1 = iter(["a,b,c", "b,c,d", "e,f,g"])
    csv_file2 = iter(["a,n,x", "e,m,f"])
    key_column = 1
    comparable_column = 3
    writable = StringIO()
    comparison_results_as_csv(writable, csv_file1, csv_file2, key_column, comparable_column)
    content = writable.getvalue().split("\r\n")
    iterator = iter(content)
    assert "key,file1_value,file2_value" == next(iterator)
    assert "a,c,x" == next(iterator)
    assert "e,g,f" == next(iterator)


def test_compare_files_throws_exception_when_invalid_key_column():
    csv_file1 = iter(["a,b,c", "b,c,d", "e,f,g"])
    csv_file2 = iter(["a,n,x", "e,m,f"])
    key_column = 4
    comparable_column = 3
    writable = StringIO()
    with pytest.raises(BadColumnException):
        comparison_results_as_csv(writable, csv_file1, csv_file2, key_column, comparable_column)


def test_compare_files_throws_exception_when_invalid_comparable_column():
    csv_file1 = iter(["a,b,c", "b,c,d", "e,f,g"])
    csv_file2 = iter(["a,n,x", "e,m,f"])
    key_column = 1
    comparable_column = 4
    writable = StringIO()
    with pytest.raises(BadColumnException):
        comparison_results_as_csv(writable, csv_file1, csv_file2, key_column, comparable_column)
