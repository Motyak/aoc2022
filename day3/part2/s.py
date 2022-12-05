#!/usr/bin/env python3

def main():
    INPUT_FILENAME = 'input.txt'
    groups = readGroups(INPUT_FILENAME)

    # visualize data #
    for group in groups:
        print(group)
        badge = group.getBadge()
        print('badge=', badge, 'priority=', badge.getPriority(), end='\n\n')

    res = sum(group.getBadge().getPriority() for group in groups)
    print("res=", res)

class Item:
    def __init__(self, type: str):
        assert len(type) == 1
        self.type = type

    def __str__(self):
        return self.type

    def getPriority(self):
        if self.type.isupper():
            return ord(self.type) - 38
        else:  # if lowercase
            return ord(self.type) - 96

Badge = Item

class Rucksack:
    def __init__(self, items: list):
        self.items = items

    def __iter__(self):
        return self.items.__iter__()

    def __str__(self):
        lst = [str(item) for item in self.items]
        return ''.join(lst)

class Group:
    def __init__(self, rucksacks: list):
        assert len(rucksacks) <= 3
        self.rucksacks = rucksacks

    def __iter__(self):
        return self.rucksacks.__iter__()

    def __str__(self):
        lst = [str(rucksack) for rucksack in self.rucksacks]
        return '\n'.join(lst)

    def getBadge(self):
        badges = list(
        set(item.type for item in self.rucksacks[0].items) &
        set(item.type for item in self.rucksacks[1].items) &
        set(item.type for item in self.rucksacks[2].items)
        )
        assert len(badges) == 1
        return Badge(badges[0])
    
def readGroups(filename):
    lines: list

    with open(filename, 'r') as file:
        lines = file.readlines()

    rucksacks = list(map(
        lambda str: Rucksack([Item(char) for char in str.strip()]),
        lines
    ))

    groups = []
    for i in range(0, len(rucksacks), 3):
        groups.append(Group(rucksacks[i:i+3]))

    return groups


main() if __name__ == '__main__' else None
