# Static Code Analysis Issues

The original `pharmacy_manager.py` was analysed using Pylint, Bandit and Flake8.

| Priority | Issue | Type / Tool | Line(s) | Description | Fix Approach |
|---|---|---|---|---|---|
| High | Use of `eval()` | Security — Bandit B307 / Pylint W0123 | 46–48 | `eval()` can execute arbitrary Python code if the formula is influenced by untrusted input. | Replaced `eval()` with an AST-based evaluator that permits only basic arithmetic operators and numeric constants. |
| High | Weak MD5 hashing | Security — Bandit B324 | 50–51 | MD5 is cryptographically weak and should not be used when a secure hash is required. | Replaced MD5 with SHA-256 using `hashlib.sha256()`. |
| High | Shell command through `os.system()` | Security — Bandit B605 | 67–68 | Building a shell command with input can lead to command injection. | Removed shell execution and used Python `print()` directly. |
| Medium | Unsafe `pickle.load()` | Security — Bandit B301 | 61–64 | Unpickling untrusted data can execute arbitrary code. | Replaced pickle persistence with JSON serialization/deserialization. |
| Medium | Hardcoded password | Security — Bandit B105 | 11 | A password embedded in source code can be exposed through source control or code sharing. | Removed the hardcoded secret and read the password from the `PHARMA_DB_PASSWORD` environment variable. |
| Medium | Bare `except:` | Security/quality — Bandit B110, Pylint W0702, Flake8 E722 | 23–28 | A bare exception catches every exception, including unexpected system-level errors, making debugging difficult. | Caught the specific `KeyError` expected when a medicine is missing. |
| Medium | Mutable default argument | Code quality — Pylint W0102 | 13 | `audit=[]` is created once and reused across calls, which can cause state to leak between calls. | Changed the default to `None` and created a new list inside the function. |
| Low | Unused imports | Code quality — Pylint/Flake8 | 2, 6 | `sys` and `logging` were imported but never used. | Removed the unused imports. |
| Low | Missing function/module documentation | Code quality — Pylint C0114/C0116 | Multiple lines | Functions lacked documentation, reducing readability and maintainability. | Added a module-level structure and docstrings to the functions. |
| Low | Non-snake-case function names | Code quality — Pylint C0103 | Multiple lines | Names such as `addMedicine` did not follow the standard Python naming convention. | Renamed functions to snake_case and updated their callers. |
