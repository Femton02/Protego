import os
import sys
protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)

from tree_sitter import Language

Language.build_library(
    # Store the library in the `build` directory
    protego_workspace_dir + "/src/core/t_sitter/build/my-languages.so",
    # Include one or more languages
    [
        protego_workspace_dir + "/src/core/t_sitter/languages/tree-sitter-javascript",
    ],
)
