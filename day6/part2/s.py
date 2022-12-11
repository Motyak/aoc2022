#!/usr/bin/env python3
from collections.abc import Callable
from typing import Generator

def main():
    INPUT_FILENAME = "input.txt"
    dataStream = DataStream.fromTextFile(INPUT_FILENAME)

    MARKER_SIZE = 14
    StartOfMessageMarker = StartMarker(MARKER_SIZE)
    marker = StartOfMessageMarker.fromDataStream(dataStream)
    print(marker)

class DataStream:
    @staticmethod
    # yield function <=> generator <=> function retuning an iterator
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
    # function generator
    def firstOccurenceOfNDifferentCharacters(n: int):
        assert isinstance(n, int)
        assert n >= 0
        
        def strategy(buffer: str, nextChar: str):
            assert isinstance(buffer, str)
            assert isinstance(nextChar, str)
            assert len(nextChar) == 1

            incompleteBuffer = len(buffer) < (n - len(nextChar))
            containsDuplicates = lambda x: len(x) != len(set(x))
            return incompleteBuffer \
                or containsDuplicates((buffer + nextChar)[-n:])
        
        return strategy

# class generator
def StartMarker(markerSize: int):
    assert isinstance(markerSize, int)
    assert markerSize >= 0

    class StartMarkerImpl:
        MARKER_SIZE: int = markerSize
        STRATEGY: Callable = StrategyGenerator.firstOccurenceOfNDifferentCharacters(markerSize)

        def __init__(self, marker: str, position: int):
            assert isinstance(marker, str)
            assert len(marker) == StartMarkerImpl.MARKER_SIZE
            assert isinstance(position, int)
            assert position >= 0

            self.marker = marker
            self.position = position

        def __str__(self):
            return f"{self.marker=}\t{self.position=}"

        @staticmethod
        def fromDataStream(dataStream: Generator):
            assert isinstance(dataStream, Generator)

            MARKER_SIZE = StartMarkerImpl.MARKER_SIZE
            STRATEGY = StartMarkerImpl.STRATEGY

            buffer = ""
            nextChar: str[1]
            position = 0
            
            while True:
                nextChar = next(dataStream, None)

                if not nextChar:
                    if len(buffer) < MARKER_SIZE:
                        raise NotEnoughCharactersException()
                    else: # if len(buffer) == MARKER_SIZE
                        return StartMarkerImpl(marker=buffer, position=position)

                if not STRATEGY(buffer, nextChar):
                    return StartMarkerImpl(
                        marker= (buffer + nextChar)[-MARKER_SIZE:],
                        position= position + len(nextChar)
                    )

                buffer += nextChar
                position += 1
    # -- end of class StartMarkerImpl

    return StartMarkerImpl

class NotEnoughCharactersException(Exception):
    def __init__(self):
        super().__init__("Not enough characters to build a valid start marker")


main() if __name__ == "__main__" else None
