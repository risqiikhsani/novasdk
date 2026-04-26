# Updating BoostingNova on PyPI

## Step 1: Make Your Code Changes

Edit the source files in `src/novasdk/` (e.g. `utils.py`, `__init__.py`).

---

## Step 2: Bump the Version

You must bump the version **before** uploading — PyPI rejects re-uploads of the same version.

### In `src/novasdk/__init__.py`:
```python
__version__ = "0.2.0"  # increment this
```

### In `pyproject.toml`:
```toml
version = "0.2.0"  # increment this too
```

### In `tests/test_utils.py`:
```python
def test_version():
    assert __version__ == "0.2.0"  # update this too so tests pass
```

---

## Step 3: Rebuild the Package

```bash
rm -rf dist/
/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 -m build
```

> `rm -rf dist/` clears old builds so stale files don't get uploaded.

---

## Step 4: (Optional) Test Install Locally First

```bash
pip install -e .                    # editable install
python -c "import boostingnova; print(boostingnova.__version__)"  # verify
```

---

## Step 5: Upload to Real PyPI

```bash
twine upload dist/*
```

View your updated package at: [pypi.org/project/boostingnova](https://pypi.org/project/boostingnova)

---

## Step 6: Verify the Update

```bash
pip install boostingnova  # or --upgrade to update from an older version
python -c "import boostingnova; print(boostingnova.__version__)"
```

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `pip install -e .` | Install locally in editable mode |
| `rm -rf dist/` | Clear old builds |
| `python -m build` | Rebuild `.whl` and `.tar.gz` |
| `twine check dist/*` | Validate package before upload |
| `twine upload dist/*` | Upload to PyPI |
| `pip install boostingnova` | Install from PyPI |
