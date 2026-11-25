# Reflection

## 1. Which static analysis issue was the most important and why?

The most important issue was the use of `eval()` in `calculate_dosage()`. It was reported by both Bandit and Pylint. `eval()` can execute arbitrary Python expressions, so allowing input to reach it can turn a simple dosage calculation into a code-execution vulnerability. The fix restricts evaluation to basic arithmetic operations using Python's AST module.

## 2. Which issue was easiest to fix?

The unused imports were the easiest to fix because they had no effect on the program's required behaviour. The unused `sys` and `logging` imports were simply removed.

## 3. Did fixing security issues affect program behaviour?

Some security fixes changed the implementation while preserving the intended functionality. MD5 was replaced with SHA-256 for patient ID generation, so the generated ID format remains a hexadecimal hash but its value changes. `os.system()` was replaced with Python's `print()` so the dispensing label is still displayed without invoking a shell. Pickle-based storage was replaced with JSON storage, which keeps the stock persistence purpose while avoiding unsafe deserialization.

The hardcoded password was also removed. The application now reads the expected password from the `PHARMA_DB_PASSWORD` environment variable rather than storing a secret in source code.

## 4. What did the static analysis tools teach you?

The tools showed that code can run successfully and still contain serious security and maintainability problems. Pylint identified design and style issues, Flake8 identified formatting and basic code-quality violations, and Bandit identified security risks such as unsafe `eval()`, weak hashing, unsafe pickle deserialization, hardcoded credentials and shell execution. Using multiple tools gives broader coverage than relying only on whether the program runs.
