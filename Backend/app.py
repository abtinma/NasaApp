from flask import Flask, jsonify
import psycopg2

# Create a Flask web application instance
app = Flask(__name__)

connection = psycopg2.connect(
    host="dpg-ckgn6ci12bvs7381hhjg-a.oregon-postgres.render.com",
    port="5432",
    user="database_nasa_user",
    password="BWp2sy9HenSR7fq6K8ZGzJHh3ygoWQmS",
    database="database_nasa"
)

# Define a route that returns a JSON response
@app.route('/', methods=['GET'])
def get_json_data():
    data = {
        'message': 'Hello, World!',
        'status': 'success'
    }
    return jsonify(data)

@app.route('/user', methods=['GET'])
def get_all_users():

    # Create a connection 
    cursor = connection.cursor()
    select_query = "SELECT * FROM users;"
    cursor.execute(select_query)
    
    # Fetch all results from the cursor
    user_list = cursor.fetchall()

    response = jsonify(user_list)

    # You can also set the HTTP status code (optional)
    response.status_code = 200

    return response

# Run the Flask app if this script is executed
if __name__ == '__main__':
    app.run(debug=True)
