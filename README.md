# Protego

Protego is a static analysis tool designed to identify security vulnerabilities in JavaScript codebases. It helps developers detect potential security risks early in the development process, enabling them to mitigate them before deployment.

## Features

- Static analysis of JavaScript code.
- Detection of common security vulnerabilities, such as Cross-Site Scripting (XSS), SQL Injection, Direct Response Write vulnerabilities and much more.
- Customizable rules to suit specific project requirements.
- Integration with CI/CD pipelines for automated security checks.
- Command-line interface for easy usage.

## Installation

To install Protego, follow these steps:

1. Clone the repository to your local machine and the submodules:

    ```
    git clone https://github.com/Femton02/Protego.git
    git submodule update --init --recursive
    ```

1. Navigate to the Protego directory:

    ```
    cd protego
    ```

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
    pip install -r src/requirements.txt
    ```

1. Build the tree-sitter parsers

    ```bash
    python3 src/core/t_sitter/language_build.py
    ```

    After running the above commands, you should have the tree-sitter parsers for the languages you need in the `src/core/t_sitter/languages` directory and the `src/core/t_sitter/build/languages.so` file.


## Usage

To analyze your JavaScript code with Protego, run the following command:

```
python3 src/cli/cli_interface.py -h
```

This will display the help message, which contains information about the available options and how to use them.


