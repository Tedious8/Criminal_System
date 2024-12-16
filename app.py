import os
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from legal_prediction import qa_system_with_crime

app = Flask(__name__, static_folder='./dist', static_url_path='')
CORS(app)

# Change this to False after finished coding
DEBUG = False

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

        # Retrieve the answers from the model
        answers = qa_system_with_crime(data)

        # Do the formatting/transformation to make the input easy to parse on frontend
        results = []
        for answer in answers:
            crime_display = answer['crime'] if answer['crime'] else "未知罪名"
            results.append(f"條文：{answer['article']}，罪名：{crime_display}，相似度：{answer['score']:.2f}")

        # Assign the data to the dictionary
        response['data'] = "\n".join(results)
    except FileNotFoundError as error:
        response['status'] = 500
        response['message'] = str(error)
    except Exception as error:
        response['status'] = 500
        response['message'] = str(error)

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=DEBUG, port=3000)