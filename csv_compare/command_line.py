import csv_compare
import sys
import argparse


def _get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('file1', help="The first file to compare", type=argparse.FileType('r'))
    parser.add_argument('file2', help="The second file to compare", type=argparse.FileType('r'))
    parser.add_argument('key_column', help="The index of the column used as key", type=int)
    parser.add_argument('comparable_column', help="The index of the column to compare", type=int)
    parser.add_argument(
            '-d', '--delimiter', default=',', help="field delimiter (default: ',')", type=str)
    return parser.parse_args()


def main():
    args = _get_arguments()
    csv_compare.CsvCompare(delimiter=args.delimiter).comparison_results_as_csv(
            sys.stdout, args.file1, args.file2, args.key_column, args.comparable_column)


if __name__ == "__main__":
    main()
