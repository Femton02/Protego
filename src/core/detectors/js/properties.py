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


class HelperDataTypes(BaseModel):
    node: ProtegoNode
    name: str
    properties: dict = {}
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

    def _detect_properties(self):
        """Detects properties in JavaScript code."""
        self._add_properties()
        self._link_properties()
        self._scope_proprties()

    def _add_properties(self):
        _, matches = query_tree(self.tree, root_properties_query)
        for x in matches:
            match = x[1]
            root_property_node = match["param_property"]
            root_property_pnode = self.protego_tree.get_node_by_id(root_property_node.id)

            self.helper_data_types[root_property_pnode.id] = HelperDataTypes(node=root_property_pnode, name=root_property_pnode.text)
        
        _, matches = query_tree(self.tree, nested_properties_query)
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
    """
    detector = PropertiesDetector(js_code)
    detector.detect()
    results = detector.get_results()
    detector.print_scopes()