from app import db
from datetime import datetime
from enum import Enum

class NotificationType(Enum):
    """Notification types"""
    TASK_ASSIGNED = 'Task Assigned'
    DEADLINE_REMINDER = 'Deadline Reminder'
    OVERDUE_ALERT = 'Overdue Alert'
    WORK_HOUR_WARNING = 'Work Hour Warning'
    TIMER_CUTOFF = 'Timer Cutoff'
    RECURRING_TASK = 'Recurring Task'

class Notification(db.Model):
    """Notification model"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    related_task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Notification {self.notification_type} for user_id={self.user_id}>'
    
    def mark_as_read(self):
        """Mark notification as read"""
        self.is_read = True
        db.session.commit()
