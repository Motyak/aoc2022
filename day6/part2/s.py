#!/usr/bin/env python3

from collections.abc import Callable
from typing import Generator

def main():
    INPUT_FILENAME = "input.txt"


    dataStream = DataStream.fromTextFile(INPUT_FILENAME)
    
    startOfMessage = StartOfMessageMarker.fromDataStream(dataStream)

    print(startOfMessage)


class DataStream:
    @staticmethod
    def fromTextFile(filename: str):
        assert isinstance(filename, str)

        with open(filename, 'r') as file:
            while True:
                nextChar = file.read(1)
                if nextChar:
                    yield nextChar
                else:
                    return

class StrategyGenerator:
    @staticmethod
    def firstOccurenceOfNDifferentCharacters(n: int):
        assert isinstance(n, int)
        def inner(currentData: str, nextChar: str):
            assert isinstance(currentData, str)
            assert isinstance(nextChar, str)
            assert len(nextChar) == 1

            CUR_DATA_MAX_SIZE = n - 1
            containsDuplicates = lambda x: len(x) != len(set(x))
            return len(currentData) < CUR_DATA_MAX_SIZE \
                or containsDuplicates(currentData[-CUR_DATA_MAX_SIZE:] + nextChar)
        
        return inner


# # return True as long as we need to continue reading
# def firstOccurenceOfFourDifferentCharacters(currentData: str, nextChar: str):
#     assert isinstance(currentData, str)
#     assert isinstance(nextChar, str)
#     assert len(nextChar) == 1

#     def containsDuplicates(characters):
#         return len(characters) != len(set(characters))

#     return len(currentData) < 3 or containsDuplicates(currentData[-3:] + nextChar)


class StartOfMessageMarker:
    MARKER_SIZE = 14
    STRATEGY = StrategyGenerator.firstOccurenceOfNDifferentCharacters(MARKER_SIZE)

    def __init__(self, marker: str, position: int):
        assert isinstance(marker, str)
        assert len(marker) == StartOfMessageMarker.MARKER_SIZE
        assert isinstance(position, int)

        self.marker = marker
        self.position = position

    def __str__(self):
        return f"{self.marker=}\t{self.position=}"

    @staticmethod
    def fromDataStream(dataStream: Generator):
        assert isinstance(dataStream, Generator)

        MARKER_SIZE = StartOfMessageMarker.MARKER_SIZE
        BUFFER_MAX_SIZE = MARKER_SIZE
        STRATEGY = StartOfMessageMarker.STRATEGY

        buffer = ""
        position = 0
        nextChar = next(dataStream)
        while nextChar and STRATEGY(buffer, nextChar):
            buffer = buffer[-BUFFER_MAX_SIZE:] + nextChar
            position += 1
            nextChar = next(dataStream)
        position += 1

        # marker has a size of four characters
        marker = (buffer + nextChar)[-MARKER_SIZE:]
        return StartOfMessageMarker(marker, position)

main() if __name__ == "__main__" else None
