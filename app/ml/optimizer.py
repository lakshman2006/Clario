"""
Learning Schedule Optimization Algorithm

This module implements the core ML feature - generating personalized learning schedules
based on user goals, time availability, and resource difficulty levels.
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta, time
from dataclasses import dataclass
import math

logger = logging.getLogger(__name__)

@dataclass
class TimeSlot:
    """Represents a time slot for learning."""
    day_of_week: str
    start_time: time
    end_time: time
    duration_minutes: int
    
    def __post_init__(self):
        if self.duration_minutes == 0:
            start_dt = datetime.combine(datetime.today(), self.start_time)
            end_dt = datetime.combine(datetime.today(), self.end_time)
            self.duration_minutes = int((end_dt - start_dt).total_seconds() / 60)

@dataclass
class LearningResource:
    """Represents a learning resource."""
    id: int
    title: str
    type: str
    difficulty_level: int
    estimated_hours: float
    tags: Optional[str] = None
    url: Optional[str] = None

@dataclass
class LearningGoal:
    """Represents a user's learning goal."""
    id: int
    goal_title: str
    description: Optional[str]
    difficulty_level: int
    target_hours: int
    deadline: Optional[str] = None

@dataclass
class ScheduleItem:
    """Represents a scheduled learning item."""
    resource_id: int
    resource_title: str
    resource_type: str
    day_of_week: str
    start_time: time
    end_time: time
    difficulty_level: int
    estimated_hours: float
    order_index: int = 0

