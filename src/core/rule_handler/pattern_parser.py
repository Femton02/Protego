from t_sitter.tree_sitter_utils import parse_js_code, traverse_tree, visualize_tree, query_tree, Node
from .tree_sitter_query_tree import QTNode, TSQueryTree
import uuid
import re

#____________________________________________________________________________________#
#                                 HELPER FUNCTIONS
#____________________________________________________________________________________#   


def pattern_preprocessing(pattern: str) -> tuple[str, dict, dict]:
    variablepattern = r'(\$<(\w+)>)'        #pattern to catch variables
    ellipsispattern = r'(\$<(\.\.\.)>)'     #pattern to catch ellipsis
    forpattern = r'for\((\$<\.\.\.>)\)'     #pattern to catch for loops
    typepattern = r'(\$<((\w+):(\w+))>)'      #pattern to catch types
    catches = {}
    types = {}
    uuidobj = uuid.uuid4()
    uuidstr = str(uuidobj.int)[0:38] #to ensure fixed length

    for match in re.finditer(typepattern, pattern):
        types[match.group(3)] = match.group(4)
    outputstr = re.sub(typepattern, "$<" +r'\3' + ">", pattern)

    for match in re.finditer(variablepattern, outputstr):
        catches[match.group(2)] = uuidstr
    outputstr = re.sub(variablepattern, "_"+ uuidstr +r'\2', outputstr)
    
    forstr = "for(_" + uuidstr + "FOR; _" + uuidstr + "FOR; _" + uuidstr + "FOR)"
    outputstr = re.sub(forpattern, forstr, outputstr) #replace for loops with a unique string

    for match in re.finditer(ellipsispattern, outputstr):
        catches["ELLIPSIS"] = uuidstr
    outputstr = re.sub(ellipsispattern, "_"+ uuidstr + "ELLIPSIS", outputstr) #replace ellipsis with a unique string


    return outputstr, catches, types

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

def parse_pattern(pattern: str) -> tuple[str, dict, dict, dict]:
    preprocessedpattern, catch, types = pattern_preprocessing(pattern)
    tree = parse_js_code(preprocessedpattern)
    root = get_first_multi_children_node(tree)
    tsqt = TSQueryTree(root, catch)
    tsqt.build_query_tree(root, tsqt.root)
    tsqt.handle_ellipsis_and_for(tsqt.root)
    query = tsqt.build_query_str(tsqt.root) + "@content"
    variables = tsqt.variables
    content = tsqt.content
    tsqt.visualize_query_tree()
    return query, variables, content, types


# query, var, cont, types = parse_pattern("app.use($<...>,serveIndex(),$<...>)")
# print(query)
# print(var)
# print(cont)
# print(types)