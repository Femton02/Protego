from t_sitter.tree_sitter_utils import parse_js_code, traverse_tree, visualize_tree, query_tree, Node
import uuid
import re

def rule_preprocessing(rule: str) -> tuple[str, dict]:
    regexpattern = r'(\$<(\w+)>)'
    variables = {}
    uuidobj = uuid.uuid4()
    uuidstr = str(uuidobj.int)[0:38] #to ensure fixed length
    for match in re.finditer(regexpattern, rule):
        variables[match.group(2)] = uuidstr
    outputstr = re.sub(regexpattern, "_"+ uuidstr +r'\2', rule)
    return outputstr, variables

def get_first_multi_children_node(tree):
    last_node = None
    for node in traverse_tree(tree):
        if len(node.children) > 1:
            return node
        last_node = node
    return last_node

def traverse_anas(node: Node, counter: int,  catch: dict, variables: dict, content: dict, level: int = 1) -> tuple[str, int, dict, dict, dict]:
    # create string "(node.type + all my children's strings)"
    query = "(" + node.type + "\n"
    for i in range(level):
        query += "    "
    for child in node.named_children:
        if child == node.named_child(0):
            query += " ."
        concatquery, counter, _, _, _ = traverse_anas(child, counter, catch, variables, content, level+1)
        query += concatquery
        query += " ."
    query += "\n"
    for i in range(level-1):
        query += "    "
    query += ")"
    if (node.child_count < 1):
        if(len(node.text.decode()) > 39): #check if length is bigger than 39 (uuid length)
            if(node.text.decode()[39:] in catch and node.text.decode()[39:] != "_"): #if it is in variables dict and is named
                if(catch[node.text.decode()[39:]] == node.text.decode()[1:39]): #if the uuid matches then add it
                    query += "@param" + str(counter)
                    variables[counter] = node.text.decode()[39:]
                    counter += 1
        else: #the size is less than 39 then it is literal match
            query += "@param" + str(counter)
            content[counter] = node.text.decode()
            counter += 1
    query += "\n"
    for i in range(level-1):
        query += "    "
    return query, counter, catch, variables, content
    

def parse_rule(rule: str) -> tuple[str, dict, dict]:
    preprocessedrule, catch = rule_preprocessing(rule)
    tree = parse_js_code(preprocessedrule)
    root = get_first_multi_children_node(tree)
    visualize_tree(tree)
    variables = {}
    content = {}
    query, _, _, variables, content = traverse_anas(root, 1, catch, variables, content)

    return query, variables, content

query, var, cont = parse_rule("x = 1;_;x = 3;")
print(query)
print(var)
print(cont)


# <Node type=import_statement, start_point=(0, 0), end_point=(0, 40)>
# <Node type="import", start_point=(0, 0), end_point=(0, 6)>
# <Node type=import_clause, start_point=(0, 7), end_point=(0, 20)>
# <Node type=named_imports, start_point=(0, 7), end_point=(0, 20)>