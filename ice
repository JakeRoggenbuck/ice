#!/usr/bin/env python3
import fire
from ice import Ice, SourceFile
from termcolor import colored


class IceInterpreter(object):
    def __init__(self):
        self.ice = Ice()

    def run(self, filename):
        with SourceFile(filename) as source:
            gen = source.lines()
            for line in gen:
                self.ice.logic(line)

    def step(self, filename):
        with SourceFile(filename) as source:
            gen = source.lines()
            for line in gen:
                input(f"{colored(line, 'green')} >")
                self.ice.logic(line)

if __name__ == '__main__':
    fire.Fire(IceInterpreter)
