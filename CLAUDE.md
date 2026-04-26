# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Package Info

- **PyPI name**: `boostingnova`
- **Install**: `pip install boostingnova`
- **Python import**: `import novasdk` (internal package dir is `src/novasdk/`)
- **Version**: stored in both `src/novasdk/__init__.py` (`__version__`) and `pyproject.toml` (`version`) — keep them in sync

## Development Commands

```bash
# Install in editable mode
uv pip install -e .

# Run all tests
.venv/bin/python -m pytest

# Run a single test
.venv/bin/python -m pytest tests/test_utils.py::test_version -v

# Build distribution (clears dist/ first)
rm -rf dist/
/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 -m build

# Validate package before upload
twine check dist/*

# Upload to PyPI
twine upload dist/*
```

## Architecture

- `src/novasdk/__init__.py` — public API, re-exports all utilities, holds `__version__`
- `src/novasdk/utils.py` — all logging utilities (NovaLogger, helpers, context managers)
- `tests/test_utils.py` — test stubs (version test only for now)

## Publishing / Versioning

When releasing a new version, bump in **all three places** before building:
1. `src/novasdk/__init__.py` → `__version__`
2. `pyproject.toml` → `version`
3. `tests/test_utils.py` → version assertion

PyPI rejects re-uploads of the same version. Always `rm -rf dist/` before rebuilding.

## Key Patterns

- `nova_log` — module-level shared `NovaLogger` instance
- Module-level helpers (`print_success`, `print_warning`, etc.) wrap `nova_log` methods
- `NovaLogger._format` builds the timestamp + level prefix string
- `print_tree`, `progress`, `status`, `timer` are context managers wrapping rich primitives
- Rich is the only runtime dependency
