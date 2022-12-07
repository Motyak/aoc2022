#!/usr/bin/env python3

from io import StringIO
import re

def main():
    # firstCrateStack = CrateStack()
    # firstCrateStack.push(Crate('A'))
    # firstCrateStack.push(Crate('B'))

    # secondCrateStack = CrateStack()
    # secondCrateStack.push(Crate('C'))
    
    # thirdCrateStack = CrateStack()
    # thirdCrateStack.push(Crate('D'))

    # crateStacks = CrateStacks([
    #     firstCrateStack,
    #     secondCrateStack,
    #     thirdCrateStack
    # ])
    # print(crateStacks)
    
    # procedure = Procedure(3, 1, 2)
    # print(procedure)

    INPUT_FILENAME = "input.txt"

    crateStacks, procedures = parseInputFile(INPUT_FILENAME)






class Crate:
    @staticmethod
    def of(txt: str):
        assert isinstance(txt, str)
        
        match = re.compile(r"^\[([A-Z])\]$").search(txt.strip())
        assert match
        assert len(match.groups()) == 1
        return Crate(match.group(1))

    def __init__(self, mark: str):
        assert isinstance(mark, str)
        assert len(mark) == 1

        self.mark = mark

    def __str__(self):
        return f"[{self.mark}]"

class CrateStack:
    def __init__(self):
        self.stack = []

    def __copy__(self):
        res = CrateStack()
        for crate in self.stack:
            res.push(crate)
        return res

    def __str__(self):
        crates = [str(crate) for crate in self.stack]
        crates.reverse() # list to stack conversion
        return "\n".join(crates)

    def __len__(self):
        return len(self.stack)

    def push(self, crate: Crate):
        assert isinstance(crate, Crate)

        self.stack.append(crate)

    def pop(self):
        return self.stack.pop()

    def getTopCrate(self):
        return self.stack[-1] if len(self.stack) > 0 else None

    

# data structure
class Procedure:
    @staticmethod
    def of(line: str):
        def parseValue(keyword, line):
            match = re.compile(rf"{keyword}\s+(\d+)").search(line)
            assert match
            assert len(match.groups()) == 1
            return int(match.group(1))

        nbOfCratesToMove = parseValue("move", line)
        originStackIndex = parseValue("from", line)
        destinationStackIndex = parseValue("to", line)

        return Procedure(nbOfCratesToMove, originStackIndex, destinationStackIndex)

    def __init__(self, nbOfCratesToMove: int, originStackIndex: int, destinationStackIndex: int):
        assert isinstance(nbOfCratesToMove, int)
        assert isinstance(originStackIndex, int)
        assert isinstance(destinationStackIndex, int)

        self.nbOfCratesToMove = nbOfCratesToMove
        self.originStackIndex = originStackIndex
        self.destinationStackIndex = destinationStackIndex

    def __str__(self):
        return f"move {self.nbOfCratesToMove}" \
              f" from {self.originStackIndex}" \
              f" to {self.destinationStackIndex}"


class CrateStacks:
    SIZE = 3

    @staticmethod
    def of(lines: list):
        assert isinstance(lines, list)

        # parsing footer row #
        stackIndices = lines[-1].split()
        assert len(stackIndices) > 0
        nbOfStacks = int(stackIndices[-1])

        # fill list with proper number of empty crate stacks #
        crateStacks = []
        for _ in range(nbOfStacks):
            crateStacks.append(CrateStack())

        # parsing upward rows #
        for row in range(2, len(lines) +1):
            # currentRow = lines[-row].split()
            currentRow = re.compile(r".{3}\s?").findall(lines[-row])
            assert len(currentRow) == nbOfStacks
            currentRow = [*map(lambda x: x.strip(), currentRow)]
            print(len(currentRow))
            assert len(currentRow) == nbOfStacks
            for col in range(nbOfStacks):
                if currentRow[col] != "":
                    crateStacks[col].push(Crate.of(currentRow[col]))

        return CrateStacks(crateStacks)

    @staticmethod
    def getNecessaryStackSizes(procedure: Procedure):
        assert isinstance(procedure, Procedure)

        return {
            procedure.originStackIndex: procedure.nbOfCratesToMove
        }

    def __init__(self, crateStacks: list):
        assert isinstance(crateStacks, list)
        assert len(crateStacks) == CrateStacks.SIZE
        for i in range(CrateStacks.SIZE):
            assert isinstance(crateStacks[i], CrateStack)

        self.firstStack, self.secondStack, self.thirdStack = crateStacks

    def __str__(self):
        def pushEmptyCrate(stack):
            stack.push(Crate(" "))

        stacks = self.getStacks()
        highestStack = max([len(stack) for stack in stacks])
        for stack in stacks:
            for _ in range(highestStack - len(stack)):
                pushEmptyCrate(stack)

        SPACE = ' '
        PLACEHOLDER = 3 * SPACE
        EMPTY_CRATE = "[ ]"
        out = StringIO()
        for _ in range(highestStack):
            row = [stacks[i].pop() for i in {0, 1, 2}]
            row = [*map(lambda x: str(x).replace(EMPTY_CRATE, PLACEHOLDER), row)]
            print(*row, file=out)
        footerRow = [f" {i} " for i in range(1, CrateStacks.SIZE +1)]
        print(*footerRow, file=out, end='')

        return out.getvalue()

    def rearrange(self, procedure: Procedure):
        stack = {
            0: self.firstStack,
            1: self.secondStack,
            2: self.thirdStack
        }

        def testPreconditions():
            preconditions = CrateStacks.getNecessaryStackSizes(procedure)
            for stackIndex, necessarySize in preconditions:
                assert len(stack[stackIndex]) >= necessarySize

        def procede():
            for _ in range(procedure.nbOfCratesToMove):
                stack[procedure.destinationStackIndex] = \
                        stack[procedure.originStackIndex].pop()

        testPreconditions()
        procede()

    def getTopCrates(self):
        return [stack.getTopCrate() for stack in self.getStacks()]

    # returns copies
    def getStacks(self):
        return [
            self.firstStack.__copy__(),
            self.secondStack.__copy__(),
            self.thirdStack.__copy__()
        ]

def parseListOfProcedures(lines: list):
    assert isinstance(lines, list)

    return [Procedure.of(line) for line in lines]

# returns the parsed CrateStack and list of Procedure
def parseInputFile(filename: str):
    assert isinstance(filename, str)

    def readUntilEmptyLine(file):
        lines = []
        line = file.readline()
        while line.strip():
            lines.append(line)
            line = file.readline()
        return lines

    crateStacks: CrateStacks
    procedures: list
    with open(filename, 'r') as file:
        crateStacks = CrateStacks.of(readUntilEmptyLine(file))
        procedures = parseListOfProcedures(readUntilEmptyLine(file))
    
    return CrateStacks(crateStacks), procedures


main() if __name__ == '__main__' else None
