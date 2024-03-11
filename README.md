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

1. Clone the repository to your local machine:

    ```
    git clone https://github.com/yourusername/protego.git
    ```

2. Navigate to the Protego directory:

    ```
    cd protego
    ```

3. Install dependencies:

    ```
    npm install
    ```

## Usage

To analyze your JavaScript code with Protego, run the following command:

  
    node src/main.js

By default, Protego analyzes all JavaScript files in the `test` directory. You can customize the file paths by editing the `filePaths` array in `main.js`.

## Contributing

Contributions to Protego are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on our GitHub repository.

## License

Protego is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
