#!/usr/bin/env python3

from io import StringIO
import re

def main():
    INPUT_FILENAME = "input.txt"

    crateStacks, procedures = parseInputFile(INPUT_FILENAME)

    # visualizing data #
    print(crateStacks, end="\n\n")
    for procedure in procedures[:3]:
        print(procedure)
    print("...")
    for procedure in procedures[-3:]:
        print(procedure)
    print()

    for procedure in procedures:
        crateStacks.rearrange(procedure)

    print(crateStacks, end="\n\n")

    topCrates = [stack.getTopCrate() for stack in crateStacks]
    res = ''.join([crate.mark for crate in topCrates])
    print("res=", res)


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

    def __copy__(self):
        return Crate(self.mark)

    def __str__(self):
        return f"[{self.mark}]"

    def __len__(self):
        return 1

class CrateStack:
    def __init__(self):
        self.stack = []

    def __copy__(self):
        res = CrateStack()
        for crate in self.stack:
            res.push(crate.__copy__())
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

    def pushMultiple(self, crates: list[Crate]):
        assert isinstance(crates, list)
        for crate in crates:
            assert isinstance(crate, Crate)

        self.stack.extend(crates)

    def pop(self):
        return self.stack.pop()

    def popMultiple(self, nbOfCrates: int):
        assert isinstance(nbOfCrates, int)

        assert len(self.stack) >= nbOfCrates
        res = [crate.__copy__() for crate in self.stack[-nbOfCrates:]]
        del self.stack[-nbOfCrates:]

        return res


    def getTopCrate(self):
        assert len(self.stack) >= 1
        return self.stack[-1]

    

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
        originStackId = parseValue("from", line)
        destinationStackId = parseValue("to", line)

        return Procedure(nbOfCratesToMove, originStackId - 1, destinationStackId - 1)

    def __init__(self, nbOfCratesToMove: int, originStackIndex: int, destinationStackIndex: int):
        assert isinstance(nbOfCratesToMove, int)
        assert isinstance(originStackIndex, int)
        assert isinstance(destinationStackIndex, int)

        self.nbOfCratesToMove = nbOfCratesToMove
        self.originStackIndex = originStackIndex
        self.destinationStackIndex = destinationStackIndex

    def __str__(self):
        return f"move {self.nbOfCratesToMove}" \
              f" from {self.originStackIndex + 1}" \
              f" to {self.destinationStackIndex + 1}"


class CrateStacks:
    @staticmethod
    def of(lines: list[str]):
        assert isinstance(lines, list)
        for line in lines:
            assert isinstance(line, str)

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
            currentRow = re.compile(r".{3}\s?").findall(lines[-row])
            assert len(currentRow) == nbOfStacks
            currentRow = [*map(lambda x: x.strip(), currentRow)]
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

    def __init__(self, crateStacks: list[CrateStack]):
        assert isinstance(crateStacks, list)
        for crateStack in crateStacks:
            assert isinstance(crateStack, CrateStack)

        self.crateStacks = crateStacks

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
            row = [stacks[i].pop() for i in range(len(self.crateStacks))]
            row = [*map(lambda x: str(x).replace(EMPTY_CRATE, PLACEHOLDER), row)]
            print(*row, file=out)
        footerRow = [f" {i} " for i in range(1, len(self.crateStacks) +1)]
        print(*footerRow, file=out, end='')

        return out.getvalue()

    def __iter__(self):
        return iter(self.crateStacks)

    def rearrange(self, procedure: Procedure):
        # testing preconditions #
        preconditions = CrateStacks.getNecessaryStackSizes(procedure)
        for stackIndex, necessarySize in preconditions.items():
            assert len(self.crateStacks[stackIndex]) >= necessarySize

        nbOfCratesToMove = procedure.nbOfCratesToMove
        originCrateStack = self.crateStacks[procedure.originStackIndex]
        destinationCrateStack = self.crateStacks[procedure.destinationStackIndex]

        movingCrates = originCrateStack.popMultiple(nbOfCratesToMove)
        destinationCrateStack.pushMultiple(movingCrates)

    def getTopCrates(self):
        return [stack.getTopCrate() for stack in self.getStacks()]

    # returns copies
    def getStacks(self):
        return [stack.__copy__() for stack in self.crateStacks]

def parseListOfProcedures(lines: list[str]):
    assert isinstance(lines, list)
    for line in lines:
        assert isinstance(line, str)

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
    
    return crateStacks, procedures


main() if __name__ == '__main__' else None
