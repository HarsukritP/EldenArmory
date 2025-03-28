from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Elden Ring Weapons API is running!"

@app.route('/debug', methods=['GET'])
def debug():
    debug_info = {
        "status": "online",
        "current_directory": os.getcwd(),
        "directory_contents": os.listdir(os.getcwd())
    }
    
    # Check if data directory exists relative to current working directory
    if os.path.exists('data'):
        debug_info["data_exists_in_cwd"] = True
        debug_info["data_contents"] = os.listdir('data')
    else:
        debug_info["data_exists_in_cwd"] = False
    
    # Try to find the data directory anywhere in the current tree
    for root, dirs, files in os.walk(os.getcwd()):
        if 'data' in dirs:
            data_path = os.path.join(root, 'data')
            debug_info["found_data_path"] = data_path
            debug_info["found_data_contents"] = os.listdir(data_path)
            break
    
    return jsonify(debug_info)

if __name__ == '__main__':
    app.run(debug=True)