from flask import Flask, request, jsonify
import time
import subprocess
from . import database

app = Flask(__name__)

@app.route('/')
def index():
    # Get request method
    request_method = request.method
    headers = dict(request.headers)
    parameters = request.args.to_dict()
    response = {
        'server-hostname' : get_hostname(),
        'timestamp': int(time.time())
    }
    
    return jsonify(response)

@app.route('/api', methods=['GET'])
def api():
    action = request.args.get('action')
    query = request.args.get('query')

    if action == 'create_table':
        status, result = database.create_table(query)
    elif action == 'insert_record':
        status, result = database.insert_record(query)
    elif action == 'select_records':
        status, result = database.select_records(query)
    else:
        status = 400
        result == "Query was denied"

    response = {
        'status_code' : status,
        'message': result
    }
    return jsonify(response)


def get_hostname() -> str:
    hostname = subprocess.check_output('hostname', shell=True)
    return hostname

if __name__ == '__main__':
    app.run(port=8080)
