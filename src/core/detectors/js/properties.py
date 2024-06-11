import os
import sys
protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
from common_includes import *

#____________________________________________________________________________________#
from detectors.detector_interface import DetectorInterface
from core.protego_node import ProtegoNode, ProtegoTree
from pydantic import BaseModel
import json
import uuid



nested_properties_query = "\
    (member_expression  \
        property: (property_identifier) @param_property \
    )@param_object \
    "

root_properties_query = "\
	(member_expression \
        object: [(identifier) (this)] @param_property    \
	)   \
    "

objects_query = "\
    (object \
	    (pair) @param_pair  \
    ) @param_object \
    "

nested_objects_query = "\
    (object \
	    (pair   \
		    value: (object) @param_child_object \
	    ) @param_pair   \
    ) @param_object \
    "

class HelperDataTypes(BaseModel):
    node: ProtegoNode
    name: str
    properties: dict[str, "HelperDataTypes"] = {}
    uuid: str = ""

    model_config = {
        "arbitrary_types_allowed": True
    }

class PropertiesDetector(DetectorInterface):
    """Detector for properties in JavaScript code."""

    def __init__(self, js_code: str):
        self.js_code = js_code
        self.tree = parse_js_code(js_code)
        self.protego_tree = ProtegoTree(self.tree)
        self.results = []
        self.helper_data_types: dict[int, HelperDataTypes] = dict()
        self.data_types: dict[int, HelperDataTypes] = dict()
        self.scopes: dict[int, dict[str, list[HelperDataTypes]]] = dict()

    def detect(self):
        """Detects properties in JavaScript code."""
        self._detect_properties()
        self._add_objects()

    def get_results(self):
        return self.scopes

    def print_scopes(self):
        for scope_id, scope in self.scopes.items():
            print(f"Scope: {scope_id}")
            for data_type_name, data_types in scope["data_types"].items():
                print(f"Data Type: {data_type_name}\n")
                for data_type in data_types:
                    print(f"New node at line {data_type.node.start_point[0]}")
                    print("Properties:")
                    for property_name, property in data_type.properties.items():
                        print(f" {property_name}, ")
                
                print("\n=====================\n")
            print("\n\n----------------------\n\n")
    
    def prettify_results(self):
       # output should be json a dict with the following structure
       # {
       #    "user": {
         #        "name": {},
            #        "surname": {}
            #    }
            #}
        prettified_results = {}
        
        for data_type in self.data_types.values():
            data_type_uuid = uuid.uuid4().__str__()
            prettified_results[data_type_uuid] = {}
            prettified_results[data_type_uuid][data_type.name] = {}
            self._prettify_helper_data_types(data_type, prettified_results[data_type_uuid][data_type.name])

        print(len(prettified_results))
        return prettified_results
    
    def _prettify_helper_data_types(self, data_type, prettified_results):
        for property_name, property in data_type.properties.items():
            prettified_results[property_name] = {}
            self._prettify_helper_data_types(property, prettified_results[property_name])

    
    def print_data_types(self):
        for data_type in self.data_types.values():
            print(f"Line: {data_type.node.start_point[0]}")
            print(f"Name: {data_type.name}")
            for property_name, property in data_type.properties.items():
                self._print_helper_data_types(property)
            print("\n=====================\n")

    def _print_helper_data_types(self, property, level=1):
        print(f"{' ' * level}Name: {property.name}")
        for property_name, property in property.properties.items():
            self._print_helper_data_types(property, level + 1)

    def _detect_properties(self):
        """Detects properties in JavaScript code."""
        self._add_properties()
        self._link_properties()
        self._scope_proprties()

    def _add_properties(self):
        _, matches = query_tree(self.tree.root_node, root_properties_query)
        for x in matches:
            match = x[1]
            root_property_node = match["param_property"]
            root_property_pnode = self.protego_tree.get_node_by_id(root_property_node.id)

            self.helper_data_types[root_property_pnode.id] = HelperDataTypes(node=root_property_pnode, name=root_property_pnode.text)
        
        _, matches = query_tree(self.tree.root_node, nested_properties_query)
        for x in matches:
            match = x[1]
            
            object_node = match["param_object"]
            property_node = match["param_property"]
            object_pnode = self.protego_tree.get_node_by_id(object_node.id)
            property_pnode = self.protego_tree.get_node_by_id(property_node.id)

            self.helper_data_types[object_pnode.id] = HelperDataTypes(node=property_pnode, name=property_pnode.text)
    
    def _link_properties(self):

        for helper_data_type in self.helper_data_types.values():
            node = helper_data_type.node

            # root nodes
            if node.type == "identifier" or node.type == "this":
                self.data_types[node.id] = helper_data_type

            
            parent = node.parent
            # user.name (parent of name is member_expression)
            if parent.type == "member_expression":
                # link to root node 

                # user.name (user is the object node)
                # user.name.surname (user.name is the object node)
                object_node = parent.tree_sitter_node.child_by_field_name("object")
                if object_node.id == node.id:
                    continue

                if object_node.type == "identifier" or object_node.type == "this":
                    # helper_data_type.name is the property name which was "name" in the above example
                    self.helper_data_types[object_node.id].properties[helper_data_type.name] = helper_data_type

                if object_node.type == "member_expression":
                    self.helper_data_types[object_node.id].properties[helper_data_type.name] = helper_data_type
                
            
            # link to root document
            self.data_types[node.id] = helper_data_type

    def _scope_proprties(self):

        scope_terminating_node_types = ["program", "function", "arrow_function", "method_definition", "statement_block"]


        for data_type in self.data_types.values():

            scope_node = data_type.node.parent
            if not scope_node:
                scope_node = data_type.node

            while (scope_node):
                parent_type = scope_node.type
                if parent_type in scope_terminating_node_types:
                    break

                scope_node = scope_node.parent
            
            if not scope_node:
                continue
            
            # Append same scope same datatype name
            if scope_node.id not in self.scopes:
                self.scopes[scope_node.id] = { "data_types": {} }
            if data_type.name not in self.scopes[scope_node.id]["data_types"]:
                self.scopes[scope_node.id]["data_types"][data_type.name] = []
            self.scopes[scope_node.id]["data_types"][data_type.name].append(data_type)

        self._unify_uuid()
    
    def _unify_uuid(self):
        """Unify the UUID of the same data types in different scopes."""
        for scope in self.scopes.values():
            uuid_val = str(uuid.uuid4())
            for data_types in scope["data_types"].values():
                for data_type in data_types:
                    data_type.uuid = uuid_val
    
    def _add_objects(self):

        _, matches = query_tree(self.tree.root_node, objects_query)
        for x in matches:
            match = x[1]
    
            object_node = match["param_object"]
            object_pnode = self.protego_tree.get_node_by_id(object_node.id)
            
            pair_node = self.protego_tree.get_node_by_id(match["param_pair"].id)
            # { name: "test"} (name is the property node)
            property_node = pair_node.tree_sitter_node.child_by_field_name("key")
            if not property_node:
                continue
            property_pnode = self.protego_tree.get_node_by_id(property_node.id)

            # create a common data type for the object
            if object_node.id not in self.data_types:
                self.data_types[object_node.id] = HelperDataTypes(node=object_pnode, name="", uuid=str(uuid.uuid4()))
            
            # add property to the object
            self.data_types[object_node.id].properties[property_pnode.text] = \
                HelperDataTypes(node=property_pnode, name=property_pnode.text)


        keys_to_delete = []
        
        # link nested objects to their properties
        _, matches = query_tree(self.tree.root_node, nested_objects_query)
        for x in matches:
            match: dict[str, Node] = x[1]
            
            # {
            #    key: 'value',
            #    key2: 'value2'
            #    key3: { nested_ket: 'nested_value' } 
            #};

            # [{ nested_ket: 'nested_value' }] this is the param_child_object
            property_value_node = match["param_child_object"]
            # this the root object node
            object_node = match["param_object"]

            property_value_pnode = self.protego_tree.get_node_by_id(property_value_node.id)
            object_pnode = self.protego_tree.get_node_by_id(object_node.id)

            # [key3: { nested_ket: 'nested_value' }]  this the param_pair
            # property_node is the key3
            property_node = match["param_pair"].child_by_field_name("key")
            if not property_node:
                continue
            property_pnode = self.protego_tree.get_node_by_id(property_node.id)

            # sometimes objects only have function names in that case we should ignore them
            if property_value_pnode.id not in self.data_types:
                continue
            if object_pnode.id not in self.data_types:
                continue

            # link property
            self.data_types[object_pnode.id].properties[property_pnode.text] = self.data_types[property_value_pnode.id]

            # update property name
            self.data_types[object_pnode.id].properties[property_pnode.text].name = property_pnode.text

            # mark root node key for deletion
            keys_to_delete.append(property_value_pnode.id)
        
        
        for key in keys_to_delete:
            del self.data_types[key]

        # add root object names
        for key, data_type in self.data_types.items():
            node = data_type.node
            parent = node.parent

            if parent.type == "assignment_expression":
                left_node = parent.tree_sitter_node.child_by_field_name("left")
                if left_node.type == "member_expression":
                    property_node = left_node.child_by_field_name("property")
                    data_type.name = property_node.text.decode()
                    continue

                if left_node.type == "identifier":
                    data_type.name = left_node.text.decode()
                    continue

                if left_node.type == "subscript_expression":
                    index_node = left_node.child_by_field_name("index")

                    if index_node and index_node.type == "member_expression":
                        property_node = index_node.child_by_field_name("property")
                        
                        if property_node and property_node.type == "property_identifier":
                            data_type.name = property_node.text.decode()
                            continue
                
            
            if parent.type == "variable_declarator":
                identifier_node = parent.tree_sitter_node.child_by_field_name("name")
                data_type.name = identifier_node.text.decode()
                continue

            if parent.type == "arguments":
                grandparent = parent.parent

                if grandparent.type == "subscript_expression":
                    index_node = grandparent.tree_sitter_node.child_by_field_name("index")

                    if not index_node:
                        continue

                    if index_node.type == "string" or index_node.type == "number":
                        data_type.name = index_node.text.decode()
                        continue
                
                if grandparent.type == "call_expression":
                    function_node = grandparent.tree_sitter_node.child_by_field_name("function")

                    if function_node.type == "identifier":
                        data_type.name = function_node.text.decode()
                        continue

                    if function_node.type == "member_expression":
                        property_node = function_node.child_by_field_name("property")
                        data_type.name = property_node.text.decode()
                        continue

            if parent.type == "return_statement":
                grandparent = parent.parent

                if grandparent.type == "statement_block":
                    grand_grandparent = grandparent.parent

                    if grand_grandparent.type == "function_declaration":
                        identifier_node = grand_grandparent.tree_sitter_node.child_by_field_name("name")

                        if identifier_node:
                            data_type.name = identifier_node.text.decode()
                            continue
                    
                    # fallback to assignment expression
                    assignment_expression_node = grand_grandparent.parent
                    if assignment_expression_node and self._object_assignment(assignment_expression_node, data_type):
                        continue
            
            if parent.type == "parenthesized_expression":
                grandparent = parent.parent

                if grandparent and grandparent.type == "arrow_function":
                    grand_grandparent = grandparent.parent

                    if not grand_grandparent:
                        continue

                    if grand_grandparent.type == "variable_declarator":
                        identifier_node = grand_grandparent.tree_sitter_node.child_by_field_name("name")
                        
                        if identifier_node and identifier_node.type == "identifier":
                            data_type.name = identifier_node.text.decode()
                            continue
                    
                    if grand_grandparent.type == "assignment_expression":
                        if self._object_assignment(grand_grandparent, data_type):
                            continue        

    def _object_assignment(self, node: ProtegoNode, datatype: HelperDataTypes) -> bool:
        left_node = node.tree_sitter_node.child_by_field_name("left")
        if not left_node:
            return True
        
        if left_node.type == "member_expression":
            property_node = left_node.child_by_field_name("property")
            if property_node and property_node.type == "property_identifier":
                datatype.name = property_node.text.decode()
                return True

        if left_node.type == "subscript_expression":
            index_node = left_node.child_by_field_name("index")

            if not index_node:
                return True
            
            if index_node.type == "string":
                content = index_node.text.decode()
                content = re.sub(r'["\'`]', '', content)
                datatype.name = content
                return True
            
            if index_node.type == "number":
                datatype.name = index_node.text.decode()
                return True
        
        return False
        
                    


def detect_objects(js_code: str):
    detector = PropertiesDetector(js_code)
    detector.detect()
    return detector.prettify_results()


if __name__ == "__main__":
    js_code = """
    user.Save();
    user.name;
    user.name = "test";
    {
        fuck.me
    }
    user.name.surname;
    this.save();

    let test = {
        address: {
            city: "new york",
            street: {
                letters: "11-th avenue",
                numer: 12,
            },
        },
    };
    """
    res = detect_objects(js_code)
    print(json.dumps(res, indent=4))