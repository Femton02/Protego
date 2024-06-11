import os
import sys
protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
from common_includes import *

#____________________________________________________________________________________#

from core.detectors.js.properties import detect_objects
from core.detectors.classification.datatypes.datatype_classification import classify_datatype
from protego_node import ProtegoTree

def detect_datatypes(tree: ProtegoTree):
    # Detect objects
    objects = detect_objects(tree)
    res = {}
    for datatype_uuid, datatype in objects.items():
        r1 = classify_datatype(datatype["object"])
        if not r1:
            continue
        for key, value in r1.items():
            for ttt in value:
                ttt["filepath"] = tree.full_file_path
                ttt["line"] = datatype["line"]
                ttt["object"] = datatype["object"]

    
        for key, value in r1.items():
            if key not in res:
                res[key] = value
            else:
                res[key] = res[key] + value

    return res

if __name__ == "__main__":
    src_code = """
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
    tree = parse_js_code(src_code)
    protego_tree = ProtegoTree(tree, "ahah", "adsfs")
    res = detect_datatypes(protego_tree)

    print(json.dumps(res, indent=4))


