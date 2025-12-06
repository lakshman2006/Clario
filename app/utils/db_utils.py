import sqlite3
import os
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Manages database connections and operations using raw SQL.
    """
    
    def __init__(self, db_path: str = "app/data/clario.db"):
        self.db_path = db_path
        self.ensure_db_directory()
        self.init_database()
    
    def ensure_db_directory(self):
        """Ensure the database directory exists."""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
    
    def get_connection(self):
        """Get a database connection."""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize the database with required tables."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Create users table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        google_id TEXT UNIQUE,
                        email TEXT UNIQUE,
                        name TEXT,
                        picture TEXT,
                        role TEXT DEFAULT 'user',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create learning_goals table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS learning_goals (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        goal_title TEXT NOT NULL,
                        description TEXT,
                        difficulty_level INTEGER DEFAULT 1,
                        target_hours INTEGER DEFAULT 10,
                        deadline DATE,
                        status TEXT DEFAULT 'active',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                """)
                
                # Create time_availability table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS time_availability (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        day_of_week TEXT NOT NULL,
                        start_time TIME NOT NULL,
                        end_time TIME NOT NULL,
                        is_available BOOLEAN DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                """)
                
                # Create resources table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS resources (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT,
                        type TEXT NOT NULL,
                        url TEXT,
                        difficulty_level INTEGER DEFAULT 1,
                        estimated_hours REAL DEFAULT 1.0,
                        tags TEXT,
                        is_active BOOLEAN DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create schedules table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS schedules (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        title TEXT NOT NULL,
                        description TEXT,
                        start_date DATE NOT NULL,
                        end_date DATE NOT NULL,
                        status TEXT DEFAULT 'active',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                """)
                
                # Create schedule_items table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS schedule_items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        schedule_id INTEGER,
                        resource_id INTEGER,
                        day_of_week TEXT NOT NULL,
                        start_time TIME NOT NULL,
                        end_time TIME NOT NULL,
                        order_index INTEGER DEFAULT 0,
                        is_completed BOOLEAN DEFAULT 0,
                        completed_at TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (schedule_id) REFERENCES schedules (id),
                        FOREIGN KEY (resource_id) REFERENCES resources (id)
                    )
                """)
                
                # Create user_progress table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_progress (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        resource_id INTEGER,
                        schedule_item_id INTEGER,
                        progress_percentage REAL DEFAULT 0.0,
                        time_spent_minutes INTEGER DEFAULT 0,
                        last_accessed TIMESTAMP,
                        notes TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id),
                        FOREIGN KEY (resource_id) REFERENCES resources (id),
                        FOREIGN KEY (schedule_item_id) REFERENCES schedule_items (id)
                    )
                """)
                
                # Create sessions table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        access_token TEXT,
                        expires_at TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                """)
                
                # Create logs table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        event TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        ip_address TEXT
                    )
                """)
                
                # Create indexes for better performance
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_google_id ON users(google_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_learning_goals_user_id ON learning_goals(user_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_time_availability_user_id ON time_availability(user_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_schedules_user_id ON schedules(user_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_schedule_items_schedule_id ON schedule_items(schedule_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_progress_user_id ON user_progress(user_id)")
                
                conn.commit()
                logger.info("Database initialized successfully with all tables")
                
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Execute a SELECT query and return results as list of dictionaries.
        
        Args:
            query: SQL SELECT query
            params: Query parameters
            
        Returns:
            List of dictionaries representing rows
        """
        try:
            with self.get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, params)
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise
    
    def execute_insert(self, query: str, params: tuple = ()) -> int:
        """
        Execute an INSERT query and return the last row ID.
        
        Args:
            query: SQL INSERT query
            params: Query parameters
            
        Returns:
            Last inserted row ID
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.lastrowid
                
        except Exception as e:
            logger.error(f"Error executing insert: {e}")
            raise
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """
        Execute an UPDATE or DELETE query and return the number of affected rows.
        
        Args:
            query: SQL UPDATE or DELETE query
            params: Query parameters
            
        Returns:
            Number of affected rows
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount
                
        except Exception as e:
            logger.error(f"Error executing update: {e}")
            raise
    
    # User management methods
    def create_user(self, google_id: str, email: str, name: str, picture: str = None, role: str = "user") -> int:
        """Create a new user."""
        query = """
            INSERT INTO users (google_id, email, name, picture, role)
            VALUES (?, ?, ?, ?, ?)
        """
        return self.execute_insert(query, (google_id, email, name, picture, role))
    
    def get_user_by_google_id(self, google_id: str) -> Optional[Dict[str, Any]]:
        """Get user by Google ID."""
        query = "SELECT * FROM users WHERE google_id = ?"
        results = self.execute_query(query, (google_id,))
        return results[0] if results else None
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email."""
        query = "SELECT * FROM users WHERE email = ?"
        results = self.execute_query(query, (email,))
        return results[0] if results else None
    
    def update_user(self, user_id: int, **kwargs) -> int:
        """Update user information."""
        if not kwargs:
            return 0
        
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        query = f"UPDATE users SET {set_clause} WHERE id = ?"
        params = tuple(kwargs.values()) + (user_id,)
        return self.execute_update(query, params)
    
    # Session management methods
    def create_session(self, user_id: int, access_token: str, expires_at: str) -> int:
        """Create a new session."""
        query = """
            INSERT INTO sessions (user_id, access_token, expires_at)
            VALUES (?, ?, ?)
        """
        return self.execute_insert(query, (user_id, access_token, expires_at))
    
    def get_session(self, access_token: str) -> Optional[Dict[str, Any]]:
        """Get session by access token."""
        query = """
            SELECT s.*, u.* FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.access_token = ? AND s.expires_at > datetime('now')
        """
        results = self.execute_query(query, (access_token,))
        return results[0] if results else None
    
    def delete_session(self, access_token: str) -> int:
        """Delete a session."""
        query = "DELETE FROM sessions WHERE access_token = ?"
        return self.execute_update(query, (access_token,))
    
    # Logging methods
    def log_event(self, event: str, ip_address: str = None) -> int:
        """Log an event."""
        query = "INSERT INTO logs (event, ip_address) VALUES (?, ?)"
        return self.execute_insert(query, (event, ip_address))
    
    # Learning Goals methods
    def create_learning_goal(self, user_id: int, goal_title: str, description: str = None, 
                           difficulty_level: int = 1, target_hours: int = 10, deadline: str = None) -> int:
        """Create a new learning goal."""
        query = """
            INSERT INTO learning_goals (user_id, goal_title, description, difficulty_level, target_hours, deadline)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        return self.execute_insert(query, (user_id, goal_title, description, difficulty_level, target_hours, deadline))
    
    def get_user_learning_goals(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all learning goals for a user."""
        query = "SELECT * FROM learning_goals WHERE user_id = ? ORDER BY created_at DESC"
        return self.execute_query(query, (user_id,))
    
    def update_learning_goal(self, goal_id: int, **kwargs) -> int:
        """Update a learning goal."""
        if not kwargs:
            return 0
        
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        query = f"UPDATE learning_goals SET {set_clause} WHERE id = ?"
        params = tuple(kwargs.values()) + (goal_id,)
        return self.execute_update(query, params)
    
    def delete_learning_goal(self, goal_id: int) -> int:
        """Delete a learning goal."""
        query = "DELETE FROM learning_goals WHERE id = ?"
        return self.execute_update(query, (goal_id,))
    
    # Time Availability methods
    def set_time_availability(self, user_id: int, day_of_week: str, start_time: str, 
                            end_time: str, is_available: bool = True) -> int:
        """Set time availability for a user."""
        query = """
            INSERT INTO time_availability (user_id, day_of_week, start_time, end_time, is_available)
            VALUES (?, ?, ?, ?, ?)
        """
        return self.execute_insert(query, (user_id, day_of_week, start_time, end_time, is_available))
    
    def get_user_time_availability(self, user_id: int) -> List[Dict[str, Any]]:
        """Get time availability for a user."""
        query = "SELECT * FROM time_availability WHERE user_id = ? ORDER BY day_of_week, start_time"
        return self.execute_query(query, (user_id,))
    
    def update_time_availability(self, availability_id: int, **kwargs) -> int:
        """Update time availability."""
        if not kwargs:
            return 0
        
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        query = f"UPDATE time_availability SET {set_clause} WHERE id = ?"
        params = tuple(kwargs.values()) + (availability_id,)
        return self.execute_update(query, params)
    
    def delete_time_availability(self, availability_id: int) -> int:
        """Delete time availability."""
        query = "DELETE FROM time_availability WHERE id = ?"
        return self.execute_update(query, (availability_id,))
    
    # Resources methods
    def create_resource(self, title: str, description: str = None, type: str = "video", 
                       url: str = None, difficulty_level: int = 1, estimated_hours: float = 1.0, 
                       tags: str = None) -> int:
        """Create a new learning resource."""
        query = """
            INSERT INTO resources (title, description, type, url, difficulty_level, estimated_hours, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        return self.execute_insert(query, (title, description, type, url, difficulty_level, estimated_hours, tags))
    
    def get_all_resources(self, active_only: bool = True) -> List[Dict[str, Any]]:
        """Get all learning resources."""
        if active_only:
            query = "SELECT * FROM resources WHERE is_active = 1 ORDER BY title"
        else:
            query = "SELECT * FROM resources ORDER BY title"
        return self.execute_query(query)
    
    def get_resources_by_type(self, resource_type: str) -> List[Dict[str, Any]]:
        """Get resources by type."""
        query = "SELECT * FROM resources WHERE type = ? AND is_active = 1 ORDER BY title"
        return self.execute_query(query, (resource_type,))
    
    def get_resources_by_difficulty(self, difficulty_level: int) -> List[Dict[str, Any]]:
        """Get resources by difficulty level."""
        query = "SELECT * FROM resources WHERE difficulty_level = ? AND is_active = 1 ORDER BY title"
        return self.execute_query(query, (difficulty_level,))
    
    def update_resource(self, resource_id: int, **kwargs) -> int:
        """Update a resource."""
        if not kwargs:
            return 0
        
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        query = f"UPDATE resources SET {set_clause} WHERE id = ?"
        params = tuple(kwargs.values()) + (resource_id,)
        return self.execute_update(query, params)
    
    # Schedules methods
    def create_schedule(self, user_id: int, title: str, start_date: str, end_date: str, 
                       description: str = None) -> int:
        """Create a new learning schedule."""
        query = """
            INSERT INTO schedules (user_id, title, description, start_date, end_date)
            VALUES (?, ?, ?, ?, ?)
        """
        return self.execute_insert(query, (user_id, title, description, start_date, end_date))
    
    def get_user_schedules(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all schedules for a user."""
        query = "SELECT * FROM schedules WHERE user_id = ? ORDER BY created_at DESC"
        return self.execute_query(query, (user_id,))
    
    def get_schedule_with_items(self, schedule_id: int) -> Dict[str, Any]:
        """Get a schedule with its items."""
        # Get schedule
        schedule_query = "SELECT * FROM schedules WHERE id = ?"
        schedule = self.execute_query(schedule_query, (schedule_id,))
        
        if not schedule:
            return None
        
        # Get schedule items
        items_query = """
            SELECT si.*, r.title, r.type, r.url, r.difficulty_level, r.estimated_hours
            FROM schedule_items si
            JOIN resources r ON si.resource_id = r.id
            WHERE si.schedule_id = ?
            ORDER BY si.day_of_week, si.start_time
        """
        items = self.execute_query(items_query, (schedule_id,))
        
        return {
            "schedule": schedule[0],
            "items": items
        }
    
    def add_schedule_item(self, schedule_id: int, resource_id: int, day_of_week: str, 
                         start_time: str, end_time: str, order_index: int = 0) -> int:
        """Add an item to a schedule."""
        query = """
            INSERT INTO schedule_items (schedule_id, resource_id, day_of_week, start_time, end_time, order_index)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        return self.execute_insert(query, (schedule_id, resource_id, day_of_week, start_time, end_time, order_index))
    
    def update_schedule_item(self, item_id: int, **kwargs) -> int:
        """Update a schedule item."""
        if not kwargs:
            return 0
        
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        query = f"UPDATE schedule_items SET {set_clause} WHERE id = ?"
        params = tuple(kwargs.values()) + (item_id,)
        return self.execute_update(query, params)
    
    def mark_schedule_item_completed(self, item_id: int) -> int:
        """Mark a schedule item as completed."""
        query = """
            UPDATE schedule_items 
            SET is_completed = 1, completed_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        """
        return self.execute_update(query, (item_id,))
    
    # User Progress methods
    def update_user_progress(self, user_id: int, resource_id: int, schedule_item_id: int = None,
                           progress_percentage: float = 0.0, time_spent_minutes: int = 0, 
                           notes: str = None) -> int:
        """Update user progress on a resource."""
        query = """
            INSERT OR REPLACE INTO user_progress 
            (user_id, resource_id, schedule_item_id, progress_percentage, time_spent_minutes, notes, last_accessed)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """
        return self.execute_insert(query, (user_id, resource_id, schedule_item_id, progress_percentage, time_spent_minutes, notes))
    
    def get_user_progress(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user progress."""
        query = """
            SELECT up.*, r.title, r.type, r.url
            FROM user_progress up
            JOIN resources r ON up.resource_id = r.id
            WHERE up.user_id = ?
            ORDER BY up.last_accessed DESC
        """
        return self.execute_query(query, (user_id,))
