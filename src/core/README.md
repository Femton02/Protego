### How to use the core module

1. Add the working directory of the project to an environment variable called `PROTEGO_WORKSPACE_DIR`

    If you are using bash, you can add the following line to your `.bashrc` or `.bash_profile` file:
    ```bash
    export PROTEGO_WORKSPACE_DIR=/path/to/your/workspace
    ```
    If you are using powershell, you can add the following line to your `profile.ps1` file:
    ```powershell
    $Env:PROTEGO_WORKSPACE_DIR = "/path/to/your/workspace"
    ```
    Make sure to replace `/path/to/your/workspace` with the path to the directory where you have the project.


1. Install tree-sitter needed language parsers


    ```bash
    cd src/core
    pip install -r requirements.txt
    ```

1. Build the tree-sitter parsers
    ```bash
    python3 ./t_sitter/language_build.py
    ```

    After running the above commands, you should have the tree-sitter parsers for the languages you need in the `src/core/t_sitter/languages` directory and the `src/core/t_sitter/build/languages.so` file.


