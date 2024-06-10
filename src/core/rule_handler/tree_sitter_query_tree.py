import os
import sys
protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
from common_includes import *


from t_sitter.tree_sitter_utils import parse_js_code, traverse_tree, visualize_tree, query_tree, Node, Tree
import graphviz
import random

class QTNode:
    """
    This class is used to represent a node in the query graph.
    """
    
    def __init__(self, value: str, text: str = None):
        self.id = random.randint(0, 100000) # random id for visualization
        self.child_index = None
        self.value = value
        self.text = text
        self.children = []
        self.parent = None
    
    def add_child(self, child: 'QTNode'):
        """
        This function adds a child to the node.
        
        Args:
            child (QGNode): The child node
        """
        child.child_index = len(self.children) + 1
        self.children.append(child)
        child.set_parent(self)
    
    def set_parent(self, parent: 'QTNode'):
        """
        This function sets the parent of the node.
        
        Args:
            parent (QGNode): The parent node
        """
        self.parent = parent

    def get_parent(self) -> 'QTNode':
        """
        This function gets the parent of the node.
        
        Returns:
            QGNode: The parent node
        """
        return self.parent
    
    def delete_child_index(self, index: int):
        """
        This function deletes the child at the given index.
        
        Args:
            index (int): The index of the child
        """
        self.children[index].parent = None
        self.children.pop(index)


    
    
    def __str__(self):
        return f"Node({self.child_index}, {self.value}, {self.children})"

class TSQueryTree:
    """
    This class is used to represent the query for a tree-sitter as a tree.
    """
    
    def __init__(self, root: Node, catch: dict = {}, trace: list = []):
        self.TS_root = root
        self.root: QTNode = QTNode("", root.text.decode())
        self.query_str = ""
        self.counter = 1
        self.catch = catch
        self.variables = {}
        self.content = {}
        self.trace = trace

    
    
    def build_query_str(self, node: QTNode):
        """
        This function builds the query string from the query tree.
        """
        if not node:
            return
        self.query_str += node.value + " "
        for child in node.children:
            self.build_query_str(child)
        
        return self.query_str

    def visualize_query_tree(self):
        """
        This function visualizes the query tree.
        """
        graph = graphviz.Digraph(format="png")
        root = self.root
        queue = [root]
        while queue:
            curr_node = queue.pop(0)
            if not curr_node:
                continue
            graph.node(str(curr_node.id), str(curr_node.value))
            if curr_node.parent:
                graph.edge(str(curr_node.parent.id), str(curr_node.id))
            for child in curr_node.children:
                queue.append(child)
        
        graph.render("./visualization/" + "query_tree")

    def handle_ellipsis(self, node: QTNode):
        # traverse the tree
        if node.text != None and len(node.text) > 39:
            if node.text[39:] == "ELLIPSIS":
                return True
        to_be_deleted = set()
        am_i_ellipsis = False
        for index, child in enumerate(node.children):
            if self.handle_ellipsis(child):
                to_be_deleted.add(index - 1)
                to_be_deleted.add(index)
                to_be_deleted.add(index + 1)
                if(node.value == "(field_definition" or node.value == "(expression_statement"):
                    am_i_ellipsis = True
            else:
                continue
        to_be_deleted = sorted(to_be_deleted, reverse=True)
        for i in to_be_deleted:
            node.delete_child_index(i)
        if node.value == "(pair" and len(node.children) == 1:
            am_i_ellipsis = True
        return am_i_ellipsis
    
    def handle_for(self, node: QTNode):
        if node.text != None and len(node.text) > 39:
            if node.text[39:] == "FOR":
                return True
        for index, child in enumerate(node.children):
            if self.handle_for(child):
                if node.value == "(for_statement":
                    node.children[index].value = "(_"
                else:
                    for i in range(3):
                        node.delete_child_index(index -1)
                    node.value = "(_"
            else:
                continue
        return False
    
    def handle_ellipsis_and_for(self, node: QTNode):
        self.handle_ellipsis(node)
        self.handle_for(node)

#____________________________________________________________________________________#
#                             MAIN FUCNTION IN CLASS
#____________________________________________________________________________________#   


    def build_query_tree(self, node: Node, parent: QTNode):
        """
        This function builds the query tree from the TS_root.
        """
        curr_node = QTNode("(" + node.type, node.text.decode())
        parent.add_child(curr_node)
        parent = curr_node
        for child in node.named_children:
            if child == node.named_child(0):
                parent.add_child(QTNode("."))
            self.build_query_tree(child, curr_node)
            parent.add_child(QTNode("."))
        parent.add_child(QTNode(")"))

        if(node.named_child_count == 0):
            if(len(node.text.decode()) > 39):
                if(node.text.decode()[39:] in self.catch and node.text.decode()[39:] != "_" and node.text.decode()[39:] != "ELLIPSIS"):
                    if(self.catch[node.text.decode()[39:]] == node.text.decode()[1:39]):
                        parent.add_child(QTNode("@param" + str(self.counter)))
                        parent.value = "(_"
                        self.variables[self.counter] = node.text.decode()[39:]
                        curr_node.value = "(_"
                        self.counter += 1
                    else:
                        parent.add_child(QTNode("@param" + str(self.counter)))
                        self.content[self.counter] = node.text.decode()
                        self.counter += 1
                if node.text.decode()[39:] == "_":
                    curr_node.value = "(_"
                if(node.text.decode()[39:] == "FOCUS" and node.text.decode()[1:39] == self.trace[0][1]):
                        if self.trace[0][2] == "LITERAL":
                            self.content[-1] = self.trace[0][0]
                        else:
                            if self.trace[0][0] != "_":
                                self.variables[-1] = self.trace[0][0]
                        parent.add_child(QTNode("@focus"))
            else:
                parent.add_child(QTNode("@param" + str(self.counter)))
                self.content[self.counter] = node.text.decode()
                self.counter += 1


if __name__ == "__main__":
    pass