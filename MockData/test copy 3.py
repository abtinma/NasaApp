from faker import Faker
import random
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import openai
import ast
import re

def sanitize_json_string(json_str):
    return re.sub(r'[\x00-\x1F\x7F]', '', json_str)

def generate_single_attribute(attribute_name, domain, objective, skills_needed):
    openai.api_key = key
    print("Generating", attribute_name, "...")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in science project descriptions."},
            {"role": "user", "content": f"Generate a {attribute_name} for a {domain} project aimed at {objective}. The project will require skills in {', '.join(skills_needed)}."}
        ],
        temperature=0.7,
        max_tokens=200,  # Adjust based on how long you expect each field to be
    )
    return response['choices'][0]['message']['content']

def generate_project_data(domain, objective, skills_needed):
    project_data = {}
    for attribute in ["project_name", "brief_description", "summary", "description", "objective"]:
        project_data[attribute] = generate_single_attribute(attribute, domain, objective, skills_needed)
        print("Generated", attribute, ":", len(project_data[attribute]))
    return project_data


def process_text(text):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform([text])
    feature_array = np.array(vectorizer.get_feature_names_out())
    return feature_array.tolist()

key = "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"

def extract_important_words(text):
    print("Extracting important words...", len(text))
    processed_text = process_text(text)
    processed_text_str = ", ".join(processed_text)
    print("Processed text:", len(processed_text_str))

    openai.api_key = key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who is an expert in science."},
            {"role": "user", "content": f"Identify and extract essential skills, technologies, and topics from the following project description. Prioritize terms that directly relate to the skills and technologies needed for the project: \n\n{processed_text}\n\nProvide these as a list of prioritized keywords. Format it as single JSON array like: " + '["term1", "term2"]' + ". Keep terms as 1 word. This array should contain a maximum of 10 terms, ordered by significance. Do not include the beginning such as 'summary:' or 'description:'. Make brief description 1 or 2 sentences"},
        ],
        
        temperature=0,
        max_tokens=256,
    )
    string = response['choices'][0]['message']['content']
    return ast.literal_eval(string)


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


