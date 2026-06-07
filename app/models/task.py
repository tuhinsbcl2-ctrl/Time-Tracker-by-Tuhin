from app import db
from datetime import datetime
from enum import Enum

class TaskType(Enum):
    """Predefined task types"""
    REPORT_PREPARATION = 'Report Preparation'
    RETURN_FILING = 'Return Filing'
    CLIENT_COMMUNICATION = 'Client Communication'
    BOOKKEEPING = 'Bookkeeping'
    GST_FILING = 'GST Filing'
    INCOME_TAX_FILING = 'Income Tax Filing'
    AUDIT_WORK = 'Audit Work'
    DATA_ENTRY = 'Data Entry'
    RECONCILIATION = 'Reconciliation'
    INTERNAL_MEETING = 'Internal Meeting'
    CLIENT_MEETING = 'Client Meeting'
    OTHER = 'Other'

class TaskPriority(Enum):
    """Task priority levels"""
    CRITICAL = 'Critical'
    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'

class TaskStatus(Enum):
    """Task status states"""
    PENDING = 'Pending'
    IN_PROGRESS = 'In Progress'
    ON_HOLD = 'On Hold'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'

class TaskRecurrence(Enum):
    """Recurring task frequency"""
    DAILY = 'Daily'
    WEEKLY = 'Weekly'
    MONTHLY = 'Monthly'
    QUARTERLY = 'Quarterly'
    YEARLY = 'Yearly'
    NONE = 'None'

class Task(db.Model):
    """Task model"""
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    task_type = db.Column(db.String(50), nullable=False, default=TaskType.OTHER.value)
    priority = db.Column(db.String(20), nullable=False, default=TaskPriority.MEDIUM.value)
    status = db.Column(db.String(20), nullable=False, default=TaskStatus.PENDING.value)
    deadline = db.Column(db.DateTime, nullable=True)
    recurrence = db.Column(db.String(20), nullable=False, default=TaskRecurrence.NONE.value)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    work_logs = db.relationship('WorkLog', backref='task', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Task {self.title}>'
    
    def mark_completed(self):
        """Mark task as completed"""
        self.status = TaskStatus.COMPLETED.value
        self.completed_at = datetime.utcnow()
        db.session.commit()
    
    def is_overdue(self):
        """Check if task is overdue"""
        if self.deadline and self.status != TaskStatus.COMPLETED.value:
            return datetime.utcnow() > self.deadline
        return False
