"""
Flask-WTF forms with CSRF protection and validation
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SelectField, \
    TextAreaField, DecimalField, DateField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, \
    NumberRange, ValidationError, Optional
from models import User, Category
from datetime import date


class SignupForm(FlaskForm):
    """User registration form"""
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80, message='Username must be 3-80 characters')
    ])
    email = EmailField('Email', validators=[
        DataRequired(),
        Email(message='Invalid email address'),
        Length(max=120)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    currency = SelectField('Currency', choices=[
        ('USD', 'USD - US Dollar ($)'),
        ('EUR', 'EUR - Euro (€)'),
        ('GBP', 'GBP - British Pound (£)'),
        ('INR', 'INR - Indian Rupee (₹)'),
        ('JPY', 'JPY - Japanese Yen (¥)'),
        ('AUD', 'AUD - Australian Dollar (A$)'),
        ('CAD', 'CAD - Canadian Dollar (C$)')
    ], default='INR')
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered')


class LoginForm(FlaskForm):
    """User login form"""
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80)
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    remember_me = BooleanField('Remember Me')


class TransactionForm(FlaskForm):
    """Transaction form"""
    transaction_type = SelectField('Type', choices=[
        ('income', 'Income'),
        ('expense', 'Expense')
    ], validators=[DataRequired()])
    
    category_id = SelectField('Category', coerce=int, validators=[
        DataRequired()
    ])
    
    amount = DecimalField('Amount', validators=[
        DataRequired(),
        NumberRange(min=0.01, message='Amount must be greater than 0')
    ], places=2)
    
    date = DateField('Date', validators=[DataRequired()], default=date.today)
    
    description = TextAreaField('Description', validators=[
        Optional(),
        Length(max=200)
    ])
    
    is_recurring = BooleanField('Recurring Transaction')
    
    recurring_frequency = SelectField('Frequency', choices=[
        ('', 'Select frequency'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')
    ], validators=[Optional()])


class CategoryForm(FlaskForm):
    """Category form"""
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=1, max=50, message='Name must be 1-50 characters')
    ])
    
    category_type = SelectField('Type', choices=[
        ('income', 'Income'),
        ('expense', 'Expense')
    ], validators=[DataRequired()])
    
    icon = StringField('Icon', validators=[
        DataRequired(),
        Length(max=5)
    ])
    
    color = StringField('Color', validators=[
        DataRequired(),
        Length(min=7, max=7, message='Must be a valid hex color')
    ], default='#6366F1')


class BudgetForm(FlaskForm):
    """Budget form"""
    category_id = SelectField('Category', coerce=int, validators=[
        DataRequired()
    ])
    
    amount = DecimalField('Budget Amount', validators=[
        DataRequired(),
        NumberRange(min=0.01, message='Amount must be greater than 0')
    ], places=2)
    
    alert_threshold = IntegerField('Alert Threshold (%)', validators=[
        DataRequired(),
        NumberRange(min=1, max=100, message='Threshold must be 1-100')
    ], default=80)


class ProfileForm(FlaskForm):
    """Profile update form"""
    email = EmailField('Email', validators=[
        DataRequired(),
        Email(message='Invalid email address'),
        Length(max=120)
    ])
    
    currency = SelectField('Currency', choices=[
        ('USD', 'USD - US Dollar ($)'),
        ('EUR', 'EUR - Euro (€)'),
        ('GBP', 'GBP - British Pound (£)'),
        ('INR', 'INR - Indian Rupee (₹)'),
        ('JPY', 'JPY - Japanese Yen (¥)'),
        ('AUD', 'AUD - Australian Dollar (A$)'),
        ('CAD', 'CAD - Canadian Dollar (C$)')
    ])


class ChangePasswordForm(FlaskForm):
    """Change password form"""
    current_password = PasswordField('Current Password', validators=[
        DataRequired()
    ])
    
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters')
    ])
    
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])