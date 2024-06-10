import os
import sys
protego_workspace_dir = os.environ.get("PROTEGO_WORKSPACE_DIR")
if not protego_workspace_dir:
    print("Please set the environment variable PROTEGO_WORKSPACE_DIR to the path of the Protego workspace directory.")
    sys.exit(1)
sys.path.append(os.path.join(protego_workspace_dir, "src/core"))
from common_includes import *

#____________________________________________________________________________________#
from core.main import scan_project

import os
import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return 'Protego API'

@app.route('/process', methods=['POST'])
def process_files():
    if 'rule.yaml' not in request.files or 'code.js' not in request.files:
        return jsonify({'error': 'Missing files'}), 400

    rule_file = request.files['rule.yaml']
    code_file = request.files['code.js']

    # Save the uploaded files
    rule_file_path = os.path.join('/tmp', 'rule.yaml')
    code_file_path = os.path.join('/tmp', 'code.js')
    rule_file.save(rule_file_path)
    code_file.save(code_file_path)

    
    try:
        result = scan_project(code_file_path, rule_file_path)
    except Exception as e:
        return jsonify({'error': 'Error processing files', 'details': str(e)}), 500

    # remove the files after processing
    os.remove(rule_file_path)
    os.remove(code_file_path)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
