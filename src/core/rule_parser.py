from t_sitter.tree_sitter_utils import parse_js_code, traverse_tree, visualize_tree, query_tree, Node
from tree_sitter_query_tree import QTNode, TSQueryTree
import uuid
import re

#____________________________________________________________________________________#
#                                 HELPER FUNCTIONS
#____________________________________________________________________________________#   


def rule_preprocessing(rule: str) -> tuple[str, dict]:
    variablepattern = r'(\$<(\w+)>)'        #pattern to catch variables
    ellipsispattern = r'(\$<(\.\.\.)>)'     #pattern to catch ellipsis
    forpattern = r'for\((\$<\.\.\.>)\)'     #pattern to catch for loops
    catches = {}
    uuidobj = uuid.uuid4()
    uuidstr = str(uuidobj.int)[0:38] #to ensure fixed length
    for match in re.finditer(variablepattern, rule):
        catches[match.group(2)] = uuidstr
    outputstr = re.sub(variablepattern, "_"+ uuidstr +r'\2', rule)
    
    forstr = "for(_" + uuidstr + "FOR; _" + uuidstr + "FOR; _" + uuidstr + "FOR)"
    outputstr = re.sub(forpattern, forstr, outputstr) #replace for loops with a unique string

    for match in re.finditer(ellipsispattern, outputstr):
        catches["ELLIPSIS"] = uuidstr
    outputstr = re.sub(ellipsispattern, "_"+ uuidstr + "ELLIPSIS", outputstr) #replace ellipsis with a unique string


    return outputstr, catches

def get_first_multi_children_node(tree):
    last_node = None
    for node in traverse_tree(tree):
        if len(node.children) > 1:
            return node
        last_node = node
    return last_node


#____________________________________________________________________________________#
#                                   ENTRY POINT
#____________________________________________________________________________________#   

def parse_rule(rule: str) -> tuple[str, dict, dict]:
    preprocessedrule, catch = rule_preprocessing(rule)
    tree = parse_js_code(preprocessedrule)
    root = get_first_multi_children_node(tree)
    tsqt = TSQueryTree(root, catch)
    tsqt.build_query_tree(root, tsqt.root)
    tsqt.handle_ellipsis_and_for(tsqt.root)
    query = tsqt.build_query_str(tsqt.root) + "@content"
    variables = tsqt.variables
    content = tsqt.content
    tsqt.visualize_query_tree()
    return query, variables, content


query, var, cont = parse_rule("const letters = new Set([$<...>, 1]);")
print(query)
print(var)
print(cont)