#!/usr/bin/env python3

import re
from io import StringIO

def main():
    # if True:
    #     file = RegularFile(name="fds", parentDirAbsPath="/", size=1337)
    #     print(file)
    #     dir = EmptyDirectory(name="fds/", parentDirAbsPath="/")
    #     print(dir)
    #     dir.addFile(file)
    #     print(dir)
    #     print(list(dir.files)[0])
        # dir.addFile(file) # FileAlreadyExistException

    if True:
        fileA = RegularFile(name="file.a", parentDirAbsPath="/", size=13)
        fileB = RegularFile(name="file.b", parentDirAbsPath="/", size=37)
        dir = Directory(name="dir/", parentDirAbsPath="/", files = {fileA, fileB})
        outputDir = EmptyDirectory(name="new/", parentDirAbsPath="/")
        outputDir.addFile(dir)
        outputDir.addFile(fileA)
        print(outputDir)

    pass
    
# uninstanciable base class for RegularFile and Directory
class File:
    def __new__(cls, *args, **kwargs):
        if cls is File:
            raise TypeError(f"'{cls.__name__}' cannot be instanciated")
        return object.__new__(cls)

    def __init__(self, name: str, parentDirAbsPath: str, size: int):
        assert isinstance(parentDirAbsPath, str)
        assert File.validAbsPath(parentDirAbsPath)

        self.name = name
        self.parentDirAbsPath = parentDirAbsPath
        self._size = size

    def __str__(self, recursionDepth: int = 0):
        out = f"- {self.parentDirAbsPath}{self.name} {self.getSize()}"
        if isinstance(self, Directory) and len(self.files) != 0:
            recursionDepth += 1
            SPACE = ' '
            INDENT = 4 * SPACE
            fileList = [f"{INDENT * recursionDepth}{file.__str__(recursionDepth)}" \
                for file in sorted(self.files)]
            out += "\n" + "\n".join(fileList)

        return out

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        return self.name < other.name

    def getSize(self):
        return self._size

    @staticmethod
    def validAbsPath(absPath: str):
        return len(absPath) > 0 and absPath[0] == absPath[-1] == '/'

class Directory(File):
    def __init__(self, name: str, parentDirAbsPath: str, files: set[File]):
        assert isinstance(name, str)
        assert Directory.validName(name)
        assert isinstance(files, set)
        for file in files:
            assert isinstance(file, File)

        totalSize = sum([file.getSize() for file in files])
        super().__init__(name, parentDirAbsPath, size=totalSize)

        self.files = set()
        for file in files:
            fileCopy = file.__copy__()
            fileCopy.parentDirAbsPath = f"{self.parentDirAbsPath}{self.name}"
            self.files.update([fileCopy])

    def __copy__(self):
        return Directory(self.name, self.parentDirAbsPath, self.files)

    def __iter__(self):
        return iter(self.files)

    # override File::getSize
    def getSize(self):
        return sum([file.getSize() for file in self.files])

    def addFile(self, file: File):
        assert isinstance(file, File)

        if file in self.files:
            raise FileAlreadyExistException(file, f"{self.parentDirAbsPath}{self.name}")

        if isinstance(file, Directory):
            dir = file
            newDir = EmptyDirectory(dir.name, f"{self.parentDirAbsPath}{self.name}")
            for subFile in dir:
                newDir.addFile(subFile)
            self.files.update([newDir])
                
        else: # isinstance(file, RegularFile)
            fileCopy = file.__copy__()
            fileCopy.parentDirAbsPath = f"{self.parentDirAbsPath}{self.name}"
            self.files.update([fileCopy])

    @staticmethod
    def validName(name: str):
        match = re.compile(r"^[a-z\.]+/$").match(name)
        return match != None

class RegularFile(File):
    def __init__(self, name: str, parentDirAbsPath: str, size: int):
        assert isinstance(name, str)
        assert RegularFile.validName(name)
        assert isinstance(size, int)
        assert size >= 0

        super().__init__(name, parentDirAbsPath, size)

    def __copy__(self):
        return RegularFile(self.name, self.parentDirAbsPath, self.getSize())

    @staticmethod
    def validName(name: str):
        match = re.compile(r"^[a-z\.]+$").match(name)
        return match != None

class EmptyDirectory(Directory):
    def __init__(self, name: str, parentDirAbsPath: str):
        super().__init__(name, parentDirAbsPath, files=set())
        

class FileAlreadyExistException(Exception):
    def __init__(self, file: File, dirAbsPath: str):
        super().__init__(f"File {file.name} already exists in {dirAbsPath}")

main() if __name__ == "__main__" else None
