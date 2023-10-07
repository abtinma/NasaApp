from flask import Flask, jsonify

# Create a Flask web application instance
app = Flask(__name__)

# Define a route that returns a JSON response
@app.route('/api/data', methods=['GET'])
def get_json_data():
    data = {
        'message': 'Hello, World!',
        'status': 'success'
    }
    return jsonify(data)

# Run the Flask app if this script is executed
if __name__ == '__main__':
    app.run(debug=True)