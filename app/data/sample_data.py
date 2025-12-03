"""
Sample data for testing the Learning Schedule Maker

This module provides sample data for testing the schedule generation algorithm.
"""

from app.utils.db_utils import DatabaseManager

def create_sample_data():
    """Create sample data for testing."""
    db = DatabaseManager()
    
    # Get or create sample user
    existing_user = db.execute_query(
        "SELECT id FROM users WHERE email = ?", ("test@example.com",)
    )
    
    if existing_user:
        user_id = existing_user[0]['id']
        print(f"Using existing user ID: {user_id}")
    else:
        user_id = db.create_user(
            google_id="sample_user_123",
            email="test@example.com",
            name="Test User",
            picture="https://example.com/avatar.jpg"
        )
        print(f"Created new user ID: {user_id}")
    
    # Create sample learning goals
    goals = [
        {
            "goal_title": "Learn Python Programming",
            "description": "Master Python fundamentals and advanced concepts",
            "difficulty_level": 2,
            "target_hours": 20,
            "deadline": "2024-02-15"
        },
        {
            "goal_title": "Data Science with Pandas",
            "description": "Learn data manipulation and analysis with pandas",
            "difficulty_level": 3,
            "target_hours": 15,
            "deadline": "2024-02-20"
        },
        {
            "goal_title": "Machine Learning Basics",
            "description": "Introduction to ML algorithms and scikit-learn",
            "difficulty_level": 4,
            "target_hours": 25,
            "deadline": "2024-03-01"
        }
    ]
    
    goal_ids = []
    for goal in goals:
        goal_id = db.create_learning_goal(
            user_id=user_id,
            goal_title=goal["goal_title"],
            description=goal["description"],
            difficulty_level=goal["difficulty_level"],
            target_hours=goal["target_hours"],
            deadline=goal["deadline"]
        )
        goal_ids.append(goal_id)
    
    # Create sample time availability
    time_slots = [
        {"day_of_week": "monday", "start_time": "09:00", "end_time": "11:00"},
        {"day_of_week": "monday", "start_time": "14:00", "end_time": "16:00"},
        {"day_of_week": "tuesday", "start_time": "10:00", "end_time": "12:00"},
        {"day_of_week": "tuesday", "start_time": "19:00", "end_time": "21:00"},
        {"day_of_week": "wednesday", "start_time": "09:00", "end_time": "11:00"},
        {"day_of_week": "wednesday", "start_time": "15:00", "end_time": "17:00"},
        {"day_of_week": "thursday", "start_time": "10:00", "end_time": "12:00"},
        {"day_of_week": "thursday", "start_time": "18:00", "end_time": "20:00"},
        {"day_of_week": "friday", "start_time": "09:00", "end_time": "11:00"},
        {"day_of_week": "saturday", "start_time": "10:00", "end_time": "14:00"},
        {"day_of_week": "sunday", "start_time": "14:00", "end_time": "18:00"}
    ]
    
    for slot in time_slots:
        db.set_time_availability(
            user_id=user_id,
            day_of_week=slot["day_of_week"],
            start_time=slot["start_time"],
            end_time=slot["end_time"],
            is_available=True
        )
    
    # Create sample learning resources
    resources = [
        # Python Resources
        {
            "title": "Python Basics Tutorial",
            "description": "Complete Python fundamentals course",
            "type": "video",
            "url": "https://example.com/python-basics",
            "difficulty_level": 1,
            "estimated_hours": 3.0,
            "tags": "python,programming,basics"
        },
        {
            "title": "Python Data Structures",
            "description": "Learn lists, dictionaries, and tuples",
            "type": "article",
            "url": "https://example.com/python-data-structures",
            "difficulty_level": 2,
            "estimated_hours": 2.5,
            "tags": "python,data-structures"
        },
        {
            "title": "Object-Oriented Programming in Python",
            "description": "Classes, objects, and inheritance",
            "type": "video",
            "url": "https://example.com/python-oop",
            "difficulty_level": 3,
            "estimated_hours": 4.0,
            "tags": "python,oop,classes"
        },
        {
            "title": "Python Advanced Concepts",
            "description": "Decorators, generators, and context managers",
            "type": "course",
            "url": "https://example.com/python-advanced",
            "difficulty_level": 4,
            "estimated_hours": 6.0,
            "tags": "python,advanced,decorators"
        },
        
        # Data Science Resources
        {
            "title": "Pandas Introduction",
            "description": "Getting started with pandas for data analysis",
            "type": "video",
            "url": "https://example.com/pandas-intro",
            "difficulty_level": 2,
            "estimated_hours": 3.0,
            "tags": "pandas,data-science,dataframe"
        },
        {
            "title": "Data Manipulation with Pandas",
            "description": "Filtering, grouping, and transforming data",
            "type": "article",
            "url": "https://example.com/pandas-manipulation",
            "difficulty_level": 3,
            "estimated_hours": 4.0,
            "tags": "pandas,data-manipulation"
        },
        {
            "title": "Pandas Advanced Techniques",
            "description": "Multi-index, pivot tables, and performance optimization",
            "type": "course",
            "url": "https://example.com/pandas-advanced",
            "difficulty_level": 4,
            "estimated_hours": 5.0,
            "tags": "pandas,advanced,optimization"
        },
        
        # Machine Learning Resources
        {
            "title": "Introduction to Machine Learning",
            "description": "Basic concepts and terminology",
            "type": "video",
            "url": "https://example.com/ml-intro",
            "difficulty_level": 2,
            "estimated_hours": 2.0,
            "tags": "machine-learning,introduction"
        },
        {
            "title": "Scikit-learn Tutorial",
            "description": "Hands-on ML with scikit-learn",
            "type": "course",
            "url": "https://example.com/scikit-learn",
            "difficulty_level": 3,
            "estimated_hours": 8.0,
            "tags": "scikit-learn,machine-learning,hands-on"
        },
        {
            "title": "Linear Regression Explained",
            "description": "Understanding and implementing linear regression",
            "type": "article",
            "url": "https://example.com/linear-regression",
            "difficulty_level": 3,
            "estimated_hours": 3.0,
            "tags": "regression,linear-algebra"
        },
        {
            "title": "Classification Algorithms",
            "description": "Decision trees, random forests, and SVM",
            "type": "video",
            "url": "https://example.com/classification",
            "difficulty_level": 4,
            "estimated_hours": 6.0,
            "tags": "classification,algorithms,decision-trees"
        },
        {
            "title": "Model Evaluation and Validation",
            "description": "Cross-validation, metrics, and overfitting",
            "type": "course",
            "url": "https://example.com/model-evaluation",
            "difficulty_level": 4,
            "estimated_hours": 4.0,
            "tags": "evaluation,validation,metrics"
        }
    ]
    
    resource_ids = []
    for resource in resources:
        resource_id = db.create_resource(
            title=resource["title"],
            description=resource["description"],
            type=resource["type"],
            url=resource["url"],
            difficulty_level=resource["difficulty_level"],
            estimated_hours=resource["estimated_hours"],
            tags=resource["tags"]
        )
        resource_ids.append(resource_id)
    
    print("Sample data created successfully!")
    print(f"   User ID: {user_id}")
    print(f"   Goals created: {len(goal_ids)}")
    print(f"   Time slots created: {len(time_slots)}")
    print(f"   Resources created: {len(resource_ids)}")
    
    return {
        "user_id": user_id,
        "goal_ids": goal_ids,
        "resource_ids": resource_ids
    }

if __name__ == "__main__":
    create_sample_data()
