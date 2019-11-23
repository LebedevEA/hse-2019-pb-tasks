#!/usr/bin/env python3
from typing import List
from typing import IO
import sys
import re
import argparse


def parse_args(args_str: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('needle', type=str)
    parser.add_argument('files', nargs='*')
    parser.add_argument('-E', dest='regex', action='store_true')
    parser.add_argument('-c', dest='count', action='store_true')
    return parser.parse_args(args_str)


def main(args_str: List[str]) -> None:
    args = parse_args(args_str)

    if not args.regex:
        args.needle = re.escape(args.needle)

    if not args.files:
        lines_in_stdin(args.needle, args.count)
    else:
        lines_in_files(args.needle, args.count, args.files)


def save_matching_lines(pattern: str, input_place: IO[str], count: bool) -> List[str]:
    lines: List[str] = []
    for line in input_place.readlines():
        lines.append(line)
    lines = [str(len(save_line(lines, pattern)))] if count else save_line(lines, pattern)
    return lines


def lines_in_stdin(pattern: str, count: bool) -> None:
    lines = save_matching_lines(pattern, sys.stdin, count)
    print_single_input(lines)


def lines_in_files(pattern: str, count: bool, files: List[str]) -> None:
    for file in files:
        with open(file, 'r') as in_file:
            lines = save_matching_lines(pattern, in_file, count)
            print_line_in_file(lines, file, bool(len(files) - 1))


def save_line(lines: List[str], pattern: str) -> List[str]:
    return_list = []
    for line in lines:
        line = line.rstrip('\n')
        if re.search(pattern, line):
            return_list.append(line)
    return return_list


def print_single_input(lines: List[str]) -> None:
    for line in lines:
        print(line)


def print_line_in_file(lines: List[str], file: str, if_many_files: bool) -> None:
    if if_many_files:
        print_in_many_inputs(file, lines)
        lines.clear()
    else:
        print_single_input(lines)


def print_in_many_inputs(file: str, lines: List[str]) -> None:
    for line in lines:
        print(file + ':' + line)


if __name__ == '__main__':
    main(sys.argv[1:])
