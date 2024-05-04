from t_sitter.tree_sitter_utils import parse_js_code, traverse_tree, visualize_tree, query_tree, Node, Tree
import graphviz
import random

class QTNode:
    """
    This class is used to represent a node in the query graph.
    """
    
    def __init__(self, value: str):
        self.id = random.randint(0, 100000)
        self.child_index = None
        self.value = value
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
    
    
    def __str__(self):
        return f"Node({self.child_index}, {self.value}, {self.children})"

class TSQueryTree:
    """
    This class is used to represent the query for a tree-sitter as a tree.
    """
    
    def __init__(self, root: Node):
        self.TS_root = root
        self.root: QTNode = QTNode("root")
        self.query_str = ""
    
    def build_query_tree(self, node: Node, parent: QTNode):
        """
        This function builds the query tree from the TS_root.
        """
        curr_node = QTNode("(" + node.type)
        parent.add_child(curr_node)
        parent = curr_node
        for child in node.named_children:
            if child == node.named_child(0):
                parent.add_child(QTNode("."))
            self.build_query_tree(child, curr_node)
            parent.add_child(QTNode("."))
        
        parent.add_child(QTNode(")"))
    
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
            graph.node(str(curr_node.id), str(curr_node.value) + " " + str(curr_node.child_index))
            if curr_node.parent:
                graph.edge(str(curr_node.parent.id), str(curr_node.id))
            for child in curr_node.children:
                queue.append(child)
        
        graph.render("./visualization/" + "query_tree")

def test_query_tree():
    tree = parse_js_code("func(a, b)")
    ts_query_tree = TSQueryTree(tree.root_node)
    ts_query_tree.build_query_tree(tree.root_node, ts_query_tree.root)
    query_str = ts_query_tree.build_query_str(ts_query_tree.root)
    ts_query_tree.visualize_query_tree()
    print(query_str)

test_query_tree()
            


        
