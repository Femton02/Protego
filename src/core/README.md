### How to use the core module

1. Install tree-sitter needed language parsers

    Make sure you are in `src/core` directory and run the following command:

    ```bash
    cd src/core
    pip install -r requirements.txt
    python3 ./t_sitter/language_build.py
    ```

    After running the above commands, you should have the tree-sitter parsers for the languages you need in the `src/core/t_sitter/languages` directory and the `src/core/t_sitter/build/languages.so` file.

1. Run the core module

    Make sure you are in the `src/core` directory and run the following command:

    ```bash
    python3 main.py
    ```
