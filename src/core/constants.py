import os
import sys
protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)

js_supported_extensions = [".js"]
default_rules_path = os.path.join(protego_workspace_dir, "rules")
if not os.path.exists(default_rules_path):
    raise Exception(f"Default rules path: {default_rules_path} does not exist.")