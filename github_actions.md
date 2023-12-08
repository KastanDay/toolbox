## Python code formatting

Filepath: `.github/workflows/yapf-format.yml`
```python
name: Format code

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: write
  pull-requests: write

jobs:
  format:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: pip install yapf
        run: pip install yapf
      - name: Format code with yapf
        run: |
          yapf --in-place --recursive --parallel \
          --style='{based_on_style: google, column_limit: 140, indent_width: 2}' \
          --exclude '*.env' .
      - name: Commit changes
        uses: EndBug/add-and-commit@v4
        with:
          author_name: ${{ github.actor }}
          author_email: ${{ github.actor }}@users.noreply.github.com
          message: Format code
          add: "."
          branch: ${{ github.ref }}

```
