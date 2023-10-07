from flask import Flask, jsonify, request, Response
import psycopg2

app = Flask(__name__)

# Database connection setup function
def get_db_connection():
    return psycopg2.connect(
        host="dpg-ckgn6ci12bvs7381hhjg-a.oregon-postgres.render.com",
        port="5432",
        user="database_nasa_user",
        password="BWp2sy9HenSR7fq6K8ZGzJHh3ygoWQmS",
        database="database_nasa"
    )

# Create a database connection for each request
@app.before_request
def before_request():
    request.db_connection = get_db_connection()

# Close the database connection after each request
@app.teardown_request
def teardown_request(exception):
    if hasattr(request, 'db_connection'):
        request.db_connection.close()

@app.route('/user', methods=['GET'])
def get_all_users():
    try:
        user_id = request.headers.get('user_id')

        # Use the database connection from the request context
        cursor = request.db_connection.cursor()

        # Use placeholders in the query to prevent SQL injection
        select_query = "SELECT * FROM users WHERE user_id = %s;"
        cursor.execute(select_query, (user_id,))

        # Fetch all results from the cursor
        user_list = cursor.fetchall()

        # Create a JSON response
        response = jsonify(user_list)

        # Set the HTTP status code to 200 (OK)
        response.status_code = 200

        return response
    except Exception as e:
        # Handle any exceptions and return an error response
        response = jsonify({'error': str(e)})
        response.status_code = 500
        return response

@app.route('/signup', methods=['POST'])
def sign_up():
    try:
        user_id = request.headers.get('user_id')
        name = request.headers.get('name')
        username = request.headers.get('username')
        email = request.headers.get('email')

        print(user_id)
        print(name)
        print(username)
        print(email)

        # Use the database connection from the request context
        cursor = request.db_connection.cursor()

        # Use placeholders in the query to prevent SQL injection
        insert_query = """
            INSERT INTO users (user_id, name, username, email)
            VALUES (%s, %s, %s, %s);
        """

        # Pass the values as a tuple to cursor.execute
        cursor.execute(insert_query, (user_id, name, username, email))

        # Commit the transaction to save the changes to the database
        request.db_connection.commit()

        # Create a response with a success message
        response = Response('User registered successfully', status=200)
        return response
    except Exception as e:
        # Handle any exceptions and return an error response
        response = Response(str(e), status=500)
        return response

# Run the Flask app if this script is executed
if __name__ == '__main__':
    app.run(debug=True)
