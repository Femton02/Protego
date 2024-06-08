import os
import sys

protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
from common_includes import *

#____________________________________________________________________________________#
import base64
import json
import re

class URLDetector:
    """Class to detect URLs in JavaScript code taking into account variables and functions."""
    def __init__(self, tree: Tree):
        self.tree: Tree = tree
        self.source_code: str = tree.root_node.text.decode()
        self.variables = {}
        self.functions = {}
        self.urls: list[str] = []

    def detect(self):
        self._traverse(self.tree.root_node, self.variables, self.functions)
        self._detect_urls(self.variables)
        return self.urls
    
    def _detect_urls(self, variables):
        url_pattern = re.compile(r"https?://[^\s]+")
        for var_name, value in variables.items():
            if value is not isinstance(value, str):
                continue
            potential_url = url_pattern.search(value)
            if potential_url:
                self.urls.append(potential_url.group())
        return self.urls

    def _traverse(self, node: Node, variables, functions):
        if node.type == 'string':
            return self.source_code[node.start_byte:node.end_byte].strip('"')
        elif node.type == 'number':
            return node.text.decode()
        elif node.type == 'template_string':
            parts = []
            for child in node.children:
                if child.type in ['template_string_start', 'template_string_end']:
                    continue
                if child.type == 'template_substitution':
                    expression = child.children[1]
                    parts.append(self._traverse(expression, variables, functions))
                else:
                    parts.append(child.text.decode())
            return ''.join(parts)
        elif node.type == 'binary_expression' and node.children[1].type == '+':
            left = self._traverse(node.child_by_field_name("left"), variables, functions)
            right = self._traverse(node.child_by_field_name("right"), variables, functions)

            return (left or '') + (right or '')
        elif node.type in ['assignment_expression', 'variable_declarator']:
            name_node = node.child_by_field_name("name") or node.child_by_field_name("left")
            value_node = node.child_by_field_name("value") or node.child_by_field_name("right")

            var_name = name_node.text.decode()
            value = self._traverse(value_node, variables, functions)
            variables[var_name] = value
            return value
        elif node.type == 'identifier':
            var_name = node.text.decode()
            return variables.get(var_name, '')
        elif node.type == 'call_expression':
            func_name = node.child_by_field_name('function').text.decode()
            args = [self._traverse(arg, variables, functions) for arg in node.child_by_field_name('arguments').named_children if arg.type != 'punctuation']
            if func_name in functions:
                return functions[func_name](*args)
            elif func_name == 'atob':  # Handle Base64 decoding
                return base64.b64decode(args[0]).decode('utf-8')
            elif func_name == 'String.fromCharCode':  # Handle char codes to string
                return ''.join(chr(int(arg)) for arg in args)
            
            # Handle array join (e.g. ['a', 'b'].join('') -> 'ab' | array.join('') -> 'ab' | array.join(' ') -> 'a b')
            elif ".join" in func_name:
                separator = args[0].replace('"', '').replace("'", '')
                array_node = node.child_by_field_name('function').child_by_field_name('object')
                array = self._traverse(array_node, variables, functions)

                return separator.join(array)
            return ''
        elif node.type == 'array':
            elements = [self._traverse(child, variables, functions) for child in node.named_children if child.type != 'punctuation']
            return elements
        elif node.type == 'function_declaration':
            func_name = node.child_by_field_name('name').text.decode()
            functions[func_name] = self._create_function(node, variables, functions)
        elif node.type == 'return_statement':
            return self._traverse(node.named_children[0], variables, functions)
        else:
            for child in node.named_children:
                self._traverse(child, variables, functions)
        return None
    

    def _create_function(self, node: Node, variables: dict, functions: dict):
        """Function to simulate the execution of a function"""

        def func(*args):
            local_vars = {**variables}
            param_list = node.children[2]
            param_names = [param.text.decode() for param in param_list.named_children if param.type == 'identifier']
            for param_name, arg in zip(param_names, args):
                local_vars[param_name] = arg
            body = node.child_by_field_name('body')
            result = None
            for stmt in body.named_children:
                result = self._traverse(stmt, local_vars, functions)
            return result
        return func
    



if __name__ == "__main__":
    # source_code = "let x = \"api\"; x = \"sss\"; var y = \"https://\" + x + \".domain\" + \"ads\"";
    # read src code from file
    file_path = os.path.join(protego_workspace_dir, "src/core/detectors/urls/test_data/urls.js")
    with open(file_path, 'r') as file:
        source_code = file.read()
    tree = parse_js_code(source_code)

    # Traverse the AST and track variable values
    root_node = tree.root_node
    url_detector = URLDetector(tree)
    urls = url_detector.detect()

    # Print tracked variables
    print(json.dumps(url_detector.variables, indent=4))
    # Print detected URLs
    print(urls)
    print(url_detector.functions)

