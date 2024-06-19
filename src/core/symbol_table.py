import os
import sys

protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
from common_includes import *

#____________________________________________________________________________________#
from core.protego_node import ProtegoNode, ProtegoTree

class SymbolTable:
    def __init__(self, parent: 'SymbolTable' = None):
        self.table = {}  # dictionary of variables in the current scope
        self.children = []  # list of scopes that are children of the current scope
        self.parent = parent  # parent scope
        self.aliases = {}  # dictionary to map variable names to their aliases

    def add_child(self, child: 'SymbolTable'):
        self.children.append(child)
        child.parent = self

    def add_variable(self, var_name: str, node: ProtegoNode):
        self.table[var_name] = node

    def add_alias(self, var_name: str, alias: str):
        if var_name == alias:
            return
        if var_name not in self.aliases:
            self.aliases[var_name] = []
        if alias not in self.aliases[var_name]:
            self.aliases[var_name].append(alias)

    def remove_aliases(self, var_name: str):
        if var_name in self.aliases:
            del self.aliases[var_name]

    def __str__(self):
        return f"SymbolTable: {self.table}, Children: {len(self.children)}, Aliases: {self.aliases}"

class SymbolTableBuilder:
    def __init__(self):
        self.root_symbol_table = SymbolTable()

    def build(self, root: ProtegoNode):
        self._traverse(root, self.root_symbol_table)

    def _traverse(self, node: ProtegoNode, current_symbol_table: SymbolTable):
        node.symbol_table = current_symbol_table  # Set the symbol table reference
        if node.type == "statement_block" or node.type == "object":
            new_scope = SymbolTable(current_symbol_table)
            current_symbol_table.add_child(new_scope)
            self._process_block(node, new_scope)
        else:
            self._handle_node_logic(node, current_symbol_table)
            for child in node.children + node.named_children:
                self._traverse(child, current_symbol_table)

    def _process_block(self, node: ProtegoNode, new_scope: SymbolTable):
        for child in node.children + node.named_children:
            self._traverse(child, new_scope)

    def _handle_node_logic(self, node: ProtegoNode, current_symbol_table: SymbolTable):
        node.symbol_table = current_symbol_table  # Set the symbol table reference
        if node.type == "lexical_declaration":
            var = self.find_first_identifier(node)
            var_name = var.text.decode()
            current_symbol_table.add_variable(var_name, node)
            self._add_aliases(node, current_symbol_table, var_name)
        elif node.type == "variable_declaration":
            var = self.find_first_identifier(node)
            var_name = var.text.decode()
            current_symbol_table.add_variable(var_name, node)
            self.add_global_variable(current_symbol_table, var_name, node)
            self._add_aliases(node, current_symbol_table, var_name)
        elif node.type in {"assignment_expression", "augmented_assignment_expression"}:
            var = node.named_children[0]
            var_name = var.text.decode()
            self._update_variable_reference(current_symbol_table, var, node, var_name)
        elif node.type == "pair":
            var = node.named_children[0]
            var_name = var.text.decode()
            current_symbol_table.add_variable(var_name, node)
            self._add_aliases(node, current_symbol_table, var_name)

    def add_global_variable(self, current_symbol_table: SymbolTable, var_name: str, node: ProtegoNode):
        global_table = current_symbol_table.parent
        while global_table and global_table.parent:
            global_table = global_table.parent
        if global_table:
            global_table.add_variable(var_name, node)

    def _update_variable_reference(self, current_symbol_table: SymbolTable, var: ProtegoNode, node: ProtegoNode, var_name: str):
        current_table = self._find_variable_in_scope_chain(current_symbol_table, var_name)
        if current_table:
            # Remove existing aliases for the variable
            self._remove_aliases_in_scope_chain(current_table, var_name)
            # Add new aliases for the variable
            self._add_aliases(node, current_table, var_name)
            existing_node = current_table.table[var_name]
            node.points_to = existing_node
            current_table.table[var_name] = node
        else:
            current_symbol_table.add_variable(var_name, node)
        self._update_aliases_in_scope_chain(current_symbol_table, var_name, var_name)

    def _remove_aliases_in_scope_chain(self, symbol_table: SymbolTable, var_name: str):
        current = symbol_table
        while current:
            current.remove_aliases(var_name)
            current = current.parent

    def _find_variable_in_scope_chain(self, symbol_table: SymbolTable, var_name: str):
        current = symbol_table
        while current:
            if var_name in current.table:
                return current
            current = current.parent
        return None

    def _update_aliases_in_scope_chain(self, symbol_table: SymbolTable, var_name: str, alias: str):
        current = symbol_table
        while current:
            current.add_alias(var_name, alias)
            current = current.parent

    def _add_aliases(self, node: ProtegoNode, symbol_table: SymbolTable, var_name: str):
        identifiers = self._find_all_identifiers(node)
        for identifier in identifiers:
            alias = identifier.text.decode()
            current = symbol_table
            while current:
                current.add_alias(var_name, alias)
                current = current.parent
            # Add logic for property identifiers
            if identifier.parent and identifier.parent.type == "property_identifier":
                property_identifier = identifier.parent.text.decode()
                current = symbol_table
                while current:
                    current.add_alias(property_identifier, alias)
                    current = current.parent

    def _find_all_identifiers(self, node: ProtegoNode):
        identifiers = []
        if node.type == "identifier":
            identifiers.append(node)
        for child in node.named_children:
            identifiers.extend(self._find_all_identifiers(child))
        return identifiers

    def find_first_identifier(self, node: ProtegoNode):
        if node.type == "identifier":
            return node
        for child in node.named_children:
            result = self.find_first_identifier(child)
            if result:
                return result
        return None

    def __str__(self):
        return str(self.root_symbol_table)
