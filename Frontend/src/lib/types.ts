interface Project {
    project_id: string;
    project_name: string;
    description: string;
    skills_needed: string[];
    collaborators_num: number;
    userId: string;
}

interface User {
    name: string;
    user_id: string;
    username: string;
    email: string;
    user_skill: string[];
    user_description: string;
    photoURL: string;
    projects: Project[];
}