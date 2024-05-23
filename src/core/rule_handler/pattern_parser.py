import os
import sys
protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
from common_includes import *

from t_sitter.tree_sitter_utils import parse_js_code, traverse_tree, visualize_tree, query_tree, Node
from rule_handler.tree_sitter_query_tree import QTNode, TSQueryTree
import uuid
import re

#____________________________________________________________________________________#
#                                 HELPER FUNCTIONS
#____________________________________________________________________________________#   


def pattern_preprocessing(pattern: str) -> tuple[str, dict, dict, dict]:
    variablepattern = r'(\$<(\w+)>)'        #pattern to catch variables
    ellipsispattern = r'(\$<(\.\.\.)>)'     #pattern to catch ellipsis
    forpattern = r'for\((\$<\.\.\.>)\)'     #pattern to catch for loops
    typepattern = r'(\$<((\w+):\s*(\w+))>)'      #pattern to catch types
    focuspattern = r'(\$<!>((\$<)?(\w*)>?))' #pattern to catch focus
    catches = {}
    types = {}
    trace = []
    uuidobj = uuid.uuid4()
    uuidstr = str(uuidobj.int)[0:38] #to ensure fixed length

    for match in re.finditer(focuspattern, pattern):
        if(match.group(2) == match.group(4)):
            trace.append([match.group(4), uuidstr, "LITERAL"])
        else:
            trace.append([match.group(4), uuidstr, "VARIABLE"])
    outputstr = re.sub(focuspattern, "_"+ uuidstr +"FOCUS", pattern) #replace focus with a regular variable

    for match in re.finditer(typepattern, pattern):
        types[match.group(3)] = match.group(4)
    outputstr = re.sub(typepattern, "$<" +r'\3' + ">", outputstr)

    for match in re.finditer(variablepattern, outputstr):
        catches[match.group(2)] = uuidstr
    outputstr = re.sub(variablepattern, "_"+ uuidstr +r'\2', outputstr)
    
    forstr = "for(_" + uuidstr + "FOR; _" + uuidstr + "FOR; _" + uuidstr + "FOR)"
    outputstr = re.sub(forpattern, forstr, outputstr) #replace for loops with a unique string

    for match in re.finditer(ellipsispattern, outputstr):
        catches["ELLIPSIS"] = uuidstr
    outputstr = re.sub(ellipsispattern, "_"+ uuidstr + "ELLIPSIS", outputstr) #replace ellipsis with a unique string


    return outputstr, catches, types, trace

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
    preprocessedpattern, catch, types, trace = pattern_preprocessing(pattern)
    tree = parse_js_code(preprocessedpattern)
    root = get_first_multi_children_node(tree)
    tsqt = TSQueryTree(root, catch, trace)
    tsqt.build_query_tree(root, tsqt.root)
    tsqt.handle_ellipsis_and_for(tsqt.root)
    query = tsqt.build_query_str(tsqt.root)[1:] + "@root"
    variables = tsqt.variables
    content = tsqt.content
    tsqt.visualize_query_tree()
    return query, variables, content, types


if __name__ == "__main__":
    query, var, cont, types = parse_pattern("var x = 2;")
    print(query)
    print(var)
    print(cont)
    print(types)

# ((identifier) @match1
# (#eq? @match1 "x"))