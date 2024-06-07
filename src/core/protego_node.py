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
        self.children: list[ProtegoNode] = []
        self.named_children: list[ProtegoNode] = []
        self.parent: ProtegoNode = None
        self.type: str = node.type
        self.text: str = node.text.decode()
        self.start_point = node.start_point
        self.end_point = node.end_point
        self.id = node.id
        self.points_to = None
        self.tree_sitter_node: Node = node

    def __str__(self):
        return f"Node: {self.id}, text: {self.text}"
    
class ProtegoTree:
    def __init__(self, tree: Tree):
        # TODO: Delete this
        self.original_tree = tree
        self.tree_sitter_tree = tree
        self.tree_sitter_nodes_map: dict[int, ProtegoNode] = dict()
        self.node_mapping = {}  # Dictionary to map original nodes to ProtegoNodes
        self.root = self._wrap_node(tree.root_node)

    def _wrap_node(self, node: Node, parent: ProtegoNode = None) -> ProtegoNode:
        protego_node = ProtegoNode(node)
        protego_node.parent = parent
        self.node_mapping[node] = protego_node  # Map the original node to the ProtegoNode
        protego_node.children = [self._wrap_node(child, protego_node) for child in node.children]
        protego_node.named_children = [self._wrap_node(child, protego_node) for child in node.named_children]
        self.tree_sitter_nodes_map[protego_node.id] = protego_node
        return protego_node
    
    def get_node_by_id(self, node_id: int) -> ProtegoNode:
        return self.tree_sitter_nodes_map.get(node_id)

    def __str__(self):
        return f"ProtegoTree with root: {self.root} and {len(self.tree_sitter_nodes_map)} nodes."



if __name__ == "__main__":
    tree = parse_js_code("const x = {a: 1, b: 2};")
    protego_tree = ProtegoTree(tree)
    print(protego_tree)
