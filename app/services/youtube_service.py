"""
YouTube Video Processing Service

Simple and effective YouTube video processing for learning schedules.
No complex ML - just smart time breakdown and content extraction.
"""

import re
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class YouTubeService:
    """Service for processing YouTube videos into learning schedules."""
    
    def __init__(self):
        self.max_session_hours = 1.5  # Maximum session length (more realistic)
        self.min_session_hours = 0.5  # Minimum session length
    
    def extract_video_id(self, youtube_url: str) -> Optional[str]:
        """Extract video ID from YouTube URL."""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
            r'youtube\.com\/v\/([^&\n?#]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, youtube_url)
            if match:
                return match.group(1)
        return None
    
    def get_video_info(self, youtube_url: str) -> Dict[str, Any]:
        """Get video information (simplified - no API needed)."""
        video_id = self.extract_video_id(youtube_url)
        if not video_id:
            raise ValueError("Invalid YouTube URL")
        
        # Simple video info extraction (no API required)
        return {
            "video_id": video_id,
            "title": "Learning Video",
            "duration": "3:00:00",  # Default 3 hours
            "description": "Educational content for learning",
            "channel": "Learning Channel",
            "url": youtube_url
        }
    
    def parse_duration(self, duration_str: str) -> float:
        """Convert duration string to hours."""
        # Parse "3:00:00" or "1:30:00" format
        parts = duration_str.split(':')
        if len(parts) == 3:  # HH:MM:SS
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2])
            return hours + minutes/60 + seconds/3600
        elif len(parts) == 2:  # MM:SS
            minutes = int(parts[0])
            seconds = int(parts[1])
            return minutes/60 + seconds/3600
        else:  # Just seconds
            return int(parts[0])/3600
    
    def break_down_video(self, duration_hours: float) -> List[Dict[str, Any]]:
        """Break down video into smart learning sessions."""
        sessions = []
        remaining_hours = duration_hours
        session_number = 1
        
        while remaining_hours > 0:
            # Smart session sizing
            if remaining_hours <= self.min_session_hours:
                # If very little time left, add it to current session
                session_hours = remaining_hours
            elif remaining_hours <= self.max_session_hours:
                # If fits in one session, use all remaining time
                session_hours = remaining_hours
            else:
                # Use maximum session length
                session_hours = self.max_session_hours
            
            sessions.append({
                "session_number": session_number,
                "duration_hours": round(session_hours, 2),
                "title": f"Session {session_number}",
                "start_time_offset": sum(s["duration_hours"] for s in sessions),
                "end_time_offset": sum(s["duration_hours"] for s in sessions) + session_hours
            })
            
            remaining_hours -= session_hours
            session_number += 1
        
        return sessions
    
    def create_learning_sessions(self, youtube_url: str, target_duration_hours: float) -> List[Dict[str, Any]]:
        """Create intelligent learning sessions from YouTube video."""
        try:
            # Get video info
            video_info = self.get_video_info(youtube_url)
            
            # Use target duration (user input)
            duration_to_use = target_duration_hours
            
            # Break down into sessions
            sessions = self.break_down_video(duration_to_use)
            
            # Generate meaningful topics for each session
            sessions = self._generate_session_topics(sessions, video_info, duration_to_use)
            
            # Enhance sessions with video content
            for session in sessions:
                session.update({
                    "video_url": youtube_url,
                    "video_id": video_info["video_id"],
                    "video_title": video_info["title"],
                    "video_description": video_info["description"],
                    "channel": video_info["channel"],
                    "original_duration": duration_to_use
                })
            
            logger.info(f"Created {len(sessions)} learning sessions for {duration_to_use}h video")
            return sessions
            
        except Exception as e:
            logger.error(f"Error processing YouTube video: {e}")
            # Fallback to simple breakdown
            return self._create_fallback_sessions(youtube_url, target_duration_hours)
    
    def _create_fallback_sessions(self, youtube_url: str, duration_hours: float) -> List[Dict[str, Any]]:
        """Fallback method if processing fails."""
        sessions = self.break_down_video(duration_hours)
        for session in sessions:
            session.update({
                "video_url": youtube_url,
                "video_id": "unknown",
                "video_title": "Learning Video",
                "video_description": "Educational content",
                "channel": "Unknown",
                "original_duration": duration_hours
            })
        return sessions
    
    def _generate_session_topics(self, sessions: List[Dict[str, Any]], video_info: Dict[str, Any], total_duration: float) -> List[Dict[str, Any]]:
        """Generate meaningful learning topics for each session based on video content."""
        try:
            # Extract base topic from video title and description
            base_topic = self._extract_base_topic(video_info["title"], video_info["description"])
            
            # Generate progressive topics for each session
            for i, session in enumerate(sessions):
                session_number = session["session_number"]
                session_duration = session["duration_hours"]
                
                # Generate topic based on session position and duration
                topic = self._generate_session_topic(
                    base_topic, 
                    session_number, 
                    len(sessions), 
                    session_duration,
                    i
                )
                
                # Update session with meaningful title and topic
                session["title"] = topic["title"]
                session["learning_topic"] = topic["topic"]
                session["learning_objectives"] = topic["objectives"]
                session["key_concepts"] = topic["concepts"]
                
            return sessions
            
        except Exception as e:
            logger.error(f"Error generating session topics: {e}")
            # Fallback to simple session titles
            for i, session in enumerate(sessions):
                session["title"] = f"Learning Session {session['session_number']}"
                session["learning_topic"] = f"Part {session['session_number']} of the course"
                session["learning_objectives"] = ["Continue learning from the video"]
                session["key_concepts"] = ["Video content"]
            return sessions
    
    def _extract_base_topic(self, title: str, description: str) -> str:
        """Extract the main learning topic from video title and description."""
        # Common programming/tech topics
        topic_keywords = {
            "python": "Python Programming",
            "javascript": "JavaScript Development", 
            "react": "React.js Development",
            "machine learning": "Machine Learning",
            "data science": "Data Science",
            "web development": "Web Development",
            "algorithms": "Algorithms & Data Structures",
            "database": "Database Design",
            "api": "API Development",
            "devops": "DevOps",
            "docker": "Docker & Containers",
            "kubernetes": "Kubernetes",
            "aws": "AWS Cloud Computing",
            "azure": "Microsoft Azure",
            "gcp": "Google Cloud Platform",
            "tutorial": "Tutorial",
            "course": "Course",
            "guide": "Guide",
            "fundamentals": "Fundamentals",
            "advanced": "Advanced Topics"
        }
        
        # Combine title and description for analysis
        text = f"{title} {description}".lower()
        
        # Find matching topics
        for keyword, topic in topic_keywords.items():
            if keyword in text:
                return topic
        
        # Default fallback
        return "Programming & Technology"
    
    def _generate_session_topic(self, base_topic: str, session_num: int, total_sessions: int, duration: float, index: int) -> Dict[str, Any]:
        """Generate a specific learning topic for a session."""
        
        # Learning progression patterns
        progression_patterns = {
            "Python Programming": [
                "Introduction & Setup", "Variables & Data Types", "Control Structures", 
                "Functions & Modules", "Object-Oriented Programming", "File Handling",
                "Error Handling", "Advanced Concepts", "Projects & Applications"
            ],
            "JavaScript Development": [
                "JavaScript Basics", "DOM Manipulation", "Event Handling", 
                "Functions & Scope", "Objects & Arrays", "Async Programming",
                "ES6+ Features", "Frameworks & Libraries", "Real-world Projects"
            ],
            "Machine Learning": [
                "ML Fundamentals", "Data Preprocessing", "Supervised Learning",
                "Unsupervised Learning", "Neural Networks", "Deep Learning",
                "Model Evaluation", "Advanced Algorithms", "Real-world Applications"
            ],
            "Web Development": [
                "HTML & CSS Basics", "Responsive Design", "JavaScript Fundamentals",
                "Backend Development", "Database Integration", "API Development",
                "Authentication", "Deployment", "Advanced Features"
            ],
            "Algorithms & Data Structures": [
                "Algorithm Basics", "Arrays & Strings", "Linked Lists",
                "Stacks & Queues", "Trees & Graphs", "Sorting Algorithms",
                "Searching Algorithms", "Dynamic Programming", "Advanced Topics"
            ]
        }
        
        # Get progression for the base topic
        progression = progression_patterns.get(base_topic, [
            "Introduction", "Core Concepts", "Practical Examples", 
            "Advanced Topics", "Real-world Applications", "Best Practices",
            "Troubleshooting", "Optimization", "Final Projects"
        ])
        
        # Select topic based on session position
        if session_num <= len(progression):
            topic = progression[session_num - 1]
        else:
            # For extra sessions, use advanced topics
            topic = f"Advanced {base_topic} Concepts"
        
        # Generate learning objectives based on topic and duration
        objectives = self._generate_learning_objectives(topic, duration, session_num, total_sessions)
        
        # Generate key concepts
        concepts = self._generate_key_concepts(topic, base_topic)
        
        return {
            "title": f"{topic} - Session {session_num}",
            "topic": topic,
            "objectives": objectives,
            "concepts": concepts
        }
    
    def _generate_learning_objectives(self, topic: str, duration: float, session_num: int, total_sessions: int) -> List[str]:
        """Generate learning objectives for a session."""
        objectives = []
        
        # Base objectives based on session position
        if session_num == 1:
            objectives.append(f"Understand the fundamentals of {topic}")
            objectives.append("Set up the learning environment")
        elif session_num == total_sessions:
            objectives.append(f"Master advanced concepts in {topic}")
            objectives.append("Apply knowledge to real-world projects")
        else:
            objectives.append(f"Learn intermediate concepts of {topic}")
            objectives.append("Practice with hands-on examples")
        
        # Duration-based objectives
        if duration >= 2.0:
            objectives.append("Complete comprehensive exercises")
            objectives.append("Work on practical projects")
        elif duration >= 1.0:
            objectives.append("Practice key concepts")
            objectives.append("Solve coding problems")
        else:
            objectives.append("Review and reinforce concepts")
        
        return objectives
    
    def _generate_key_concepts(self, topic: str, base_topic: str) -> List[str]:
        """Generate key concepts for a session."""
        concept_templates = {
            "Introduction": ["Basic concepts", "Terminology", "Overview"],
            "Variables": ["Data types", "Variable declaration", "Naming conventions"],
            "Functions": ["Function definition", "Parameters", "Return values"],
            "Control Structures": ["Conditionals", "Loops", "Flow control"],
            "Object-Oriented": ["Classes", "Objects", "Inheritance", "Polymorphism"],
            "Data Structures": ["Arrays", "Lists", "Dictionaries", "Sets"],
            "Algorithms": ["Problem solving", "Time complexity", "Space complexity"],
            "Machine Learning": ["Training data", "Models", "Predictions", "Evaluation"],
            "Web Development": ["HTML structure", "CSS styling", "JavaScript functionality"],
            "Database": ["Tables", "Queries", "Relationships", "Indexing"]
        }
        
        # Find matching concepts
        for key, concepts in concept_templates.items():
            if key.lower() in topic.lower():
                return concepts
        
        # Default concepts
        return ["Core concepts", "Practical examples", "Best practices"]
