export interface Project {
    project_id: string;
    project_name: string;
    project_photo: string;
    description: string;
    brief_description: string;
    summary: string;
    objective: string;
    skills_needed: string[];
    collaborators_num: number;
    userId: string;
}

export interface User {
    name: string;
    user_id: string;
    username: string;
    email: string;
    user_skill: string[];
    user_description: string;
    photoURL: string;
    projects: Project[];
}