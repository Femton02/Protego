from tree_sitter import Parser, Language, Tree, Node
from typing import Generator

JS_LANGUAGE = Language("./tree-sitter/build/my-languages.so", "javascript")

def get_js_parser() -> Parser:
    parser = Parser()
    parser.set_language(JS_LANGUAGE)
    return parser

def parse_js_code(js_code: str) -> Tree:
    parser = get_js_parser()
    tree = parser.parse(bytes(js_code, "utf8"))
    return tree

def traverse_tree(tree: Tree) -> Generator[Node, None, None]:
    """
    Traverse the tree in depth-first order (pre-order traversal) and yield each node.

    Example usage:
    Read about generators and the yield keyword in Python here: https://docs.python.org/3/tutorial/classes.html#generators
        - either using a for loop:
            ```python
            node_gen_object = traverse_tree(tree)
                for node in node_gen_object:
                    print(node)
            ```
        - or the next() function:
            ```python
            node_gen_object = traverse_tree(tree)
            while True:
                try:
                    node = next(node_gen_object)
                    print(node)
                except StopIteration:
                    break
            ```

    Args:
        tree (Tree): The tree to traverse (root node of the tree)

    Yields:
        Generator[Node, None, None]: A generator that yields each node in the tree
    """
    cursor = tree.walk()

    visited_children = False
    while True:

        if not visited_children:
            yield cursor.node # the return value will be used as the input for the next call for the function
            # code will continue from here after the generator is resumed (in the next call for the function)
            if not cursor.goto_first_child(): #goto_first_child() returns False if the cursor doesn't have any children
                visited_children = True
        elif cursor.goto_next_sibling():
            visited_children = False
        elif not cursor.goto_parent():
            break

def edit_tree(
        new_src: str,
        old_tree: Tree,
        start_byte: int,
        old_end_byte: int,
        new_end_byte: int,
        start_point: tuple[int, int],
        old_end_point: tuple[int, int],
        new_end_point: tuple[int, int],
    ) -> Tree:
    """
    Edit the syntax tree to reflect the changes made to the source code.

    Example usage:
    ```python
        old_src = "a = 1;"
        old_tree = parse_js_code(old_src)
        addition = "let "
        new_src = addition + old_src
        new_tree = edit_tree(
            new_src,
            old_tree,
            start_byte=0,
            old_end_byte=0,
            new_end_byte=len(addition),
            start_point=(0, 0),
            old_end_point=(0, 0),
            new_end_point=(0, len(addition)),
        )
    ```

    Args:
        new_src (str): The new source code
        old_tree (Tree): The old syntax tree
        start_byte (int): The starting byte index of the edit in the edited source code.
        old_end_byte (int): The ending byte index of the edit in the original source code (if the edit is an insertion, this should be the same as start_byte)
        new_end_byte (int): The ending byte index of the edit in the edited source code.
        start_point (tuple[int, int]): The starting position (line and column numbers) of the edit in the edited source code.
        old_end_point (tuple[int, int]): The ending position (line and column numbers) of the edit in the original source code.
        new_end_point (tuple[int, int]): The ending position (line and column numbers) of the edit in the edited source code.

    Returns:
        Tree: The new syntax tree
    """

    old_tree.edit(
        start_byte=start_byte,
        old_end_byte=old_end_byte,
        new_end_byte=new_end_byte,
        start_point=start_point,
        old_end_point=old_end_point,
        new_end_point=new_end_point,
    )
    parser = get_js_parser()
    new_tree = parser.parse(bytes(new_src, "utf8"), old_tree)
    return new_tree

def test_edit_tree():
    src_code = "a = 1;"
    tree = parse_js_code(src_code)
    node_gen_object = traverse_tree(tree)
    for node in node_gen_object:
        print(node)

    new_tree = edit_tree(
        new_src="const " + src_code,
        old_tree=tree,
        start_byte=0,
        old_end_byte=0,
        new_end_byte=5,
        start_point=(0, 0),
        old_end_point=(0, 0),
        new_end_point=(0, 5),
    )

    # get_changed_ranges returns a list of Range objects that represent the byte ranges of the source code that were changed between the old tree and the new tree.
    for changed_range in tree.changed_ranges(new_tree):
        print("Changed range:")
        print(f"  Start point {changed_range.start_point}")
        print(f"  Start byte {changed_range.start_byte}")
        print(f"  End point {changed_range.end_point}")
        print(f"  End byte {changed_range.end_byte}")

    node_gen_object = traverse_tree(new_tree)
    for node in node_gen_object:
        print(node)

def query_tree(tree: Tree, query_str: str) -> tuple[list[tuple[Node, str]], list[tuple[int, dict]]]:
    """Query the tree using the given query string.

    Read more about tree-sitter queries here: https://tree-sitter.github.io/tree-sitter/using-parsers#pattern-matching-with-queries

    Args:
        tree (Tree): The tree to query
        query_str (str): The query string

    Returns:
        capture, matches
        - List of captures:
            - each containing a node and the name of the capture that matched the node
        - List of matches:
            - each containing an int (which we don't know it's meaning yet) and
                a dictionary of the captures that matched the node and relevant info
    """    
    try:
        query = JS_LANGUAGE.query(query_str)
    except Exception as e:
        print(e)
        print("Error in query")

    captures = query.captures(tree.root_node)

    # print("Captures:")
    # for capture in captures:
    #     print(capture[0]) # Node
    #     print(capture[1]) # Capture name

    matches = query.matches(tree.root_node)
    # print("Matches:")
    # for match in matches:
    #     print(match) # Match object (0, {'assig-expr': <Node type=assignment_expression, start_point=(0, 0), end_point=(0, 5)>, 'num-value': <Node type=number, start_point=(0, 4), end_point=(0, 5)>})

    return captures, matches

def test_query_tree():
    tree = parse_js_code("a = 1; z = 2; console.log(a);")
    query_tree(tree, "(assignment_expression (number) @num-value)  @assig-expr")

# test_edit_tree()
# test_query_tree()


