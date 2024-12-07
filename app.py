import os
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder='./dist', static_url_path='')
CORS(app)

# Change this to False after finished coding
DEBUG = True

# This render the index.html from React
@app.route("/")
def index():
    return send_from_directory(os.path.join(app.static_folder), 'index.html')

@app.route('/api', methods=['POST'])
def api():
    response = {
        'status': 200,
        'message': 'Success',
        'data': None,
    }
    try:
        # Read the data from the interface
        data = request.get_json()['fact']

        # For Debugging
        print(data)

        # TODO
        '''
        Do the processing here
        after finished processing
        save the data into structure like this
        data = {'data': string}
        where string is the value that will be put in the output box.
        '''
    except e:
        print('Error:\n', e)
        response['status'] = 500
        response['message'] = 'There is something wrong in the server'

    return jsonify({'status': 200, 'message': 'Success', 'data': data})


if __name__ == '__main__':
    app.run(debug=DEBUG, port=3000)