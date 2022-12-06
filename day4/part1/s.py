#!/usr/bin/env python3

from functools import reduce


def main():

    INPUT_FILENAME = 'input.txt'

    assignmentPairs = parseAssignmentPairs(INPUT_FILENAME)
    
    # data visualization #
    for assignmentPair in assignmentPairs[:3]:
        print(assignmentPair)
    print('...')
    for assignmentPair in assignmentPairs[-3:]:
        print(assignmentPair)

    def countWheneverRangeFullyContainsTheOther(i, rangePair):
        return i + rangePair.oneRangeFullyContainsTheOther()

    res = reduce(
        countWheneverRangeFullyContainsTheOther,
        assignmentPairs,
        0
    )

    print("res=", res)


class SectionRange:
    SEPARATOR = '-'

    @staticmethod
    def of(line: str):
        assert isinstance(line, str)

        edgeValues = [int(str) for str in line.split(SectionRange.SEPARATOR)]
        assert len(edgeValues) == 2
        return SectionRange(*edgeValues)

    def __init__(self, beginSection: int, endSection: int):
        assert isinstance(beginSection, int)
        assert isinstance(endSection, int)
        assert beginSection > 0
        assert endSection >= beginSection

        self.begin = beginSection
        self.end = endSection

    def __str__(self):
        return ', '.join(str(i) for i in range(self.begin, self.end +1))

    def __iter__(self):
        return iter(range(self.begin, self.end +1))

    def __len__(self):
        return self.end - self.begin + 1


class SectionRangePair:
    SEPARATOR = ','

    @staticmethod
    def of(line: str):
        assert isinstance(line, str)

        sectionRanges = [SectionRange.of(str) for str in line.split(SectionRangePair.SEPARATOR)]
        assert len(sectionRanges) == 2
        return SectionRangePair(*sectionRanges)

    def __init__(self, leftRange: SectionRange, rightRange: SectionRange):
        assert isinstance(leftRange, SectionRange)
        assert isinstance(rightRange, SectionRange)

        self.leftRange = leftRange
        self.rightRange = rightRange

    def __str__(self):
        return f"{self.leftRange.begin}-{self.leftRange.end}" \
                + f",{self.rightRange.begin}-{self.rightRange.end}"

    def oneRangeFullyContainsTheOther(self):
        return len(self.findCommonSections()) == self.getSmallerRangeSize()

    def findCommonSections(self):
        return list(set(self.leftRange) & set(self.rightRange))

    def getSmallerRangeSize(self):
        return min([len(self.leftRange), len(self.rightRange)])


Assignment = SectionRange
AssignmentPair = SectionRangePair


def parseAssignmentPairs(filename: str):
    assert isinstance(filename, str)

    lines: list
    with open(filename, 'r') as file:
        lines = file.readlines()

    return [AssignmentPair.of(line) for line in lines]


main() if __name__ == '__main__' else None
