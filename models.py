"""
Database models for MoneyWise - Personal Finance Tracker
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import func

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and profile management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    currency = db.Column(db.String(3), default='USD')  # USD, EUR, INR, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    categories = db.relationship('Category', backref='user', lazy=True, cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', backref='user', lazy=True, cascade='all, delete-orphan')
    budgets = db.relationship('Budget', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify the user's password"""
        return check_password_hash(self.password_hash, password)
    
    def get_total_income(self, month=None, year=None):
        """Calculate total income for a specific month/year or all time"""
        query = Transaction.query.filter_by(user_id=self.id, type='income')
        
        if month and year:
            query = query.filter(
                func.extract('month', Transaction.date) == month,
                func.extract('year', Transaction.date) == year
            )
        
        total = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == self.id,
            Transaction.type == 'income'
        )
        
        if month and year:
            total = total.filter(
                func.extract('month', Transaction.date) == month,
                func.extract('year', Transaction.date) == year
            )
        
        result = total.scalar()
        return float(result) if result else 0.0
    
    def get_total_expenses(self, month=None, year=None):
        """Calculate total expenses for a specific month/year or all time"""
        total = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == self.id,
            Transaction.type == 'expense'
        )
        
        if month and year:
            total = total.filter(
                func.extract('month', Transaction.date) == month,
                func.extract('year', Transaction.date) == year
            )
        
        result = total.scalar()
        return float(result) if result else 0.0
    
    def get_balance(self):
        """Calculate current balance (total income - total expenses)"""
        return self.get_total_income() - self.get_total_expenses()
    
    def __repr__(self):
        return f'<User {self.username}>'


class Category(db.Model):
    """Category model for organizing transactions"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    color = db.Column(db.String(7), default='#6366F1')  # Hex color code
    icon = db.Column(db.String(50), default='💰')  # Emoji or icon class
    is_default = db.Column(db.Boolean, default=False)  # System-created categories
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    transactions = db.relationship('Transaction', backref='category', lazy=True)
    budgets = db.relationship('Budget', backref='category', lazy=True)
    
    def get_total_spent(self, month=None, year=None):
        """Get total amount spent in this category for a given period"""
        query = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.category_id == self.id
        )
        
        if month and year:
            query = query.filter(
                func.extract('month', Transaction.date) == month,
                func.extract('year', Transaction.date) == year
            )
        
        result = query.scalar()
        return float(result) if result else 0.0
    
    def __repr__(self):
        return f'<Category {self.name} ({self.type})>'


class Transaction(db.Model):
    """Transaction model for income and expense records"""
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)  # Up to 99,999,999.99
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    description = db.Column(db.String(200))
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow, index=True)
    is_recurring = db.Column(db.Boolean, default=False)
    recurring_frequency = db.Column(db.String(20))  # 'daily', 'weekly', 'monthly', 'yearly'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Transaction {self.type} {self.amount} - {self.description}>'


class Budget(db.Model):
    """Budget model for setting spending limits per category"""
    __tablename__ = 'budgets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    month = db.Column(db.Date, nullable=False, index=True)  # First day of the month
    alert_threshold = db.Column(db.Integer, default=80)  # Alert at 80% by default
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_spent_amount(self):
        """Get amount spent in this category for the budget month"""
        month = self.month.month
        year = self.month.year
        
        result = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.category_id == self.category_id,
            Transaction.user_id == self.user_id,
            func.extract('month', Transaction.date) == month,
            func.extract('year', Transaction.date) == year
        ).scalar()
        
        return float(result) if result else 0.0
    
    def get_percentage_used(self):
        """Calculate what percentage of the budget has been used"""
        spent = self.get_spent_amount()
        if float(self.amount) == 0:
            return 0
        return (spent / float(self.amount)) * 100
    
    def get_remaining(self):
        """Get remaining budget amount"""
        return float(self.amount) - self.get_spent_amount()
    
    def get_status(self):
        """Get budget status (on_track, warning, alert, exceeded)"""
        percentage = self.get_percentage_used()
        
        if percentage >= 100:
            return 'exceeded'
        elif percentage >= 90:
            return 'alert'
        elif percentage >= self.alert_threshold:
            return 'warning'
        else:
            return 'on_track'
    
    def __repr__(self):
        return f'<Budget {self.category.name} - {self.amount} for {self.month}>'


def create_default_categories(user_id):
    """Create default categories for a new user"""
    
    income_categories = [
        {'name': 'Salary', 'icon': '💼', 'color': '#10B981'},
        {'name': 'Freelance', 'icon': '💰', 'color': '#34D399'},
        {'name': 'Investments', 'icon': '📈', 'color': '#059669'},
        {'name': 'Gifts', 'icon': '🎁', 'color': '#6EE7B7'},
        {'name': 'Other Income', 'icon': '💵', 'color': '#A7F3D0'},
    ]
    
    expense_categories = [
        {'name': 'Food & Dining', 'icon': '🍔', 'color': '#EF4444'},
        {'name': 'Transportation', 'icon': '🚗', 'color': '#F87171'},
        {'name': 'Housing/Rent', 'icon': '🏠', 'color': '#DC2626'},
        {'name': 'Utilities', 'icon': '⚡', 'color': '#B91C1C'},
        {'name': 'Groceries', 'icon': '🛒', 'color': '#991B1B'},
        {'name': 'Entertainment', 'icon': '🎬', 'color': '#F59E0B'},
        {'name': 'Shopping', 'icon': '🛍️', 'color': '#FBBF24'},
        {'name': 'Healthcare', 'icon': '💊', 'color': '#F59E0B'},
        {'name': 'Education', 'icon': '📚', 'color': '#D97706'},
        {'name': 'Bills & Subscriptions', 'icon': '💳', 'color': '#B45309'},
        {'name': 'Travel', 'icon': '✈️', 'color': '#6366F1'},
        {'name': 'Fitness', 'icon': '💪', 'color': '#8B5CF6'},
        {'name': 'Personal Care', 'icon': '💄', 'color': '#EC4899'},
        {'name': 'Gifts & Donations', 'icon': '🎁', 'color': '#F472B6'},
        {'name': 'Other Expenses', 'icon': '📁', 'color': '#94A3B8'},
    ]
    
    categories = []
    
    # Create income categories
    for cat_data in income_categories:
        category = Category(
            user_id=user_id,
            name=cat_data['name'],
            type='income',
            icon=cat_data['icon'],
            color=cat_data['color'],
            is_default=True
        )
        categories.append(category)
    
    # Create expense categories
    for cat_data in expense_categories:
        category = Category(
            user_id=user_id,
            name=cat_data['name'],
            type='expense',
            icon=cat_data['icon'],
            color=cat_data['color'],
            is_default=True
        )
        categories.append(category)
    
    # Add all categories to the database
    db.session.add_all(categories)
    db.session.commit()
    
    return categories