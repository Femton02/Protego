from rule_handler.rule_parser import process_rule

process_rule("test/rules/rule.yaml")




# def read_file(file_path):
#     with open(file_path, "r") as file:
#         return file.read()

# src_code = read_file("../../test/express/hardcoded-secret/testdata/hardcoded_secret_in_jwt.js")
# # print(src_code)

# tree = parse_js_code(src_code)
# visualize_tree(tree)
# node_gen_object = traverse_tree(tree)
# for node in node_gen_object:
#     print(node)


# # default_import_query = """
# # (import_statement
# #     (import_clause
# #         (identifier) @import_identifier
# #     )
# #     (string
# #         (string_fragment) @library_name (#eq? @library_name "expressjwt")
# #     ) @string
# # )
# # """

# # require_import_query = """
# # (variable_declarator
# #     (identifier) @import_identifier
# #     (call_expression
# #         (identifier) @require_identifier (#eq? @require_identifier "require")
# #         (arguments
# #             (string
# #                 (string_fragment) @library_name (#eq? @library_name "expressjwt")
# #             )
# #         )
# #     ) @require_call
# # )
# # """

# # captures, matches = query_tree(tree, default_import_query)


# # print("=====")
# # for capture in captures:
# #     print(capture)

# # print("=====")
# # for match in matches:
# #     print(match)

# # print("=====")
# # captures, matches = query_tree(tree, require_import_query)
# # print("=====")
# # for capture in captures:
# #     print(capture)

# # print("=====")
# # for match in matches:
# #     print(match)


# detect_hardcoded_secret_query = """
# (variable_declarator
#     (identifier) @import_identifier
#     (call_expression
#         (identifier) @require_identifier (#eq? @require_identifier "require")
#         (arguments
#             (string
#                 (string_fragment) @library_name (#eq? @library_name "expressjwt")
#             )
#         )
#     ) @require_call
# ) @import_statement
# (import_statement
#     (import_clause
#         (identifier) @import_identifier
#     )
#     (string
#         (string_fragment) @library_name (#eq? @library_name "expressjwt")
#     ) @string
# ) @import_statement
# (import_statement
#     (import_clause
#         (namespace_import
#             (identifier) @import_identifier
#         )
#     )
#     (string
#         (string_fragment) @library_name (#eq? @library_name "expressjwt")
#     ) @string
# ) @import_statement
# (call_expression
#     (identifier) @calling_identifier (#eq? @calling_identifier @import_identifier)
#     (arguments
#         (object
#             (pair
#                 (property_identifier) @property_identifier (#eq? @property_identifier "secret")
#                 (string
#                     (string_fragment) @secret_value
#                 ) 
#             ) @secret_pair
#         )
#     )
# ) @calling_expressjwt
# """

# captures, matches = query_tree(tree, detect_hardcoded_secret_query)
# print("=====")
# for capture in captures:
#     print(capture)

# print("=====")
# for match in matches:
#     print(match)

# src_code_lines = src_code.split("\n")

# # print the src code highlighted with the matches
# for match in matches:
#     match_object = match[1]
#     if "secret_pair" not in match_object:
#         continue
#     # import_statement_node = match_object["import_statement"]
#     secret_pair_node = match_object["secret_pair"]
#     start_line = secret_pair_node.start_point[0]
#     start_col = secret_pair_node.start_point[1]
#     end_line = secret_pair_node.end_point[0]
#     end_col = secret_pair_node.end_point[1]
#     print("=====")
#     print("HARD CODED SECRET DETECTED")
#     print("Details:")
#     # print(f"Import statement of expressjwt library detected at line {import_statement_node.start_point[0] + 1}")
#     # print(f"{src_code_lines[import_statement_node.start_point[0]]}")
#     print(f"Passing secret value to expressjwt library at line {start_line + 1}")
#     print(f"{src_code_lines[start_line][start_col:end_col]}")
    
        