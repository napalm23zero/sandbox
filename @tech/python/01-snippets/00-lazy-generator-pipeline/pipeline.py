"""A lazy pipeline: each stage is a generator, nothing runs until someone asks for a value."""
from itertools import islice


def read_lines(lines, log):
    for line in lines:
        log.append(f"read {line!r}")
        yield line


def parse_numbers(lines):
    for line in lines:
        line = line.strip()
        if line.lstrip("-").isdigit():
            yield int(line)


def squares(numbers):
    for number in numbers:
        yield number * number


def first_squares(lines, count, log):
    """Square the first `count` numbers found in `lines`, reading only as far as needed."""
    return list(islice(squares(parse_numbers(read_lines(lines, log))), count))


if __name__ == "__main__":
    log = []
    source = ["1", "two", "3", "4", "5", "6"]
    print("result:", first_squares(source, 2, log))
    print("\n".join(log))
    print(f"read {len(log)} of {len(source)} lines")
