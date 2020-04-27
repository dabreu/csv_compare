import sys
import csv
import argparse


class BadColumnException(Exception):
    pass


def comparison_results_as_csv(writable, csv_file1, csv_file2, key_column, comparable_column):
    join_result = join_files(csv_file1, csv_file2, key_column, comparable_column)
    csv_writer = csv.writer(writable)
    csv_writer.writerow(['key', 'file1_value', 'file2_value'])
    for key, value in join_result.items():
        csv_writer.writerow([key, *value])


def join_files(csv_file1, csv_file2, key_column, comparable_column):
    file1_rows = load_rows(csv_file1, key_column, comparable_column)
    file2_reader = csv.reader(csv_file2)
    join_result = {}
    for row_number, row in enumerate(file2_reader):
        join_key = get_column_value(row, key_column, row_number)
        if join_key in file1_rows:
            join_result[join_key] = (file1_rows[join_key],
                                     get_column_value(row, comparable_column, row_number))
    return join_result


def load_rows(csv_file, key_column, comparable_column):
    rows = {}
    reader = csv.reader(csv_file)
    for row_number, row in enumerate(reader):
        load_row_columns(rows, row, key_column, comparable_column, row_number)
    return rows


def load_row_columns(rows, row, key_column, comparable_column, row_number):
    key = get_column_value(row, key_column, row_number)
    value = get_column_value(row, comparable_column, row_number)
    rows[key] = value


def get_column_value(row, column, row_number):
    try:
        return row[column - 1]
    except IndexError as exception:
        raise BadColumnException("Couldn't find column {} in row {}".
                                 format(column, row_number)) from exception


def _get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('file1', help="The first file to compare", type=argparse.FileType('r'))
    parser.add_argument('file2', help="The second file to compare", type=argparse.FileType('r'))
    parser.add_argument('key_column', help="The index of the column used as key", type=int)
    parser.add_argument('comparable_column', help="The index of the column to compare", type=int)
    return parser.parse_args()


def main():
    args = _get_arguments()
    comparison_results_as_csv(sys.stdout, args.file1, args.file2,
                              args.key_column, args.comparable_column)


if __name__ == "__main__":
    main()
