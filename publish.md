# Publishing Nova SDK to PyPI

## Step 1: Create PyPI Accounts

1. [test.pypi.org](https://test.pypi.org) — Register an account (for testing)
2. [pypi.org](https://pypi.org) — Register an account (for real publishing)

---

## Step 2: Enable 2FA and Get API Tokens

You need a token from **both** Test PyPI and real PyPI.

### Test PyPI Token
1. Log into [test.pypi.org](https://test.pypi.org) → **Account Settings** → **API Tokens** → **Add API Token**
2. Copy the token

### Real PyPI Token
1. Log into [pypi.org](https://pypi.org) → **Account Settings** → **Two-Factor Authentication** → Enable it
2. Then **API Tokens** → **Add API Token**
3. Copy the token

> Both tokens look like `pypi-Ag...` — name them differently so you can tell them apart.

---

## Step 3: Add Credentials to `~/.pypirc`

Create or edit `~/.pypirc`:

```ini
[testpypi]
username = __token__
password = your-test-pypi-token-here

[pypi]
username = __token__
password = your-real-pypi-token-here
```

Or use `twine` interactively — it will ask on first run.

---

## Step 4: Upload to Test PyPI First (Safe Test)

```bash
twine upload --repository testpypi dist/*
```

When asked for credentials:
- Username: `__token__`
- Password: `your-test-pypi-token`

---

## Step 5: Verify Test Install Works

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ novasdk
```

If it installs cleanly, you're good to go.

---

## Step 6: Upload to Real PyPI

```bash
twine upload dist/*
```

This publishes `novasdk 0.1.0` publicly to PyPI.

---

## After Updating Code (Re-publishing)

You must bump the version each time — PyPI does not allow re-uploading the same version.

```bash
# 1. Update version in src/novasdk/__init__.py
#    e.g. change "0.1.0" → "0.2.0"

# 2. Also update version in pyproject.toml

# 3. Rebuild
/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 -m build

# 4. Upload
twine upload dist/*
```

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python -m build` | Build `.whl` and `.tar.gz` into `dist/` |
| `twine check dist/*` | Validate package before upload |
| `twine upload --repository testpypi dist/*` | Upload to Test PyPI |
| `twine upload dist/*` | Upload to real PyPI |
