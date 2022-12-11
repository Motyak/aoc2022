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

            BUFFER_MAX_SIZE = n - 1
            containsDuplicates = lambda x: len(x) != len(set(x))
            return len(buffer) < BUFFER_MAX_SIZE \
                or containsDuplicates(buffer[-BUFFER_MAX_SIZE:] + nextChar)
        
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
            BUFFER_MAX_SIZE = StartMarkerImpl.MARKER_SIZE
            STRATEGY = StartMarkerImpl.STRATEGY

            buffer = ""
            position = 0
            nextChar = next(dataStream, None)
            while nextChar and STRATEGY(buffer, nextChar):
                buffer = buffer[-BUFFER_MAX_SIZE:] + nextChar
                position += 1
                nextChar = next(dataStream)
            position += 1

            marker = (buffer + nextChar)[-MARKER_SIZE:]

            return StartMarkerImpl(marker, position)
    # -- end of class StartMarkerImpl

    return StartMarkerImpl

main() if __name__ == "__main__" else None
