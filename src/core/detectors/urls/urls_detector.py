import os
import sys

protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
from common_includes import *

#____________________________________________________________________________________#
from core.protego_node import ProtegoTree, ProtegoNode
import base64
import json
import re
from dotenv import load_dotenv


# process.env.VARIABLE
# process.env['VARIABLE']
# const { VARIABLE } = process.env
environment_variable_query = """
(
    (member_expression
        object: (member_expression) @object
        property: (property_identifier) @key) @node
)
(
    (subscript_expression
        object: (member_expression) @object
        index: (string) @key) @node
)
(
    (variable_declarator
        name: (object_pattern (shorthand_property_identifier_pattern) @key)
        value: (member_expression) @object) @node
)
"""

class URLDetector:
    """Class to detect URLs in JavaScript code taking into account variables and functions."""
    def __init__(self, tree: Tree, file_path: str):
        self.tree: ProtegoTree = ProtegoTree(tree)
        self.source_code: str = tree.root_node.text.decode()
        self.variables = {}
        self.functions = {}
        self.urls: list[str] = []
        self.file_path = file_path

    def detect(self):
        self._handle_env_vars()
        self._traverse(self.tree.root, self.variables, self.functions)
        self._detect_urls()
        return self.urls
    
    def _detect_urls(self):
        url_pattern = re.compile(r'https?://[^\s]*')
        for var_name, value in self.variables.items():
            if not isinstance(value, str):
                continue
            matches = url_pattern.findall(value)
            self.urls.extend(matches)

        return self.urls

    def _traverse(self, node: ProtegoNode, variables, functions):
        # in case if it's previously annotated by an env variable
        if node.value:
            return node.value
    
        if node.type == 'string':
            node.value = node.text.strip('"')
            return node.value
        elif node.type == 'number':
            node.value = int(node.text)
            return node.text
        elif node.type == 'template_string':
            parts = []
            for child in node.children:
                if child.type in ['template_string_start', 'template_string_end']:
                    continue
                if child.type == 'template_substitution':
                    expression = child.children[1]
                    parts.append(self._traverse(expression, variables, functions))
                else:
                    parts.append(child.text)
            node.value = ''.join(parts)
            return node.value
        elif node.type == 'binary_expression' and node.children[1].type == '+':
            p_left_node = self.tree.get_node_by_id(node.tree_sitter_node.child_by_field_name("left").id)
            p_right_node = self.tree.get_node_by_id(node.tree_sitter_node.child_by_field_name("right").id)

            left = self._traverse(p_left_node, variables, functions)
            right = self._traverse(p_right_node, variables, functions)

            node.value = (left or '') + (right or '')
            return node.value
        elif node.type in ['assignment_expression', 'variable_declarator']:
            name_node = node.tree_sitter_node.child_by_field_name("name") or node.tree_sitter_node.child_by_field_name("left")
            value_node = node.tree_sitter_node.child_by_field_name("value") or node.tree_sitter_node.child_by_field_name("right")
            p_value_node = self.tree.get_node_by_id(value_node.id)

            var_name = name_node.text.decode()
            value = self._traverse(p_value_node, variables, functions)
            variables[var_name] = value

            node.value = value
            return value
        elif node.type == 'identifier':
            var_name = node.text
            node.value = variables.get(var_name, '')
            return node.value
        elif node.type == 'call_expression':
            func_name = node.tree_sitter_node.child_by_field_name('function').text.decode()
            args = [self._traverse(self.tree.get_node_by_id(arg.id), variables, functions) for arg in node.tree_sitter_node.child_by_field_name('arguments').named_children if arg.type != 'punctuation']
            if func_name in functions:
                node.value = functions[func_name](*args)
            elif func_name == 'atob':  # Handle Base64 decoding
                node.value = base64.b64decode(args[0]).decode('utf-8')
            elif func_name == 'String.fromCharCode':  # Handle char codes to string
                node.value = ''.join(chr(int(arg)) for arg in args)
            
            # Handle array join (e.g. ['a', 'b'].join('') -> 'ab' | array.join('') -> 'ab' | array.join(' ') -> 'a b')
            elif ".join" in func_name:
                separator = args[0].replace('"', '').replace("'", '')
                array_node = node.tree_sitter_node.child_by_field_name('function').child_by_field_name('object')
                p_array_node = self.tree.get_node_by_id(array_node.id)
                array = self._traverse(p_array_node, variables, functions)

                node.value = separator.join(array)
            

            return node.value or ''
        elif node.type == 'array':
            elements = [self._traverse(self.tree.get_node_by_id(child.id), variables, functions) for child in node.named_children if child.type != 'punctuation']
            node.value = elements
            return elements
        elif node.type == 'function_declaration':
            func_name = node.tree_sitter_node.child_by_field_name('name').text.decode()
            functions[func_name] = self._create_function(node, variables, functions)
        elif node.type == 'return_statement':
            return self._traverse(self.tree.get_node_by_id(node.named_children[0].id), variables, functions)
        else:
            for child in node.named_children:
                self._traverse(self.tree.get_node_by_id(child.id), variables, functions)
        return None
    

    def _create_function(self, node: ProtegoNode, variables: dict, functions: dict):
        """Function to simulate the execution of a function"""

        def func(*args):
            local_vars = {**variables}
            param_list = node.children[2]
            param_names = [param.text for param in param_list.named_children if param.type == 'identifier']
            for param_name, arg in zip(param_names, args):
                local_vars[param_name] = arg
            body = node.tree_sitter_node.child_by_field_name('body')
            result = None
            for stmt in body.named_children:
                result = self._traverse(self.tree.get_node_by_id(stmt.id), local_vars, functions)
            return result
        return func
    
    def _handle_env_vars(self):

        captures, matches = query_tree(self.tree.root.tree_sitter_node, environment_variable_query)
        for x in matches:
            match = x[1]

            key_node: Node = match['key']
            expr_node: Node = match['node']

            env_var_name = key_node.text.decode().strip('"').strip("'")
            env_value = self._get_env_var_value(env_var_name)
            self.variables[env_var_name] = env_value

            p_expr_node = self.tree.get_node_by_id(expr_node.id)
            p_expr_node.value = env_value

    def _get_env_var_value(self, env_var_name: str):
        return os.getenv(env_var_name)


    def _find_env_files(self):
        env_files = []
        for root, _, files in os.walk(os.path.dirname(self.file_path)):
            for file in files:
                if file.startswith('.env'):
                    env_files.append(os.path.join(root, file))
        for env_file in env_files:
            load_dotenv(env_file)
        return env_files


if __name__ == "__main__":
    # source_code = "let x = \"api\"; x = \"sss\"; var y = \"https://\" + x + \".domain\" + \"ads\"";
    # read src code from file
    file_path = os.path.join(protego_workspace_dir, "src/core/detectors/urls/test_data/urls.js")
    with open(file_path, 'r') as file:
        source_code = file.read()
    tree = parse_js_code(source_code)

    # Traverse the AST and track variable values
    root_node = tree.root_node
    url_detector = URLDetector(tree, file_path)
    urls = url_detector.detect()

    # Print tracked variables
    print(json.dumps(url_detector.variables, indent=4))
    # Print detected URLs
    print(url_detector.urls)
    print(url_detector.functions)

