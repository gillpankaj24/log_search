from flask import Flask, jsonify, request

from search_logs import search_logs_data

app = Flask(__name__)


@app.route('/search/logs', methods=['GET'])
def search():
    data = request.values.to_dict()
    success, params = search_logs_data.validate_request_params(data)
    if not success:
        return jsonify(params), 400
    result = search_logs_data.search_logs(params)
    return jsonify(result)


if __name__ == '__main__':
    app.run()

