from app import db
from datetime import datetime

class Timer(db.Model):
    """Timer model for tracking active timers"""
    __tablename__ = 'timers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    started_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    stopped_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Timer user_id={self.user_id} task_id={self.task_id} active={self.is_active}>'
    
    def stop(self):
        """Stop the timer"""
        self.stopped_at = datetime.utcnow()
        self.is_active = False
        db.session.commit()
    
    def get_duration(self):
        """Get timer duration in seconds"""
        end_time = self.stopped_at if self.stopped_at else datetime.utcnow()
        duration = end_time - self.started_at
        return int(duration.total_seconds())
    
    def get_duration_formatted(self):
        """Get formatted duration (HH:MM:SS)"""
        seconds = self.get_duration()
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f'{hours:02d}:{minutes:02d}:{secs:02d}'

class WorkLog(db.Model):
    """Work log model for storing completed time entries"""
    __tablename__ = 'work_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    remarks = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    modified_at = db.Column(db.DateTime, nullable=True)
    was_auto_cutoff = db.Column(db.Boolean, default=False)
    cutoff_reason = db.Column(db.String(255), nullable=True)
    
    def __repr__(self):
        return f'<WorkLog user_id={self.user_id} task_id={self.task_id} date={self.date}>'
    
    def get_duration_formatted(self):
        """Get formatted duration (HH:MM)"""
        hours = self.duration_minutes // 60
        minutes = self.duration_minutes % 60
        return f'{hours}h {minutes}m'
    
    def get_duration_hours(self):
        """Get duration in decimal hours"""
        return round(self.duration_minutes / 60, 2)
