#!/usr/bin/env python3

import re # parse blank lines and numbers

INPUT_FILENAME = 'input.txt'

g_groups = []
g_working_group = []

def main():

    lines = files_to_lines(INPUT_FILENAME)

    for line in lines:
        process(line)
    process('')

    res = max([sum(group) for group in g_groups])

    # printing variables #
    print('g_groups = ')
    for group in [*g_groups[:3]]:
        print(len(group), '->', *group)
    print('...')
    for group in [*g_groups[-3:]]:
        print(len(group), '->', *group)
    print('g_working_group =', g_working_group)    
    print('res = ', res)


def files_to_lines(filename):
    
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().splitlines()


def process(line):

    def is_blank(line):
        return re.compile(r'^\s*$').match(line)

    def parse_integer(line):
        matches = re.compile(r'^[0-9]+$').findall(line)
        return None if not matches else int(matches[0])

    if is_blank(line):
        move_working_group_to_groups()

    number = parse_integer(line)
    if number:
        g_working_group.append(number)


def move_working_group_to_groups():

    if len(g_working_group) != 0:
        # need to pass a copy because of the clear
        g_groups.append([*g_working_group])
        g_working_group.clear()


main() if __name__ == '__main__' else None
