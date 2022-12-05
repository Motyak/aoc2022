#!/usr/bin/env python3

INPUT_FILENAME = 'input.txt'


def main():
    lines = fileToLines(INPUT_FILENAME)

    totalSum = 0
    for line in lines:
        rucksack = Rucksack.parse(line, splitInHalf)
        duplicateItems = rucksack.findDuplicatedItems()
        totalSum += sum([i.getPriority() for i in duplicateItems])

    # printing variables #
    print('totalSum = ', totalSum)


def fileToLines(filename: str):
    with open(filename, 'r') as file:
        return file.read().splitlines()


class Rucksack:
    @staticmethod
    def parse(line: str, strategy: callable):
        leftPart, rightPart = strategy(line)
        leftCompartment = Compartment(leftPart)
        rightCompartment = Compartment(rightPart)
        return Rucksack(leftCompartment, rightCompartment)

    def __init__(self, leftCompartment, rightCompartment):
        self.leftCompartement = leftCompartment
        self.rightCompartement = rightCompartment

    def findDuplicatedItems(self):
        leftItems = set(self.leftCompartement.items)
        rightItems = set(self.rightCompartement.items)
        return [Item(char) for char in leftItems & rightItems]


def splitInHalf(line: str):
    length = len(line)
    leftPart = line[:int(length / 2)]
    rightPart = line[int(length / 2):]
    return [*leftPart], [*rightPart]


class Compartment:
    def __init__(self, items: list):
        self.items = items


class Item:
    def __init__(self, character):
        self.type = character

    def getPriority(self):
        if self.type.isupper():
            return ord(self.type) - 38
        else:  # if lowercase
            return ord(self.type) - 96


main() if __name__ == '__main__' else None
