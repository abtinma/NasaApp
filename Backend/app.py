from flask import Flask, jsonify, request, Response, redirect, url_for, make_response
from dotenv import load_dotenv
import os
import psycopg2

app = Flask(__name__)
# Specify the path to your .env file (relative to your Flask app)
dotenv_path = 'Backend/.env'  
load_dotenv(dotenv_path)
app.secret_key = os.getenv("SECRET_KEY")


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

@app.route('/signin', methods=['POST'])
def get_user_details():
    try:
        user_id = request.headers.get('user_id')

        # Use the database connection from the request context
        cursor = request.db_connection.cursor()

        # check if user with user_id exists in database
        user_select_query = "SELECT username FROM users WHERE user_id = %s"

        cursor.execute(user_select_query, (user_id,))

        username = cursor.fetchone()

        if username:
            return redirect(f'home/{username}?user_id={user_id}')
        else:
            return jsonify({'error': 'user not found'}), 404
            
    except Exception as e:
        # Handle any exceptions and return an error response
        response = jsonify({'error': str(e)})
        response.status_code = 500
        return response

@app.route('/home/<username>')
def home_page(username):
    user_id = request.args.get('user_id')

    # Use the database connection from the request context
    cursor = request.db_connection.cursor()

    # Get a list of all projects
    all_project_select = "SELECT * FROM projects;"
    
    # Execute the query to fetch all projects
    cursor.execute(all_project_select)
    
    # Fetch all results from the cursor for all projects
    all_projects = cursor.fetchall()

    project_list = []
    for project in all_projects:
        project_dict = {
            "projects_id": project[0],
            "project_name": project[1],
            "description": project[2],
            "skills_needed": project[3],
            "collaborators_num": project[4],
            "completed": project[5], 
            "users_id": project[6],
            "brief_description": project[7],
            "summary": project[8], 
            "photourl": project[9]
        }
        project_list.append(project_dict)

    # Get info about the current user
    user_select_query = "SELECT * FROM users WHERE user_id = %s"
    cursor.execute(user_select_query, (user_id,))
    user_info = cursor.fetchone()

    # Create a JSON response
    response_data = {
        "all_projects": project_list, 
        "user_info": {
            "user_id": user_info[0],
            "name": user_info[1], 
            "email": user_info[2],
            "username": user_info[3],
            "user_skill": user_info[4],
            "user_description": user_info[5],
            "photourl": user_info[6]
        }
    }

    print(user_info)
    print(type(user_info))

    # Create a response object with JSON data and set the status code
    response = make_response(jsonify(response_data))
    response.status_code = 200

    return response


@app.route('/signup', methods=['POST'])
def sign_up():
    try:
        user_id = request.headers.get('user_id')
        name = request.headers.get('name')
        username = request.headers.get('username')
        email = request.headers.get('email')

        # Input Validation (Example: Checking if user_id and email are provided)
        if not user_id or not email:
            return jsonify({'error': 'User ID and email are required fields.'}), 400

        # Use the database connection from the request context
        cursor = request.db_connection.cursor()

        # Check if the user with the same user_id already exists
        user_exists_query = "SELECT 1 FROM users WHERE user_id = %s"
        cursor.execute(user_exists_query, (user_id,))
        if cursor.fetchone():
            return jsonify({'error': 'User with this user_id already exists.'}), 409

        # Use placeholders in the query to prevent SQL injection
        insert_query = """
            INSERT INTO users (user_id, name, username, email)
            VALUES (%s, %s, %s, %s);
        """

        # Pass the values as a tuple to cursor.execute
        cursor.execute(insert_query, (user_id, name, username, email))

        # Commit the transaction to save the changes to the database
        request.db_connection.commit()

        # Redirect to the user's home page
        return redirect(f'/home/{username}?user_id={user_id}')

    except Exception as e:
        # Handle any exceptions and return an error response
        response = jsonify({'error': str(e)})
        response.status_code = 500
        return response

@app.route('/user_projects/<user_id>', methods=['GET'])
def get_user_projects(user_id):
    try:
        # Use the database connection from the request context
        cursor = request.db_connection.cursor()

        select_project_query = """
        SELECT
            projects.project_name,
            projects.description,
            projects.skills_needed,
            projects.collaborators_num,
            projects.completed,
            Users.username  -- Selecting a column from the "Users" table
        FROM
            projects
        INNER JOIN
            Users
        ON
            projects.users_id = Users.user_id
        WHERE
            Users.user_id = %s;
        """
        # Execute the query to fetch the user's projects
        cursor.execute(select_project_query, (user_id,))
        
        # Fetch all results from the cursor for the user's projects
        user_projects = cursor.fetchall()

        # Create a JSON response
        response_data = {
            "user_id": user_id,
            "projects": [],
        }

        for project in user_projects:
            project_dict = {
                "project_name": project[0],
                "description": project[1],
                "skills_needed": project[2],
                "collaborators_num": project[3],
                "completed": project[4],
                "username": project[5],  # Username of the project owner
            }
            response_data["projects"].append(project_dict)

        # Create a response object with JSON data and set the status code
        response = make_response(jsonify(response_data))
        response.status_code = 200

        return response

    except Exception as e:
        # Handle any exceptions and return an error response
        response = jsonify({'error': str(e)})
        response.status_code = 500
        return response

# Run the Flask app if this script is executed
if __name__ == '__main__':
    app.run(debug=True)
