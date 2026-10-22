# Python cheatsheet

Targets Python 3.9 and newer; newer syntax is marked.

## Data structures

```python
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field

Counter("mississippi").most_common(2)     # [('i', 4), ('s', 4)]
groups = defaultdict(list); groups[key].append(item)
queue = deque(maxlen=100)                 # O(1) at both ends, bounded

@dataclass(frozen=True)
class Point:
    x: int
    y: int
    tags: list = field(default_factory=list)   # never a mutable default directly
```

## Comprehensions and unpacking

```python
squares = [n * n for n in numbers if n > 0]
index = {user.id: user for user in users}
first, *rest = items
merged = {**defaults, **overrides}        # 3.9+: defaults | overrides
```

## Iterators and generators

```python
def read_chunks(path, size=65536):
    with open(path, "rb") as f:
        while chunk := f.read(size):      # walrus, 3.8+
            yield chunk

from itertools import islice, chain, groupby
list(islice(endless(), 10))
```

A generator is lazy and single use. See [`01-snippets/00-lazy-generator-pipeline`](../01-snippets/00-lazy-generator-pipeline/).

## Functions

```python
def connect(host, *, timeout=5.0): ...    # timeout is keyword only

from functools import cache, wraps
@cache
def fib(n): return n if n < 2 else fib(n - 1) + fib(n - 2)

def logged(fn):
    @wraps(fn)                            # keeps __name__ and __doc__
    def wrapper(*args, **kwargs):
        print(f"calling {fn.__name__}")
        return fn(*args, **kwargs)
    return wrapper
```

## Context managers

```python
import time
from contextlib import contextmanager

@contextmanager
def timer(label):
    start = time.perf_counter()
    try:
        yield
    finally:
        print(f"{label}: {time.perf_counter() - start:.3f}s")
```

## Typing

```python
from typing import Optional, Protocol

def find(user_id: str) -> Optional[User]: ...    # 3.10+: User | None

class Closeable(Protocol):                       # structural: no inheritance needed
    def close(self) -> None: ...
```

## asyncio

```python
import asyncio

async def main():
    results = await asyncio.gather(fetch(a), fetch(b))
    async with asyncio.timeout(5):               # 3.11+
        await slow()

asyncio.run(main())
```

Async helps with waiting on I/O. CPU-bound work needs processes, not coroutines.

## Environment and tooling

```sh
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m unittest -v                  # standard library test runner
python3 -m pytest -x                    # stop at the first failure
python3 -m cProfile -s cumtime app.py   # where the time goes
python3 -X importtime -c "import app"   # slow imports
```
