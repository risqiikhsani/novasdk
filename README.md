# HyperNova SDK

A utility library for common Python tasks.

## Installation

```bash
pip install hypernova-sdk
```

## Quick Start

```python
import hypernova_sdk

print(hypernova_sdk.__version__)
```

---

## Display Utilities

Rich-powered logging and output helpers.

```python
import hypernova_sdk

# Print helpers
hypernova_sdk.print_success("It worked!")
hypernova_sdk.print_warning("Watch out!")
hypernova_sdk.print_error("Something went wrong")
hypernova_sdk.print_info("Here's some info")
hypernova_sdk.print_header("Section Title")

# Tables
hypernova_sdk.print_table("Name", "Age", rows=[("Alice", "30"), ("Bob", "25")])

# Trees
hypernova_sdk.print_tree("Project", ("src", ["a.py", "b.py"]), "README.md")

# Progress bar
with hypernova_sdk.progress() as prog:
    task = prog.add_task("Downloading...", total=100)
    for i in range(100):
        prog.update(task, advance=1)

# Spinner
with hypernova_sdk.status("Loading..."):
    data = fetch_data()

# Timer
with hypernova_sdk.timer("Operation"):
    do_work()

# Or use the logger directly
from hypernova_sdk import nova_log
nova_log.success("Done!")
```

---

## Cache Utilities

Thread-safe caching utilities with optional TTL.

### `@ttl_cache(seconds=60)` — Decorator

Cache function results with a time-to-live expiry.

```python
import time
from hypernova_sdk import ttl_cache

@ttl_cache(seconds=30)
def fetch_data(url):
    # Simulate slow I/O
    time.sleep(2)
    return {"data": "value"}

print(fetch_data("https://api.example.com"))  # 2s delay
print(fetch_data("https://api.example.com"))  # instant (cached)
```

### `@memoize` — Decorator

Simple unbounded memoization (no expiry, lifetime of process).

```python
from hypernova_sdk import memoize

@memoize
def expensive_computation(x, y):
    return x ** y

print(expensive_computation(2, 10))  # computed
print(expensive_computation(2, 10))  # cached
```

### `TTLCache` — Class

Manual key-value cache with TTL and LRU eviction.

```python
from hypernova_sdk import TTLCache

cache = TTLCache(ttl=60, maxsize=256)

cache.set("user:1", {"name": "Alice", "role": "admin"})
print(cache.get("user:1"))  # {'name': 'Alice', 'role': 'admin'}

cache.clear()  # remove all entries
```

## License

MIT License
