
# CAREER_INFO = {

#     "AI": {
#         "title": "Artificial Intelligence Engineer",
#         "description": "Build intelligent systems using machine learning and AI.",
#         "skills": [
#             "Python",
#             "Machine Learning",
#             "Deep Learning",
#             "Mathematics",
#             "Neural Networks"
#         ],
#         "tools": ["Python", "TensorFlow", "PyTorch", "Scikit-learn"],
#         "roadmap": [
#             "Learn Python Programming",
#             "Master Mathematics and Statistics",
#             "Learn Machine Learning",
#             "Study Deep Learning",
#             "Build AI Projects"
#         ]
#     },

#     "Data Science": {
#         "title": "Data Scientist",
#         "description": "Analyze data and develop predictive models.",
#         "skills": [
#             "Python",
#             "Statistics",
#             "SQL",
#             "Data Visualization",
#             "Machine Learning"
#         ],
#         "tools": ["Pandas", "NumPy", "Power BI", "Scikit-learn"],
#         "roadmap": [
#             "Learn Python and SQL",
#             "Study Statistics",
#             "Master Data Analysis",
#             "Learn Machine Learning",
#             "Build Data Science Projects"
#         ]
#     },

#     "HR": {
#         "title": "Human Resources Professional",
#         "description": "Manage recruitment, employee relations and talent development.",
#         "skills": [
#             "Communication",
#             "Leadership",
#             "Problem Solving",
#             "Team Management",
#             "Recruitment"
#         ],
#         "tools": ["Excel", "HRMS", "Communication Tools"],
#         "roadmap": [
#             "Learn HR Fundamentals",
#             "Develop Communication Skills",
#             "Understand Recruitment",
#             "Learn Employee Management",
#             "Practice HR Case Studies"
#         ]
#     },

#     "Management": {
#         "title": "Business Management Professional",
#         "description": "Plan business operations and manage teams and projects.",
#         "skills": [
#             "Leadership",
#             "Communication",
#             "Business Strategy",
#             "Decision Making",
#             "Project Management"
#         ],
#         "tools": ["Excel", "Power BI", "Project Management Tools"],
#         "roadmap": [
#             "Learn Management Fundamentals",
#             "Develop Leadership Skills",
#             "Study Business Strategy",
#             "Learn Project Management",
#             "Work on Business Case Studies"
#         ]
#     }
# }


# def get_career_info(career):
#     return CAREER_INFO.get(career, {
#         "title": career,
#         "description": "Explore this career path.",
#         "skills": [],
#         "tools": [],
#         "roadmap": []
#     })








CAREER_INFO = {

    "AI": {
        "title": "Artificial Intelligence Engineer",
        "description": "Build intelligent systems using Machine Learning and Deep Learning.",
        "skills": ["Python", "Machine Learning", "Deep Learning", "Mathematics", "Neural Networks"],
        "tools": ["Python", "TensorFlow", "PyTorch", "Scikit-learn"],
        "roadmap": [
            "Learn Python Programming",
            "Master Mathematics and Statistics",
            "Learn Machine Learning",
            "Study Deep Learning",
            "Build AI Projects"
        ]
    },

    "Data Science": {
        "title": "Data Scientist",
        "description": "Analyze data and develop predictive models.",
        "skills": ["Python", "Statistics", "SQL", "Data Visualization", "Machine Learning"],
        "tools": ["Pandas", "NumPy", "Power BI", "Scikit-learn"],
        "roadmap": [
            "Learn Python and SQL",
            "Study Statistics",
            "Master Data Analysis",
            "Learn Machine Learning",
            "Build Data Science Projects"
        ]
    },

    "HR": {
        "title": "Human Resources Professional",
        "description": "Manage recruitment, employee relations and talent development.",
        "skills": ["Communication", "Leadership", "Problem Solving", "Team Management", "Recruitment"],
        "tools": ["Excel", "HRMS", "Communication Tools"],
        "roadmap": [
            "Learn HR Fundamentals",
            "Develop Communication Skills",
            "Understand Recruitment",
            "Learn Employee Management",
            "Practice HR Case Studies"
        ]
    },

    "Management": {
        "title": "Business Management Professional",
        "description": "Plan business operations and manage teams and projects.",
        "skills": ["Leadership", "Communication", "Business Strategy", "Decision Making", "Project Management"],
        "tools": ["Excel", "Power BI", "Project Management Tools"],
        "roadmap": [
            "Learn Management Fundamentals",
            "Develop Leadership Skills",
            "Study Business Strategy",
            "Learn Project Management",
            "Work on Business Case Studies"
        ]
    }
}


def get_career_info(career):
    return CAREER_INFO.get(career, {
        "title": career,
        "description": "Explore this career path.",
        "skills": [],
        "tools": [],
        "roadmap": []
    })


# Skill mapping for career-specific analysis
CAREER_SKILL_MAPPING = {

    "AI": {
        "Mathematics": "math_marks",
        "Programming": "programming_marks",
        "Logical Reasoning": "logical_reasoning",
        "Coding Interest": "interest_coding"
    },

    "Data Science": {
        "Mathematics": "math_marks",
        "Programming": "programming_marks",
        "Logical Reasoning": "logical_reasoning",
        "Communication": "communication"
    },

    "HR": {
        "Communication": "communication",
        "Management Interest": "interest_management",
        "Logical Reasoning": "logical_reasoning"
    },

    "Management": {
        "Communication": "communication",
        "Management Interest": "interest_management",
        "Logical Reasoning": "logical_reasoning"
    }
}


def get_skill_gap_analysis(career, student_data):

    mapping = CAREER_SKILL_MAPPING.get(career, {})

    strengths = []
    improvements = []

    suggestions = {
        "Mathematics": "Practice statistics, algebra and problem-solving exercises.",
        "Programming": "Build Python projects and practice coding regularly.",
        "Logical Reasoning": "Solve logical puzzles and aptitude questions.",
        "Coding Interest": "Explore programming projects and real-world applications.",
        "Communication": "Practice presentations, group discussions and English speaking.",
        "Management Interest": "Learn leadership, planning and project management."
    }

    for skill, feature in mapping.items():

        score = float(student_data[feature])

        item = {
            "name": skill,
            "score": round(score, 1),
            "suggestion": suggestions.get(skill, "Practice this skill regularly.")
        }

        if score >= 70:
            strengths.append(item)
        else:
            improvements.append(item)

    return {
        "strengths": strengths,
        "improvements": improvements,
        "average_score": round(
            sum(float(student_data[f]) for f in mapping.values()) / len(mapping),
            1
        ) if mapping else 0
    }
