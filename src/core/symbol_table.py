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

    def add_child(self, child: 'SymbolTable'):
        self.children.append(child)
        child.parent = self

    def __str__(self):
        return f"SymbolTable: {self.table}, Children: {len(self.children)}"

class SymbolTableBuilder:
    def __init__(self):
        self.root_symbol_table = SymbolTable()

    def build(self, protego_tree: ProtegoTree):
        self._traverse(protego_tree.root, self.root_symbol_table)

    def _traverse(self, node: ProtegoNode, current_symbol_table: SymbolTable):
        if node.type == "statement_block":
            new_scope = SymbolTable(current_symbol_table)
            current_symbol_table.add_child(new_scope)
            self._process_block(node, new_scope)
        else:
            self._handle_node_logic(node, current_symbol_table)
            for child in node.children:
                self._traverse(child, current_symbol_table)

    def _process_block(self, node: ProtegoNode, new_scope: SymbolTable):
        for child in node.children:
            self._traverse(child, new_scope)

    def _handle_node_logic(self, node: ProtegoNode, current_symbol_table: SymbolTable):
        # TODO: Custom logic for handling other node types like lexical declarations, variable declarations, etc.
        if node.type == "lexical_declaration":                  # example: let x = 5;
            var = self.find_first_identifier(node)
            current_symbol_table.table[var.text.decode()] = node
        if node.type == "variable_declaration":                 # example: var x = 5;
            var = self.find_first_identifier(node)
            # put the node in the global symbol table
            current_symbol_table.table[var.text.decode()] = node
            globaltable = current_symbol_table.parent
            if globaltable is not None:
                while globaltable.parent is not None:
                    globaltable = globaltable.parent
                globaltable.table[var] = node
        if node.type == "expression_statement":                # example: x = 5;
            var = self.find_first_identifier(node)
            # look for the variable in the symbol table
            if var.text.decode() in current_symbol_table.table:
                var.points_to = current_symbol_table.table[var.text.decode()]
                current_symbol_table.table[var.text.decode()] = node
            else:
                # look for the variable in all the parent scopes, if didn't find it, put it in the current scope
                parent = current_symbol_table.parent
                while parent is not None:
                    if var.text.decode() in parent.table:
                        var.points_to = parent.table[var.text.decode()]
                        parent.table[var.text.decode()] = node
                        break
                    parent = parent.parent
                if parent is None:  # if the variable is not found in any of the parent scopes, put it in the current scope
                    current_symbol_table.table[var.text.decode()] = node
        pass

    def find_first_identifier(self, node: ProtegoNode):
        if node.type == "identifier" or node.type == "property_identifier":
            return node
        for child in node.named_children:
            return self.find_first_identifier(child)

    def __str__(self):
        return str(self.root_symbol_table)