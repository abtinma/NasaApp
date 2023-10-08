from faker import Faker
import random
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def extract_important_words(text, n=5):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform([text])
    feature_array = np.array(vectorizer.get_feature_names_out())
    tfidf_sorting = np.argsort(X.toarray()).flatten()[::-1]
    
    # Get top n keywords
    top_n = feature_array[tfidf_sorting][:n]
    return top_n.tolist()


fake = Faker()

science_skills = ['Biology', 'Physics', 'Chemistry', 'Computer Science', 'Astronomy', 'Mathematics']


def generate_fake_user(project_ids):
    user_id = fake.uuid4()
    assigned_project_ids = random.sample(project_ids, min(len(project_ids), random.randint(0, 4)))
    return {
        "name": fake.name(),
        "user_id": user_id,
        "username": fake.user_name(),
        "email": fake.email(),
        "user_skill": random.sample(science_skills, random.randint(1, 4)),
        "user_description": fake.text(max_nb_chars=200),
        "photoURL": fake.image_url(),
        "project_ids": assigned_project_ids,
    }

def generate_fake_project():
    project_id = fake.uuid4()
    description = fake.text(max_nb_chars=1000)
    extracted_keywords = extract_important_words(description)
    return {
        "project_id": project_id,
        "project_name": fake.word().capitalize() + " " + fake.company_suffix(),
        "project_photo": fake.image_url(),
        "description": description,
        "brief_description": fake.text(max_nb_chars=100),
        "summary": fake.text(max_nb_chars=2000),
        "objective": fake.text(max_nb_chars=3000),
        "skills_needed": random.sample(science_skills, random.randint(2, 5)),
        "collaborators_num": random.randint(1, 10),
        "userId": None,  # Will be filled in later
        "extracted_keywords": extracted_keywords,  # Newly added field
    }

def generate_mock_data(n_users=100, n_projects=200):
    project_ids = []

    # Generate projects first to populate project_ids
    projects = [generate_fake_project() for _ in range(n_projects)]
    project_ids = [project['project_id'] for project in projects]

    # Generate users
    users = [generate_fake_user(project_ids) for _ in range(n_users)]

    # Assign userIds to projects
    user_ids = [user['user_id'] for user in users]
    for project in projects:
        project['userId'] = random.choice(user_ids)

    return users, projects

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Generate mock data
users, projects = generate_mock_data()

# Save to JSON
save_to_json(users, "mock_users.json")
save_to_json(projects, "mock_projects.json")
