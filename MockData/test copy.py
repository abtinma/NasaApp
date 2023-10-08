from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import random
import openai
import ast
# OpenAI API key
key = "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"
def ask_gpt3(prompt):
    openai.api_key = key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Identify and extract essential skills, technologies, and topics from the following project description. Prioritize terms that directly relate to the skills and technologies needed for the project: \n\n{prompt}\n\nProvide these as a list of prioritized keywords. Format it as single JSON array like: " + '["term1", "term2"]' + ". Keep terms as 1 word."},
        ],
        
        temperature=0,
        max_tokens=308,
    )
    return response['choices'][0]['message']['content']


# Function to extract important words using TF-IDF
def extract_important_words(text, n=10):
    print("Extracting important words...")

    openai.api_key = key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Identify and extract essential skills, technologies, and topics from the following project description. Prioritize terms that directly relate to the skills and technologies needed for the project: \n\n{text}\n\nProvide these as a list of prioritized keywords. Format it as single JSON array like: " + '["term1", "term2"]' + ". Keep terms as 1 word."},
        ],
        
        temperature=0,
        max_tokens=308,
    )
    string = response['choices'][0]['message']['content']
    return ast.literal_eval(string)

# Custom project description
project_description = "This is a space exploration project aimed at sending a rover to Mars. The objective is to collect soil samples and search for signs of ancient microbial life."

# Sample science skills
science_skills = ['Biology', 'Physics', 'Chemistry', 'Computer Science', 'Astronomy', 'Mathematics']

# Generate a single project with a custom description
project = {
    "project_id": "custom_project_id",
    "project_name": "Mars Rover Exploration",
    "project_photo": "https://example.com/project_photo.jpg",
    "description": project_description,
    "brief_description": "A mission to send a rover to Mars for scientific research.",
    "summary": "The project aims to explore Mars' surface with a state-of-the-art rover.",
    "objective": "Collect soil samples and search for signs of ancient microbial life.",
    "skills_needed": random.sample(science_skills, random.randint(2, 5)),
    "collaborators_num": random.randint(1, 10),
    "userId": "custom_user_id",
    "extracted_keywords": extract_important_words(project_description)
}

# Output to the console
print("Generated Project:")
print(project["extracted_keywords"])
