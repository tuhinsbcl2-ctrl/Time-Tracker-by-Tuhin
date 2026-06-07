from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from enum import Enum

class Role(Enum):
    """User roles"""
    MANAGER = 'Manager'
    EMPLOYEE = 'Employee'

class User(UserMixin, db.Model):
    """User model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False, default=Role.EMPLOYEE.value)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    employees = db.relationship('User', backref=db.backref('manager', remote_side=[id]), lazy='dynamic')
    tasks = db.relationship('Task', backref='creator', lazy='dynamic', foreign_keys='Task.created_by')
    assigned_tasks = db.relationship('Task', backref='assigned_employee', lazy='dynamic', foreign_keys='Task.assigned_to')
    timers = db.relationship('Timer', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    work_logs = db.relationship('WorkLog', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    @property
    def full_name(self):
        """Return full name"""
        return f'{self.first_name} {self.last_name}'
    
    def is_manager(self):
        """Check if user is manager"""
        return self.role == Role.MANAGER.value
    
    def get_employees(self):
        """Get all employees under this manager"""
        if self.is_manager():
            return self.employees.all()
        return []
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))
