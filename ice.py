import shlex


class SourceFile:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        """Open file, make it a list called stack, then return self"""
        self.file = open(self.filename, 'r')
        self.make_stack()
        return self

    def make_stack(self):
        """Generate stack with lines"""
        self.stack = self.file.readlines()

    def clean_line(self, line):
        """Clean the lines, strip newline"""
        line = line.strip("\n")
        return line

    def lines(self):
        """Generate lines"""
        for _line in self.stack:
            yield self.clean_line(_line)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the file"""
        self.file.close()


class Ice:
    def __init__(self):
        # Set default keywords
        self.KEYWORDS = {
            "print": self._print,
            "input": self._input,
            "int": self._int,
            "str": self._str,
            "float": self._float,
            "bool": self._bool,
            "dump": self._dump,
        }
        # Makes memory
        self.MEMORY = []

    def _print(self, foo):
        print(foo)

    def _input(self, foo):
        self.MEMORY.append(input(foo))

    def _int(self, val):
        self.MEMORY.append(int(val))

    def _str(self, val):
        self.MEMORY.append(str(val))

    def _float(self, val):
        self.MEMORY.append(float(val))

    def _bool(self, val):
        self.MEMORY.append(bool(val))

    def _dump(self):
        print(self.MEMORY)

    # Checks if value actually points to a location in memory
    def mem_location_check(self, value):
        if isinstance(value, list):
            value = value[0]
        if value[0] == "$":
            return self.MEMORY[int(value[1:])]
        else:
            return value

    # Logic for parsing
    def logic(self, line):
        first, *value = shlex.split(line)
        if (command := self.KEYWORDS.get(first, False)):
            if len(value) != 0:
                value = self.mem_location_check(*value)
                command(value)
            else:
                command()


# Main loop
ice = Ice()
with SourceFile("test.ice") as source:
    for line in source.lines():
        ice.logic(line)
