"""
Pydantic schemas for Learning Schedule Management

Defines request/response models for schedule generation and management.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import date, time
from enum import Enum

class DayOfWeek(str, Enum):
    """Days of the week enum."""
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"

class ResourceType(str, Enum):
    """Learning resource types."""
    VIDEO = "video"
    ARTICLE = "article"
    COURSE = "course"
    BOOK = "book"
    PODCAST = "podcast"
    EXERCISE = "exercise"

class DifficultyLevel(int, Enum):
    """Difficulty levels (1-5 scale)."""
    BEGINNER = 1
    ELEMENTARY = 2
    INTERMEDIATE = 3
    ADVANCED = 4
    EXPERT = 5

# Request Models
class LearningGoalRequest(BaseModel):
    """Request model for creating a learning goal."""
    goal_title: str = Field(..., min_length=1, max_length=200, description="Title of the learning goal")
    description: Optional[str] = Field(None, max_length=1000, description="Detailed description of the goal")
    difficulty_level: int = Field(1, ge=1, le=5, description="Difficulty level (1-5)")
    target_hours: int = Field(10, ge=1, le=1000, description="Target hours to complete this goal")
    deadline: Optional[str] = Field(None, description="Deadline in YYYY-MM-DD format")
    
    @validator('deadline')
    def validate_deadline(cls, v):
        if v is not None:
            try:
                date.fromisoformat(v)
            except ValueError:
                raise ValueError('Deadline must be in YYYY-MM-DD format')
        return v

class TimeAvailabilityRequest(BaseModel):
    """Request model for setting time availability."""
    day_of_week: DayOfWeek = Field(..., description="Day of the week")
    start_time: str = Field(..., description="Start time in HH:MM format")
    end_time: str = Field(..., description="End time in HH:MM format")
    is_available: bool = Field(True, description="Whether this time slot is available")
    
    @validator('start_time', 'end_time')
    def validate_time_format(cls, v):
        try:
            time.fromisoformat(v)
        except ValueError:
            raise ValueError('Time must be in HH:MM format')
        return v

class ScheduleGenerationRequest(BaseModel):
    """Request model for generating a learning schedule."""
    goal_ids: List[int] = Field(..., min_items=1, description="List of goal IDs to include in schedule")
    start_date: str = Field(..., description="Schedule start date in YYYY-MM-DD format")
    end_date: str = Field(..., description="Schedule end date in YYYY-MM-DD format")
    title: Optional[str] = Field(None, max_length=200, description="Custom schedule title")
    description: Optional[str] = Field(None, max_length=1000, description="Schedule description")
    
    @validator('start_date', 'end_date')
    def validate_date_format(cls, v):
        try:
            date.fromisoformat(v)
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
        return v
    
    @validator('end_date')
    def validate_end_after_start(cls, v, values):
        if 'start_date' in values:
            start = date.fromisoformat(values['start_date'])
            end = date.fromisoformat(v)
            if end <= start:
                raise ValueError('End date must be after start date')
        return v

class ScheduleUpdateRequest(BaseModel):
    """Request model for updating a schedule."""
    title: Optional[str] = Field(None, max_length=200, description="Updated schedule title")
    description: Optional[str] = Field(None, max_length=1000, description="Updated description")
    status: Optional[str] = Field(None, description="Schedule status")

# Response Models
class ScheduleItemResponse(BaseModel):
    """Response model for a schedule item."""
    id: Optional[int] = None
    resource_id: int
    resource_title: str
    resource_type: str
    day_of_week: str
    start_time: str
    end_time: str
    difficulty_level: int
    estimated_hours: float
    order_index: int
    is_completed: bool = False
    completed_at: Optional[str] = None

class ScheduleResponse(BaseModel):
    """Response model for a complete schedule."""
    id: int
    user_id: int
    title: str
    description: Optional[str]
    start_date: str
    end_date: str
    status: str
    total_hours: float
    available_hours: float
    efficiency: float
    feasible: bool = True
    goals_covered: List[str]
    schedule_items: List[ScheduleItemResponse]
    generated_at: str
    created_at: str

class ScheduleListResponse(BaseModel):
    """Response model for a list of schedules."""
    id: int
    title: str
    description: Optional[str]
    start_date: str
    end_date: str
    status: str
    total_hours: float
    efficiency: float
    goals_count: int
    items_count: int
    created_at: str

class ScheduleValidationResponse(BaseModel):
    """Response model for schedule feasibility validation."""
    feasible: bool
    needed_hours: float
    available_hours: float
    efficiency_percentage: float
    recommendations: List[str]
    goals_count: int
    time_slots_count: int

class ScheduleGenerationResponse(BaseModel):
    """Response model for schedule generation."""
    status: str
    message: str
    data: Optional[ScheduleResponse] = None
    validation: Optional[ScheduleValidationResponse] = None

# Utility Models
class TimeSlotInfo(BaseModel):
    """Information about a time slot."""
    day_of_week: str
    start_time: str
    end_time: str
    duration_minutes: int
    is_available: bool

class GoalProgressInfo(BaseModel):
    """Information about goal progress."""
    goal_id: int
    goal_title: str
    target_hours: int
    completed_hours: float
    progress_percentage: float
    difficulty_level: int

class ScheduleStatsResponse(BaseModel):
    """Response model for schedule statistics."""
    total_schedules: int
    active_schedules: int
    completed_schedules: int
    total_learning_hours: float
    average_efficiency: float
    most_common_goals: List[str]
    preferred_learning_times: Dict[str, int]

# Error Response Models
class ScheduleErrorResponse(BaseModel):
    """Error response model for schedule operations."""
    status: str = "error"
    message: str
    error_code: str
    details: Optional[Dict[str, Any]] = None

class ValidationErrorResponse(BaseModel):
    """Validation error response model."""
    status: str = "error"
    message: str = "Validation error"
    error_code: str = "VALIDATION_ERROR"
    details: List[Dict[str, Any]]

# Success Response Models
class SuccessResponse(BaseModel):
    """Generic success response model."""
    status: str = "success"
    message: str
    data: Optional[Dict[str, Any]] = None

class ScheduleCreatedResponse(BaseModel):
    """Response model for successful schedule creation."""
    status: str = "success"
    message: str = "Schedule created successfully"
    data: ScheduleResponse

class ScheduleUpdatedResponse(BaseModel):
    """Response model for successful schedule update."""
    status: str = "success"
    message: str = "Schedule updated successfully"
    data: ScheduleResponse

class ScheduleDeletedResponse(BaseModel):
    """Response model for successful schedule deletion."""
    status: str = "success"
    message: str = "Schedule deleted successfully"
