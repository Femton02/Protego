### How to use the core module

1. Install tree-sitter needed language parsers

Make sure you are in `src/core/tree-sitter` directory and run the following command:

```bash
mkdir languages
cd languages
git clone https://github.com/tree-sitter/tree-sitter-javascript
pip install tree-sitter
python3 ./language_build.py
```

After running the above commands, you should have the tree-sitter parsers for the languages you need in the `src/core/tree-sitter/languages` directory and the `src/core/tree-sitter/build/languages.so` file.