projects = [
    {'project_name': 'Advanced Computational Models for Climate Prediction', 'brief_objective': 'Climate Prediction'},
    {'project_name': 'Sustainable Energy Solutions for the Next Generation', 'brief_objective': 'Next Generation'},
    {'project_name': 'Machine Learning Algorithms for Predictive Healthcare', 'brief_objective': 'Predictive Healthcare'},
    {'project_name': 'The Social Media Impact on Mental Health', 'brief_objective': 'Mental Health'},
    {'project_name': 'Cutting-Edge Methods for Targeted Drug Delivery', 'brief_objective': 'Drug Delivery'},
    {'project_name': 'Human Microbiome Analysis for Disease Prevention', 'brief_objective': 'Disease Prevention'},
    {'project_name': 'Long-Term Effects of Space Travel on Human Physiology', 'brief_objective': 'Human Physiology'},
    {'project_name': 'Pioneering Gene Therapies for Rare Genetic Disorders', 'brief_objective': 'Genetic Disorders'},
    {'project_name': 'Impact of Climate Change on Marine Ecosystems', 'brief_objective': 'Marine Ecosystems'},
    {'project_name': 'Alternative Materials for Sustainable Construction', 'brief_objective': 'Sustainable Construction'},
    {'project_name': 'Advanced Weather Forecasting Through Computational Modeling', 'brief_objective': 'Computational Modeling'},
    {'project_name': 'Mapping Neural Pathways to Decode Consciousness', 'brief_objective': 'Decode Consciousness'},
    {'project_name': 'Next-Gen Techniques for Water Purification', 'brief_objective': 'Water Purification'},
    {'project_name': 'Effects of Environmental Pollutants on Wildlife', 'brief_objective': 'on Wildlife'},
    {'project_name': 'Renewable Materials for Future Electronics', 'brief_objective': 'Future Electronics'},
    {'project_name': 'Investigating Epigenetic Factors in Cancer Progression', 'brief_objective': 'Cancer Progression'},
    {'project_name': 'Non-Invasive Glucose Monitoring Solutions', 'brief_objective': 'Monitoring Solutions'},
    {'project_name': 'Researching Nuclear Fusion as the Ultimate Energy Source', 'brief_objective': 'Energy Source'},
    {'project_name': 'Soil Health Analysis for Sustainable Agriculture', 'brief_objective': 'Sustainable Agriculture'},
    {'project_name': 'Studying the Unseen Forces Shaping the Universe', 'brief_objective': 'the Universe'},
    {'project_name': 'Automating Financial Risk Assessment', 'brief_objective': 'Risk Assessment'},
    {'project_name': 'Optimizing Supply Chain Logistics Through AI', 'brief_objective': 'Through AI'},
    {'project_name': 'Deep Learning for Natural Language Understanding', 'brief_objective': 'Language Understanding'},
    {'project_name': 'Investigating Quantum Computing Applications', 'brief_objective': 'Computing Applications'},
    {'project_name': 'Cybersecurity Measures for IoT Devices', 'brief_objective': 'IoT Devices'},
    {'project_name': 'Augmented Reality in Education', 'brief_objective': 'in Education'},
    {'project_name': 'Blockchain for Transparent Governance', 'brief_objective': 'Transparent Governance'},
    {'project_name': 'Evolutionary Algorithms in Game Theory', 'brief_objective': 'Game Theory'},
    {'project_name': 'Real-Time Analytics for Emergency Response', 'brief_objective': 'Emergency Response'},
    {'project_name': 'Predictive Maintenance for Industrial Equipment', 'brief_objective': 'Industrial Equipment'},
    {'project_name': 'Smart Grid Systems for Efficient Energy Use', 'brief_objective': 'Energy Use'},
    {'project_name': 'Human-Robot Interaction in Healthcare', 'brief_objective': 'in Healthcare'},
    {'project_name': 'AI in Autonomous Vehicle Navigation', 'brief_objective': 'Vehicle Navigation'},
    {'project_name': 'Fighting Fake News with Machine Learning', 'brief_objective': 'Machine Learning'},
    {'project_name': 'Edge Computing in Mobile Networks', 'brief_objective': 'Mobile Networks'},
    {'project_name': 'Voice Recognition Systems for Accessibility', 'brief_objective': 'for Accessibility'},
    {'project_name': 'Smart Agriculture Techniques', 'brief_objective': 'Agriculture Techniques'},
    {'project_name': 'Biometric Security Solutions', 'brief_objective': 'Security Solutions'},
    {'project_name': 'AR/VR for Surgical Training', 'brief_objective': 'Surgical Training'},
    {'project_name': 'Graph Theory in Social Network Analysis', 'brief_objective': 'Network Analysis'},
    {'project_name': 'Remote Sensing for Environmental Monitoring', 'brief_objective': 'Environmental Monitoring'},
    {'project_name': 'Ethical AI and Algorithmic Bias', 'brief_objective': 'Algorithmic Bias'},
    {'project_name': '3D Printing in Healthcare', 'brief_objective': 'in Healthcare'},
    {'project_name': 'Optical Communication Networks', 'brief_objective': 'Communication Networks'},
    {'project_name': 'Signal Processing for Biomedical Applications', 'brief_objective': 'Biomedical Applications'},
    {'project_name': 'Decentralized Finance (DeFi) Innovations', 'brief_objective': 'DeFi Innovations'},
    {'project_name': 'Bioinformatics for Personalized Medicine', 'brief_objective': 'Personalized Medicine'},
    {'project_name': 'Low-Code/No-Code Development Platforms', 'brief_objective': 'Development Platforms'},
    {'project_name': 'Big Data in Precision Medicine', 'brief_objective': 'Precision Medicine'},
    {'project_name': 'Human-Centric AI Design', 'brief_objective': 'AI Design'}
]


def generate_fake_project():
    project_id = fake.uuid4()
    domain = random.choice(science_skills)
    
    # Randomly select an objective from the list of possible objectives
    objective = random.choice(possible_objectives)
    
    skills_needed = random.sample(science_skills, random.randint(2, 5))

    project_data = generate_project_data(domain, objective, skills_needed)
    extracted_keywords = extract_important_words(project_data["description"])

    project_data.update({
        "project_id": project_id,
        "project_photo": fake.image_url(),
        "skills_needed": skills_needed,
        "collaborators_num": random.randint(1, 10),
        "userId": None,  # Will be filled in later
        "extracted_keywords": extracted_keywords,  # Newly added field
    })

    return project_data

def generate_mock_data(n_users=1, n_projects=2):
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