class ScheduleOptimizer:
    """
    Learning Schedule Optimization Algorithm
    
    Creates personalized learning schedules by:
    1. Analyzing user goals and time availability
    2. Matching resources to available time slots
    3. Optimizing for difficulty progression and learning efficiency
    4. Considering user preferences and constraints
    """
    
    def __init__(self):
        self.week_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        self.optimal_session_duration = 90  # minutes
        self.break_duration = 15  # minutes between sessions
        self.max_daily_hours = 6  # maximum learning hours per day
        
    def generate_schedule(
        self,
        user_id: int,
        goals: List[LearningGoal],
        time_availability: List[Dict[str, Any]],
        resources: List[LearningResource],
        start_date: str,
        end_date: str,
        title: str = "Personalized Learning Schedule",
        description: str = None
    ) -> Dict[str, Any]:
        """
        Generate a personalized learning schedule.
        
        Args:
            user_id: User ID
            goals: List of learning goals
            time_availability: User's available time slots
            resources: Available learning resources
            start_date: Schedule start date (YYYY-MM-DD)
            end_date: Schedule end date (YYYY-MM-DD)
            title: Schedule title
            description: Schedule description
            
        Returns:
            Generated schedule with optimized time slots
        """
        try:
            logger.info(f"Generating schedule for user {user_id} with {len(goals)} goals")
            
            # Step 1: Analyze goals and calculate total learning time needed
            total_hours_needed = self._calculate_total_learning_time(goals)
            logger.info(f"Total learning time needed: {total_hours_needed} hours")
            
            # Step 2: Process time availability into usable slots
            available_slots = self._process_time_availability(time_availability)
            total_available_hours = self._calculate_available_hours(available_slots)
            logger.info(f"Total available time: {total_available_hours} hours")
            
            # Step 3: Validate if schedule is feasible
            if total_available_hours < total_hours_needed:
                logger.warning(f"Insufficient time: need {total_hours_needed}h, have {total_available_hours}h")
                return self._create_infeasible_schedule(user_id, goals, total_hours_needed, total_available_hours)
            
            # Step 4: Match resources to goals based on difficulty and type
            goal_resource_mapping = self._match_resources_to_goals(goals, resources)
            
            # Step 5: Optimize time slot allocation
            schedule_items = self._optimize_time_allocation(
                goals, goal_resource_mapping, available_slots, total_hours_needed
            )
            
            # Step 6: Create final schedule structure
            schedule = {
                "user_id": user_id,
                "title": title,
                "description": description or f"Personalized schedule for {len(goals)} learning goals",
                "start_date": start_date,
                "end_date": end_date,
                "total_hours": total_hours_needed,
                "available_hours": total_available_hours,
                "efficiency": round((total_hours_needed / total_available_hours) * 100, 1),
                "schedule_items": schedule_items,
                "goals_covered": [goal.goal_title for goal in goals],
                "generated_at": datetime.now().isoformat()
            }
            
            logger.info(f"Schedule generated successfully with {len(schedule_items)} items")
            return schedule
            
        except Exception as e:
            logger.error(f"Error generating schedule: {e}")
            raise
    
    def _calculate_total_learning_time(self, goals: List[LearningGoal]) -> float:
        """Calculate total learning time needed for all goals."""
        return sum(goal.target_hours for goal in goals)
    
    def _process_time_availability(self, time_availability: List[Dict[str, Any]]) -> List[TimeSlot]:
        """Process raw time availability data into TimeSlot objects."""
        slots = []
        
        for availability in time_availability:
            if not availability.get('is_available', True):
                continue
                
            try:
                start_time = datetime.strptime(availability['start_time'], '%H:%M').time()
                end_time = datetime.strptime(availability['end_time'], '%H:%M').time()
                day = availability['day_of_week'].lower()
                
                # Calculate duration
                start_dt = datetime.combine(datetime.today(), start_time)
                end_dt = datetime.combine(datetime.today(), end_time)
                duration = int((end_dt - start_dt).total_seconds() / 60)
                
                if duration > 0:
                    slots.append(TimeSlot(
                        day_of_week=day,
                        start_time=start_time,
                        end_time=end_time,
                        duration_minutes=duration
                    ))
                    
            except (ValueError, KeyError) as e:
                logger.warning(f"Invalid time availability data: {e}")
                continue
        
        return slots
    
    def _calculate_available_hours(self, slots: List[TimeSlot]) -> float:
        """Calculate total available learning hours per week."""
        total_minutes = sum(slot.duration_minutes for slot in slots)
        return total_minutes / 60.0
    
    def _match_resources_to_goals(
        self, 
        goals: List[LearningGoal], 
        resources: List[LearningResource]
    ) -> Dict[int, List[LearningResource]]:
        """
        Match resources to goals based on difficulty and content type.
        
        Returns:
            Dictionary mapping goal_id to list of suitable resources
        """
        goal_resource_mapping = {}
        
        for goal in goals:
            suitable_resources = []
            
            # Filter resources by difficulty level (within 1 level of goal difficulty)
            for resource in resources:
                difficulty_diff = abs(resource.difficulty_level - goal.difficulty_level)
                
                # Match if difficulty is within 1 level or resource is easier
                if difficulty_diff <= 1 or resource.difficulty_level <= goal.difficulty_level:
                    suitable_resources.append(resource)
            
            # Sort by difficulty (easier resources first for progression)
            suitable_resources.sort(key=lambda r: r.difficulty_level)
            
            goal_resource_mapping[goal.id] = suitable_resources
            logger.info(f"Goal '{goal.goal_title}' matched with {len(suitable_resources)} resources")
        
        return goal_resource_mapping
    
    def _optimize_time_allocation(
        self,
        goals: List[LearningGoal],
        goal_resource_mapping: Dict[int, List[LearningResource]],
        available_slots: List[TimeSlot],
        total_hours_needed: float
    ) -> List[ScheduleItem]:
        """
        Optimize time allocation across available slots.
        
        Strategy:
        1. Prioritize goals by deadline (if any)
        2. Allocate time proportionally based on target hours
        3. Consider difficulty progression (easier first)
        4. Respect time slot constraints
        """
        schedule_items = []
        order_index = 0
        
        # Sort goals by deadline (earliest first) and then by difficulty
        sorted_goals = sorted(goals, key=lambda g: (g.deadline or '9999-12-31', g.difficulty_level))
        
        # Calculate time allocation per goal
        total_target_hours = sum(goal.target_hours for goal in goals)
        time_per_goal = {}
        
        for goal in goals:
            if total_target_hours > 0:
                proportion = goal.target_hours / total_target_hours
                time_per_goal[goal.id] = total_hours_needed * proportion
            else:
                time_per_goal[goal.id] = 0
        
        # Allocate time slots
        for goal in sorted_goals:
            goal_hours = time_per_goal[goal.id]
            if goal_hours <= 0:
                continue
                
            goal_resources = goal_resource_mapping.get(goal.id, [])
            if not goal_resources:
                continue
            
            # Allocate time for this goal across available slots
            allocated_items = self._allocate_goal_time(
                goal, goal_resources, available_slots, goal_hours, order_index
            )
            
            schedule_items.extend(allocated_items)
            order_index += len(allocated_items)
        
        # Sort schedule items by day and time
        schedule_items.sort(key=lambda item: (
            self.week_days.index(item.day_of_week.lower()),
            item.start_time
        ))
        
        return schedule_items
    
    def _allocate_goal_time(
        self,
        goal: LearningGoal,
        resources: List[LearningResource],
        available_slots: List[TimeSlot],
        target_hours: float,
        start_order_index: int
    ) -> List[ScheduleItem]:
        """Allocate time for a specific goal across available slots."""
        items = []
        remaining_hours = target_hours
        order_index = start_order_index
        
        # Sort resources by difficulty (easier first for progression)
        sorted_resources = sorted(resources, key=lambda r: r.difficulty_level)
        
        for slot in available_slots:
            if remaining_hours <= 0:
                break
                
            # Calculate how much time we can use in this slot
            slot_hours = slot.duration_minutes / 60.0
            max_session_hours = min(slot_hours, self.optimal_session_duration / 60.0)
            session_hours = min(max_session_hours, remaining_hours)
            
            if session_hours <= 0:
                continue
            
            # Find best resource for this time slot
            best_resource = self._select_best_resource(
                sorted_resources, session_hours, goal.difficulty_level
            )
            
            if best_resource:
                # Calculate session times
                session_duration = int(session_hours * 60)
                end_time = self._add_minutes_to_time(slot.start_time, session_duration)
                
                # Ensure we don't exceed slot end time
                if end_time > slot.end_time:
                    end_time = slot.end_time
                    session_duration = self._time_difference_minutes(slot.start_time, end_time)
                
                if session_duration > 0:
                    items.append(ScheduleItem(
                        resource_id=best_resource.id,
                        resource_title=best_resource.title,
                        resource_type=best_resource.type,
                        day_of_week=slot.day_of_week,
                        start_time=slot.start_time,
                        end_time=end_time,
                        difficulty_level=best_resource.difficulty_level,
                        estimated_hours=session_duration / 60.0,
                        order_index=order_index
                    ))
                    
                    remaining_hours -= session_duration / 60.0
                    order_index += 1
        
        return items
    
    def _select_best_resource(
        self,
        resources: List[LearningResource],
        available_hours: float,
        goal_difficulty: int
    ) -> Optional[LearningResource]:
        """Select the best resource for a time slot."""
        if not resources:
            return None
        
        # Filter resources that fit the time constraint
        suitable_resources = [
            r for r in resources 
            if r.estimated_hours <= available_hours * 1.5  # Allow some flexibility
        ]
        
        if not suitable_resources:
            # If no resources fit, take the shortest one
            suitable_resources = [min(resources, key=lambda r: r.estimated_hours)]
        
        # Select based on difficulty match and duration
        best_resource = min(suitable_resources, key=lambda r: (
            abs(r.difficulty_level - goal_difficulty),
            r.estimated_hours
        ))
        
        return best_resource
    
    def _add_minutes_to_time(self, time_obj: time, minutes: int) -> time:
        """Add minutes to a time object."""
        dt = datetime.combine(datetime.today(), time_obj)
        new_dt = dt + timedelta(minutes=minutes)
        return new_dt.time()
    
    def _time_difference_minutes(self, start_time: time, end_time: time) -> int:
        """Calculate difference between two times in minutes."""
        start_dt = datetime.combine(datetime.today(), start_time)
        end_dt = datetime.combine(datetime.today(), end_time)
        return int((end_dt - start_dt).total_seconds() / 60)
    
    def _create_infeasible_schedule(
        self,
        user_id: int,
        goals: List[LearningGoal],
        needed_hours: float,
        available_hours: float
    ) -> Dict[str, Any]:
        """Create a schedule when time constraints make it infeasible."""
        return {
            "user_id": user_id,
            "title": "Schedule - Insufficient Time",
            "description": f"Schedule cannot be completed with available time",
            "feasible": False,
            "needed_hours": needed_hours,
            "available_hours": available_hours,
            "deficit_hours": needed_hours - available_hours,
            "recommendations": [
                "Increase available learning time",
                "Reduce number of goals",
                "Extend deadline",
                "Focus on higher priority goals"
            ],
            "schedule_items": [],
            "generated_at": datetime.now().isoformat()
        }
    
    def validate_schedule_feasibility(
        self,
        goals: List[LearningGoal],
        time_availability: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Validate if a schedule is feasible given constraints.
        
        Returns:
            Validation results with recommendations
        """
        total_hours_needed = self._calculate_total_learning_time(goals)
        available_slots = self._process_time_availability(time_availability)
        total_available_hours = self._calculate_available_hours(available_slots)
        
        feasible = total_available_hours >= total_hours_needed
        efficiency = (total_hours_needed / total_available_hours * 100) if total_available_hours > 0 else 0
        
        recommendations = []
        if not feasible:
            deficit = total_hours_needed - total_available_hours
            recommendations.extend([
                f"Need {deficit:.1f} more hours per week",
                "Consider reducing number of goals",
                "Extend learning timeline",
                "Increase daily learning time"
            ])
        elif efficiency < 50:
            recommendations.append("Consider adding more learning goals")
        elif efficiency > 90:
            recommendations.append("Schedule is very tight - consider buffer time")
        
        return {
            "feasible": feasible,
            "needed_hours": total_hours_needed,
            "available_hours": total_available_hours,
            "efficiency_percentage": round(efficiency, 1),
            "recommendations": recommendations,
            "goals_count": len(goals),
            "time_slots_count": len(available_slots)
        }
