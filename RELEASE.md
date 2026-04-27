# Release Guide

## Manual Versioning Steps

Follow these steps **in order** each time you release a new version.

### 1. Bump the version

Update `__version__` in `src/hypernova_sdk/__init__.py`:

```python
__version__ = "x.y.z"
```

Update `version` in `pyproject.toml`:

```toml
version = "x.y.z"
```

Update the version assertion in `tests/test_utils.py`:

```python
assert __version__ == "x.y.z"
```

### 2. Rebuild the package

```bash
rm -rf dist/
/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 -m build
twine check dist/*
```

### 3. Commit the changes

```bash
git add .
git commit -m "release: vx.y.z"
```

### 4. Upload to PyPI

```bash
twine upload --repository testpypi dist/*    # test first
twine upload dist/*                          # then real PyPI
```

### 5. Create and push the tag

```bash
git tag vx.y.z
git push origin main --tags
```

### 6. Create the GitHub Release

1. Go to your repo on GitHub → **Releases** → **Draft a new release**
2. Select the tag you just pushed (`vx.y.z`)
3. Fill in the **Release title** and **description**
4. Click **Publish release**

---

## Versioning Convention

Follow [Semantic Versioning](https://semver.org/):

| Change | Example | Notes |
|---|---|---|
| Patch fix | `1.0.0` → `1.0.1` | Bug fixes, no API changes |
| Minor feature | `1.0.1` → `1.1.0` | New features, backward compatible |
| Major breaking | `1.1.0` → `2.0.0` | Breaks backward compatibility |

---

## Quick Reference

```bash
# 1. Update version in 3 places:
#    - src/hypernova_sdk/__init__.py
#    - pyproject.toml
#    - tests/test_utils.py

# 2. Rebuild and validate
rm -rf dist/
python -m build
twine check dist/*

# 3. Commit
git add . && git commit -m "release: v1.2.0"

# 4. Upload to PyPI
twine upload --repository testpypi dist/*
twine upload dist/*

# 5. Tag and push
git tag v1.2.0 && git push origin main --tags
```