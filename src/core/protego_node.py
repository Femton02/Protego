import os
import sys

protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
from common_includes import *

#____________________________________________________________________________________#

class ProtegoNode:
    def __init__(self, node: Node):
        self.children = []
        self.named_children = []
        self.parent = None
        self.type = node.type
        self.text = node.text
        self.start_point = node.start_point
        self.end_point = node.end_point
        self.id = node.id
        self.points_to = None

    def __str__(self):
        return f"Node: {self.type} ({self.text})"
    
class ProtegoTree:
    def __init__(self, tree: Tree):
        self.original_tree = tree
        self.node_mapping = {}  # Dictionary to map original nodes to ProtegoNodes
        self.root = self._wrap_node(tree.root_node)

    def _wrap_node(self, node: Node, parent: ProtegoNode = None) -> ProtegoNode:
        protego_node = ProtegoNode(node)
        protego_node.parent = parent
        self.node_mapping[node] = protego_node  # Map the original node to the ProtegoNode
        protego_node.children = [self._wrap_node(child, protego_node) for child in node.children]
        protego_node.named_children = [self._wrap_node(child, protego_node) for child in node.named_children]
        return protego_node

    def __str__(self):
        return f"ProtegoTree with root: {self.root}"