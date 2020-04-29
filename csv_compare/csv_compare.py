import csv


class BadColumnException(Exception):
    pass


class CsvCompare():
    def __init__(self, delimiter=','):
        self._delimiter = delimiter

    def comparison_results_as_csv(
            self, writable, csv_file1, csv_file2, key_column, comparable_column):
        csv_writer = csv.writer(writable, delimiter=self._delimiter)
        csv_writer.writerow(['key', 'file1_value', 'file2_value'])
        for result in self.join_files(csv_file1, csv_file2, key_column, comparable_column):
            csv_writer.writerow(result)

    def join_files(self, csv_file1, csv_file2, key_column, comparable_column):
        file1_rows = self.load_rows(csv_file1, key_column, comparable_column)
        file2_reader = csv.reader(csv_file2, delimiter=self._delimiter)
        for row_number, row in enumerate(file2_reader):
            join_key = self.get_column_value(row, key_column, row_number)
            if join_key in file1_rows:
                value1 = file1_rows[join_key]
                value2 = self.get_column_value(row, comparable_column, row_number)
                if value1 != value2:
                    yield (join_key, value1, value2)

    def load_rows(self, csv_file, key_column, comparable_column):
        rows = {}
        reader = csv.reader(csv_file, delimiter=self._delimiter)
        for row_number, row in enumerate(reader):
            self.load_row_columns(rows, row, key_column, comparable_column, row_number)
        return rows

    def load_row_columns(self, rows, row, key_column, comparable_column, row_number):
        key = self.get_column_value(row, key_column, row_number)
        value = self.get_column_value(row, comparable_column, row_number)
        rows[key] = value

    def get_column_value(self, row, column, row_number):
        try:
            return row[column - 1]
        except IndexError:
            raise BadColumnException(
                    "Couldn't find column {} in row {}".format(column, row_number))
