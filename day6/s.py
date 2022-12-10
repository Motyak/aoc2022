#!/usr/bin/env python3

from collections.abc import Callable
from typing import Generator

def main():
    INPUT_FILENAME = "input.txt"

    dataStream = DataStream.fromTextFile(INPUT_FILENAME)
    
    startOfPacket = StartOfPacketMarker.fromDataStream(dataStream)

    print(startOfPacket)


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

# return True as long as we need to continue reading
def firstOccurenceOfFourDifferentCharacters(currentData: str, nextChar: str):
    assert isinstance(currentData, str)
    assert isinstance(nextChar, str)
    assert len(nextChar) == 1

    def containsDuplicates(characters):
        return len(characters) != len(set(characters))

    return len(currentData) < 3 or containsDuplicates(currentData[-3:] + nextChar)

class StartOfPacketMarker:
    def __init__(self, marker: str, position: int):
        assert isinstance(marker, str)
        assert len(marker) == 4
        assert isinstance(position, int)

        self.marker = marker
        self.position = position

    def __str__(self):
        return f"{self.marker=}\t{self.position=}"

    @staticmethod
    def fromDataStream(dataStream: Generator, strategy: Callable = firstOccurenceOfFourDifferentCharacters):
        assert isinstance(dataStream, Generator)
        assert isinstance(strategy, Callable)

        buffer = ""
        position = 0
        nextChar = next(dataStream)
        while nextChar and strategy(buffer, nextChar):
            buffer = buffer[-3:] + nextChar
            position += 1
            nextChar = next(dataStream)
        position += 1

        # marker has a size of four characters
        marker = (buffer + nextChar)[-4:]
        return StartOfPacketMarker(marker, position)

main() if __name__ == "__main__" else None
