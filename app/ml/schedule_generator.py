"""
ML-Powered Schedule Generator

This module implements the core ML feature - generating personalized learning schedules
using the trained recommendation model and optimization algorithms.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, time
from dataclasses import dataclass
import random
import math

logger = logging.getLogger(__name__)

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
class TimeSlot:
    """Represents a time slot for learning."""
    day_of_week: str
    start_time: time
    end_time: time
    duration_minutes: int

class MLScheduleGenerator:
    """
    ML-Powered Learning Schedule Generator
    
    Uses the trained recommendation model to generate personalized schedules
    based on user goals, time availability, and resource difficulty levels.
    """
    
    def __init__(self, recommender):
        self.recommender = recommender
        self.week_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        self.optimal_session_duration = 90  # minutes
        self.break_duration = 15  # minutes between sessions
        
    def generate_schedule(
        self,
        user_id: int,
        goals: List[LearningGoal],
        time_availability: List[Dict[str, Any]],
        start_date: str,
        end_date: str,
        title: str = "ML-Powered Learning Schedule",
        description: str = None
    ) -> Dict[str, Any]:
        """
        Generate a personalized learning schedule using ML.
        
        Args:
            user_id: User ID
            goals: List of learning goals
            time_availability: User's available time slots
            start_date: Schedule start date (YYYY-MM-DD)
            end_date: Schedule end date (YYYY-MM-DD)
            title: Schedule title
            description: Schedule description
            
        Returns:
            Generated schedule with ML-optimized time slots
        """
        try:
            logger.info(f"Generating ML-powered schedule for user {user_id} with {len(goals)} goals")
            
            # Step 1: Calculate total learning time needed
            total_hours_needed = sum(goal.target_hours for goal in goals)
            logger.info(f"Total learning time needed: {total_hours_needed} hours")
            
            # Step 2: Process time availability
            available_slots = self._process_time_availability(time_availability)
            total_available_hours = self._calculate_available_hours(available_slots)
            logger.info(f"Total available time: {total_available_hours} hours")
            
            # Step 3: Generate ML-powered schedule items
            schedule_items = self._generate_ml_schedule_items(
                goals, available_slots, total_hours_needed
            )
            
            # Step 4: Calculate efficiency
            efficiency = (total_hours_needed / total_available_hours * 100) if total_available_hours > 0 else 0
            
            # Step 5: Create final schedule
            schedule = {
                "user_id": user_id,
                "title": title,
                "description": description or f"ML-optimized schedule for {len(goals)} learning goals",
                "start_date": start_date,
                "end_date": end_date,
                "total_hours": total_hours_needed,
                "available_hours": total_available_hours,
                "efficiency": round(efficiency, 1),
                "schedule_items": schedule_items,
                "goals_covered": [goal.goal_title for goal in goals],
                "ml_algorithm": "TF-IDF + Cosine Similarity + Time-blocking Optimization",
                "ml_confidence": self._calculate_ml_confidence(schedule_items),
                "generated_at": datetime.now().isoformat()
            }
            
            logger.info(f"ML schedule generated successfully with {len(schedule_items)} items")
            return schedule
            
        except Exception as e:
            logger.error(f"Error generating ML schedule: {e}")
            raise
    
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
    
    def _generate_ml_schedule_items(
        self,
        goals: List[LearningGoal],
        available_slots: List[TimeSlot],
        total_hours_needed: float
    ) -> List[Dict[str, Any]]:
        """Generate schedule items using ML recommendations."""
        schedule_items = []
        order_index = 0
        
        # Sort goals by difficulty and deadline
        sorted_goals = sorted(goals, key=lambda g: (g.difficulty_level, g.deadline or '9999-12-31'))
        
        for goal in sorted_goals:
            # Use ML model to get recommendations for this goal
            recommendations = self._get_ml_recommendations(goal)
            
            if not recommendations:
                continue
                
            # Calculate time allocation for this goal
            goal_hours = goal.target_hours
            if total_hours_needed > 0:
                goal_hours = (goal.target_hours / total_hours_needed) * total_hours_needed
            
            # Allocate time slots for this goal
            allocated_items = self._allocate_goal_time_ml(
                goal, recommendations, available_slots, goal_hours, order_index
            )
            
            schedule_items.extend(allocated_items)
            order_index += len(allocated_items)
        
        # Sort by day and time
        schedule_items.sort(key=lambda item: (
            self.week_days.index(item['day_of_week'].lower()),
            item['start_time']
        ))
        
        return schedule_items
    
    def _get_ml_recommendations(self, goal: LearningGoal) -> List[Dict[str, Any]]:
        """Get ML recommendations for a specific goal."""
        try:
            # Use the trained ML model to get recommendations
            recommendations = self.recommender.get_recommendations(
                topic=goal.goal_title,
                top_k=5
            )
            
            # Convert to schedule-friendly format
            ml_resources = []
            for rec in recommendations:
                ml_resources.append({
                    'title': rec['title'],
                    'type': rec['type'],
                    'url': rec['url'],
                    'confidence': rec['confidence'],
                    'difficulty_level': self._estimate_difficulty(rec, goal.difficulty_level),
                    'estimated_hours': self._estimate_duration(rec, goal.target_hours)
                })
            
            return ml_resources
            
        except Exception as e:
            logger.warning(f"Error getting ML recommendations for goal {goal.goal_title}: {e}")
            return []
    
    def _estimate_difficulty(self, recommendation: Dict[str, Any], goal_difficulty: int) -> int:
        """Estimate difficulty level based on ML confidence and goal difficulty."""
        confidence = recommendation.get('confidence', 0.5)
        
        # Higher confidence = closer to goal difficulty
        if confidence > 0.8:
            return goal_difficulty
        elif confidence > 0.6:
            return max(1, goal_difficulty - 1)
        else:
            return max(1, goal_difficulty - 2)
    
    def _estimate_duration(self, recommendation: Dict[str, Any], target_hours: int) -> float:
        """Estimate duration based on resource type and target hours."""
        resource_type = recommendation.get('type', 'video')
        confidence = recommendation.get('confidence', 0.5)
        
        # Base duration by type
        base_duration = {
            'video': 2.0,
            'article': 1.0,
            'course': 4.0,
            'book': 3.0
        }.get(resource_type, 2.0)
        
        # Adjust based on confidence and target hours
        duration = base_duration * (0.5 + confidence)
        
        # Ensure it fits within target hours
        return min(duration, target_hours * 0.5)
    
    def _allocate_goal_time_ml(
        self,
        goal: LearningGoal,
        recommendations: List[Dict[str, Any]],
        available_slots: List[TimeSlot],
        target_hours: float,
        start_order_index: int
    ) -> List[Dict[str, Any]]:
        """Allocate time for a goal using ML recommendations."""
        items = []
        remaining_hours = target_hours
        order_index = start_order_index
        
        # Sort recommendations by confidence (highest first)
        sorted_recs = sorted(recommendations, key=lambda r: r['confidence'], reverse=True)
        
        for slot in available_slots:
            if remaining_hours <= 0:
                break
                
            # Find best recommendation for this time slot
            best_rec = self._select_best_recommendation(
                sorted_recs, slot.duration_minutes / 60.0, goal.difficulty_level
            )
            
            if not best_rec:
                continue
                
            # Calculate session duration
            session_hours = min(
                slot.duration_minutes / 60.0,
                self.optimal_session_duration / 60.0,
                remaining_hours,
                best_rec['estimated_hours']
            )
            
            if session_hours <= 0:
                continue
                
            # Calculate end time
            session_duration = int(session_hours * 60)
            end_time = self._add_minutes_to_time(slot.start_time, session_duration)
            
            # Ensure we don't exceed slot end time
            if end_time > slot.end_time:
                end_time = slot.end_time
                session_duration = self._time_difference_minutes(slot.start_time, end_time)
                session_hours = session_duration / 60.0
            
            if session_hours > 0:
                items.append({
                    'resource_id': order_index + 1,  # Simple ID
                    'resource_title': best_rec['title'],
                    'resource_type': best_rec['type'],
                    'day_of_week': slot.day_of_week,
                    'start_time': slot.start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'estimated_hours': session_hours,
                    'difficulty_level': best_rec['difficulty_level'],
                    'ml_confidence': best_rec['confidence'],
                    'order_index': order_index
                })
                
                remaining_hours -= session_hours
                order_index += 1
                
                # Remove used recommendation to avoid repetition
                if best_rec in sorted_recs:
                    sorted_recs.remove(best_rec)
        
        return items
    
    def _select_best_recommendation(
        self,
        recommendations: List[Dict[str, Any]],
        available_hours: float,
        goal_difficulty: int
    ) -> Optional[Dict[str, Any]]:
        """Select the best recommendation for a time slot."""
        if not recommendations:
            return None
            
        # Filter recommendations that fit the time constraint
        suitable_recs = [
            r for r in recommendations
            if r['estimated_hours'] <= available_hours * 1.5  # Allow some flexibility
        ]
        
        if not suitable_recs:
            # If no recommendations fit, take the shortest one
            suitable_recs = [min(recommendations, key=lambda r: r['estimated_hours'])]
        
        # Select based on confidence and difficulty match
        best_rec = max(suitable_recs, key=lambda r: (
            r['confidence'],
            -abs(r['difficulty_level'] - goal_difficulty)
        ))
        
        return best_rec
    
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
    
    def _calculate_ml_confidence(self, schedule_items: List[Dict[str, Any]]) -> float:
        """Calculate overall ML confidence for the schedule."""
        if not schedule_items:
            return 0.0
            
        confidences = [item.get('ml_confidence', 0.5) for item in schedule_items]
        return round(sum(confidences) / len(confidences), 3)
    
    def _distribute_sessions_weekly(
        self, 
        sessions: List[Dict[str, Any]], 
        available_slots: List[TimeSlot], 
        youtube_url: str
    ) -> List[Dict[str, Any]]:
        """
        Create a realistic, human-friendly weekly learning schedule.
        - Max 3-4 hours per day (realistic study limit)
        - Proper break times between sessions
        - Specific time slots with start/end times
        - Distributes across multiple days intelligently
        """
        schedule_items = []
        
        # Realistic study parameters
        MAX_DAILY_HOURS = 3.5  # Maximum study hours per day
        SESSION_DURATION = 1.5  # Optimal session duration (1.5 hours)
        BREAK_DURATION = 30     # Break between sessions (30 minutes)
        
        # Group available slots by day
        daily_slots = {}
        for slot in available_slots:
            if slot.day_of_week not in daily_slots:
                daily_slots[slot.day_of_week] = []
            daily_slots[slot.day_of_week].append(slot)
        
        # Sort days in order (weekdays first, then weekends)
        weekday_order = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        weekend_order = ['saturday', 'sunday']
        sorted_days = [day for day in weekday_order if day in daily_slots] + [day for day in weekend_order if day in daily_slots]
        
        if not sorted_days:
            logger.warning("No available time slots found")
            return []
        
        # Break down sessions into realistic chunks
        realistic_sessions = self._create_realistic_sessions(sessions, SESSION_DURATION)
        
        # Track daily study hours
        daily_study_hours = {day: 0.0 for day in sorted_days}
        
        # Distribute sessions across days
        session_index = 0
        day_index = 0
        
        while session_index < len(realistic_sessions) and day_index < len(sorted_days) * 2:  # Allow cycling through days
            current_day = sorted_days[day_index % len(sorted_days)]
            day_slots = daily_slots[current_day]
            
            # Check if we can add more study time to this day
            if daily_study_hours[current_day] >= MAX_DAILY_HOURS:
                day_index += 1
                continue
            
            # Find a suitable time slot for this day
            session_placed = False
            for slot in day_slots:
                if daily_study_hours[current_day] >= MAX_DAILY_HOURS:
                    break
                    
                # Calculate available time in this slot
                remaining_slot_hours = self._time_difference_minutes(slot.start_time, slot.end_time) / 60.0
                remaining_daily_hours = MAX_DAILY_HOURS - daily_study_hours[current_day]
                
                # Determine session duration
                session_hours = min(
                    realistic_sessions[session_index]["duration_hours"],
                    remaining_slot_hours,
                    remaining_daily_hours
                )
                
                if session_hours >= 0.5:  # Minimum 30 minutes
                    # Calculate specific timing
                    session_duration_minutes = int(session_hours * 60)
                    end_time = self._add_minutes_to_time(slot.start_time, session_duration_minutes)
                    
                    # Ensure we don't exceed slot time
                    if end_time <= slot.end_time:
                        # Create session with specific timing and meaningful topic
                        session = realistic_sessions[session_index]
                        session_item = {
                            "resource_id": session_index + 1,
                            "resource_title": session.get("title", f"Learning Session {session['session_number']}"),
                            "learning_topic": session.get("learning_topic", f"Part {session['session_number']} of the course"),
                            "learning_objectives": session.get("learning_objectives", ["Continue learning from the video"]),
                            "key_concepts": session.get("key_concepts", ["Video content"]),
                            "resource_type": "video",
                            "day_of_week": current_day,
                            "start_time": slot.start_time.strftime("%H:%M"),
                            "end_time": end_time.strftime("%H:%M"),
                            "estimated_hours": session_hours,
                            "difficulty_level": 1,
                            "video_url": youtube_url,
                            "video_id": session.get("video_id", ""),
                            "session_number": session["session_number"],
                            "video_title": session["video_title"],
                            "video_description": session["video_description"],
                            "order_index": session_index,
                            "break_after": min(BREAK_DURATION, 15) if session_index < len(realistic_sessions) - 1 else 0
                        }
                        
                        schedule_items.append(session_item)
                        
                        # Update tracking
                        daily_study_hours[current_day] += session_hours
                        slot.start_time = self._add_minutes_to_time(end_time, BREAK_DURATION)  # Add break time
                        
                        session_index += 1
                        session_placed = True
                        
                        logger.info(f"Placed session {session_index} on {current_day}: {slot.start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')} ({session_hours:.1f}h)")
                        break
            
            if not session_placed:
                day_index += 1
        
        # Log distribution summary
        used_days = [day for day, hours in daily_study_hours.items() if hours > 0]
        logger.info(f"Distributed {len(schedule_items)} sessions across {len(used_days)} days")
        for day in used_days:
            logger.info(f"  {day}: {daily_study_hours[day]:.1f} hours")
        
        return schedule_items
    
    def _create_realistic_sessions(self, sessions: List[Dict[str, Any]], target_duration: float) -> List[Dict[str, Any]]:
        """Break down sessions into realistic 1.5-hour chunks with proper breaks."""
        realistic_sessions = []
        
        for session in sessions:
            original_duration = session["duration_hours"]
            
            if original_duration <= target_duration:
                # Session is already realistic size
                realistic_sessions.append(session)
            else:
                # Break down into smaller chunks
                remaining_duration = original_duration
                sub_session_num = 1
                
                while remaining_duration > 0:
                    chunk_duration = min(remaining_duration, target_duration)
                    
                    realistic_sessions.append({
                        **session,
                        "duration_hours": chunk_duration,
                        "title": f"{session['title']} - Part {sub_session_num}",
                        "session_number": f"{session['session_number']}.{sub_session_num}"
                    })
                    
                    remaining_duration -= chunk_duration
                    sub_session_num += 1
        
        return realistic_sessions

    def generate_youtube_schedule(
        self,
        youtube_url: str,
        duration_hours: float,
        time_availability: List[Dict[str, Any]],
        title: str = "YouTube Learning Schedule"
    ) -> Dict[str, Any]:
        """Generate schedule specifically for YouTube videos - simple and effective."""
        try:
            from app.services.youtube_service import YouTubeService
            
            logger.info(f"Generating YouTube schedule for: {youtube_url}, Duration: {duration_hours}h")
            
            # Initialize YouTube service
            youtube_service = YouTubeService()
            
            # Create learning sessions from video
            sessions = youtube_service.create_learning_sessions(youtube_url, duration_hours)
            
            # Process time availability
            available_slots = self._process_time_availability(time_availability)
            
            # Distribute sessions across multiple days for proper weekly timetable
            schedule_items = self._distribute_sessions_weekly(sessions, available_slots, youtube_url)
            
            # Calculate efficiency
            total_hours = sum(item["estimated_hours"] for item in schedule_items)
            available_hours = self._calculate_available_hours(available_slots)
            efficiency = (total_hours / available_hours * 100) if available_hours > 0 else 0
            
            logger.info(f"YouTube schedule generated: {len(schedule_items)} sessions, {total_hours}h total")
            
            # Group by day for better visualization
            daily_schedule = {}
            for item in schedule_items:
                day = item["day_of_week"]
                if day not in daily_schedule:
                    daily_schedule[day] = []
                daily_schedule[day].append(item)
            
            return {
                "title": title,
                "description": f"YouTube video learning schedule - {len(sessions)} sessions across {len(daily_schedule)} days",
                "total_hours": total_hours,
                "available_hours": available_hours,
                "efficiency": round(efficiency, 1),
                "schedule_items": schedule_items,
                "daily_schedule": daily_schedule,
                "video_info": {
                    "url": youtube_url,
                    "sessions_count": len(sessions),
                    "original_duration": duration_hours,
                    "video_id": sessions[0]["video_id"] if sessions else "unknown",
                    "days_used": len(daily_schedule)
                },
                "ml_algorithm": "YouTube Video Processing + Weekly Time Distribution",
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating YouTube schedule: {e}")
            raise
