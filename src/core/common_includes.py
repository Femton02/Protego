import os
import sys

protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(protego_workspace_dir)
sys.path.append(os.path.join(protego_workspace_dir, "src"))
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
sys.path.append(os.path.join(protego_workspace_dir, "src/core/rule_handler"))
sys.path.append(os.path.join(protego_workspace_dir, "src/core/t_sitter"))


from core.t_sitter.tree_sitter_utils import *
from core.rule_handler.rule import *
from rule_handler.pattern_parser import *
from core.rule_handler.rule_parser import *

# Code snippet to be used in each file that needs to run from

# import os
# import sys
# protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
# if not protego_workspace_dir:
#     print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
#     sys.exit(1)
# sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
# from common_includes import *