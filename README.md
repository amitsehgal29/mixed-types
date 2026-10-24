# mixed-types

Find CSV columns that quietly mix types, like a date column with a stray `oops` or an id column with text, before a typed load fails or silently casts.

Pure Python stdlib. Detects int, float, date, bool and text, ignores nulls, and treats int plus float as fine.

```bash
python mixed_types.py orders.csv
```

Prints counts and sample values per offending column; exits `1` if any column is mixed.

```bash
python -m unittest -v
```
