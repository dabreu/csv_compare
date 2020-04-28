from io import StringIO
import pytest

from csv_compare import CsvCompare, BadColumnException


def test_load_empty_rows():
    csv_file = iter([])
    key_column = 1
    comparable_column = 3
    fields_dict = CsvCompare().load_rows(csv_file, key_column, comparable_column)
    assert len(fields_dict) == 0


def test_load_rows():
    _load_with_delimiter(',')
    _load_with_delimiter('^')


def _load_with_delimiter(delimiter):
    csv_file = iter((
            delimiter.join(('a', 'b', 'c')),
            delimiter.join(('b', 'c', 'd')),
            delimiter.join(('e', 'f', 'g'))))
    key_column = 1
    comparable_column = 3
    rows = CsvCompare(delimiter=delimiter).load_rows(csv_file, key_column, comparable_column)
    assert rows["a"] == "c"
    assert rows["b"] == "d"
    assert rows["e"] == "g"


def test_join_files():
    csv_file1 = iter(["a,b,c", "b,c,d", "e,f,g"])
    csv_file2 = iter(["a,n,x", "e,m,f"])
    key_column = 1
    comparable_column = 3
    rows = list(CsvCompare().join_files(csv_file1, csv_file2, key_column, comparable_column))
    assert len(rows) == 2
    assert rows[0] == ("a", "c", "x")
    assert rows[1] == ("e", "g", "f")


def test_compare_files():
    csv_file1 = iter(["a,b,c", "b,c,d", "e,f,g"])
    csv_file2 = iter(["a,n,x", "b,m,d", "e,m,f"])
    key_column = 1
    comparable_column = 3
    writable = StringIO()
    CsvCompare().comparison_results_as_csv(
            writable, csv_file1, csv_file2, key_column, comparable_column)
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
        CsvCompare().comparison_results_as_csv(
                writable, csv_file1, csv_file2, key_column, comparable_column)


def test_compare_files_throws_exception_when_invalid_comparable_column():
    csv_file1 = iter(["a,b,c", "b,c,d", "e,f,g"])
    csv_file2 = iter(["a,n,x", "e,m,f"])
    key_column = 1
    comparable_column = 4
    writable = StringIO()
    with pytest.raises(BadColumnException):
        CsvCompare().comparison_results_as_csv(
                writable, csv_file1, csv_file2, key_column, comparable_column)
