"""
MoneyWise - Personal Finance Tracker
Main Flask Application
"""

import os
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Category, Transaction, Budget, create_default_categories
from datetime import datetime, date
from sqlalchemy import func, extract
import calendar

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database configuration
database_url = os.environ.get('DATABASE_URL', 'sqlite:///moneywise.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Create tables
with app.app_context():
    db.create_all()


# ==================== ROUTES ====================

# Home/Landing Page
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


# Authentication Routes
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        currency = request.form.get('currency', 'USD')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required!', 'danger')
            return redirect(url_for('signup'))
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('signup'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('signup'))
        
        # Create new user
        user = User(username=username, email=email, currency=currency)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Create default categories for the user
        create_default_categories(user.id)
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(next_page if next_page else url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    # Get current month and year
    today = date.today()
    current_month = today.month
    current_year = today.year
    
    # Calculate statistics
    total_income = current_user.get_total_income(current_month, current_year)
    total_expenses = current_user.get_total_expenses(current_month, current_year)
    balance = total_income - total_expenses
    
    # Get recent transactions (last 10)
    recent_transactions = Transaction.query.filter_by(user_id=current_user.id)\
        .order_by(Transaction.date.desc(), Transaction.created_at.desc())\
        .limit(10).all()
    
    # Get expense breakdown by category for current month
    category_breakdown = db.session.query(
        Category.name,
        Category.icon,
        Category.color,
        func.sum(Transaction.amount).label('total')
    ).join(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == 'expense',
        extract('month', Transaction.date) == current_month,
        extract('year', Transaction.date) == current_year
    ).group_by(Category.id).all()
    
    return render_template('dashboard.html',
                         total_income=total_income,
                         total_expenses=total_expenses,
                         balance=balance,
                         recent_transactions=recent_transactions,
                         category_breakdown=category_breakdown,
                         month_name=calendar.month_name[current_month],
                         year=current_year)


# Transactions
@app.route('/transactions')
@login_required
def transactions():
    # Get filter parameters
    category_filter = request.args.get('category', type=int)
    type_filter = request.args.get('type')
    month_filter = request.args.get('month', type=int)
    year_filter = request.args.get('year', type=int)
    
    # Base query
    query = Transaction.query.filter_by(user_id=current_user.id)
    
    # Apply filters
    if category_filter:
        query = query.filter_by(category_id=category_filter)
    if type_filter:
        query = query.filter_by(type=type_filter)
    if month_filter and year_filter:
        query = query.filter(
            extract('month', Transaction.date) == month_filter,
            extract('year', Transaction.date) == year_filter
        )
    
    # Order by date (newest first)
    transactions_list = query.order_by(Transaction.date.desc()).all()
    
    # Get categories for filter dropdown
    categories = Category.query.filter_by(user_id=current_user.id).all()
    
    return render_template('transactions.html',
                         transactions=transactions_list,
                         categories=categories)


@app.route('/transactions/add', methods=['POST'])
@login_required
def add_transaction():
    try:
        amount = float(request.form.get('amount'))
        category_id = int(request.form.get('category_id'))
        trans_type = request.form.get('type')
        description = request.form.get('description', '')
        trans_date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        
        # Validate category belongs to user
        category = Category.query.filter_by(id=category_id, user_id=current_user.id).first()
        if not category:
            flash('Invalid category!', 'danger')
            return redirect(url_for('transactions'))
        
        # Create transaction
        transaction = Transaction(
            user_id=current_user.id,
            category_id=category_id,
            amount=amount,
            type=trans_type,
            description=description,
            date=trans_date
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        flash('Transaction added successfully!', 'success')
        
    except Exception as e:
        flash(f'Error adding transaction: {str(e)}', 'danger')
    
    return redirect(url_for('transactions'))


@app.route('/transactions/delete/<int:id>', methods=['POST'])
@login_required
def delete_transaction(id):
    transaction = Transaction.query.filter_by(id=id, user_id=current_user.id).first()
    
    if transaction:
        db.session.delete(transaction)
        db.session.commit()
        flash('Transaction deleted successfully!', 'success')
    else:
        flash('Transaction not found!', 'danger')
    
    return redirect(url_for('transactions'))


# Categories
@app.route('/categories')
@login_required
def categories():
    income_categories = Category.query.filter_by(user_id=current_user.id, type='income').all()
    expense_categories = Category.query.filter_by(user_id=current_user.id, type='expense').all()
    
    return render_template('categories.html',
                         income_categories=income_categories,
                         expense_categories=expense_categories)


# Budgets
# AFTER (accepts both GET and POST):
@app.route('/budgets', methods=['GET', 'POST'])
@login_required
def budgets():
    if request.method == 'POST':
        # Handle budget creation
        category_id = request.form.get('category_id')
        amount = request.form.get('amount')
        alert_threshold = request.form.get('alert_threshold', 80)
        
        # Create new budget
        from datetime import date
        current_month = date.today().replace(day=1)
        
        new_budget = Budget(
            user_id=current_user.id,
            category_id=category_id,
            amount=amount,
            month=current_month,
            alert_threshold=alert_threshold
        )
        
        db.session.add(new_budget)
        db.session.commit()
        
        flash('Budget created successfully!', 'success')
        return redirect(url_for('budgets'))
    
    # GET request - display budgets
    from datetime import date
    current_month = date.today().replace(day=1)
    
    budgets = Budget.query.filter_by(
        user_id=current_user.id,
        month=current_month
    ).all()
    
    # Get expense categories for the dropdown
    categories = Category.query.filter_by(
        user_id=current_user.id,
        type='expense'
    ).all()
    
    return render_template(
        'budgets.html',
        budgets=budgets,
        categories=categories,
        month_name=current_month.strftime('%B'),
        year=current_month.year
    )































# Profile
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


# API Endpoints for Charts
@app.route('/api/expense-breakdown')
@login_required
def api_expense_breakdown():
    """Get expense breakdown by category for current month"""
    today = date.today()
    
    breakdown = db.session.query(
        Category.name,
        Category.color,
        func.sum(Transaction.amount).label('total')
    ).join(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == 'expense',
        extract('month', Transaction.date) == today.month,
        extract('year', Transaction.date) == today.year
    ).group_by(Category.id).all()
    
    data = {
        'labels': [item.name for item in breakdown],
        'amounts': [float(item.total) for item in breakdown],
        'colors': [item.color for item in breakdown]
    }
    
    return jsonify(data)


@app.route('/api/income-expense-trend')
@login_required
def api_income_expense_trend():
    """Get income vs expense trend for last 6 months"""
    today = date.today()
    
    # This is a simplified version - you can expand this
    data = {
        'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'income': [5000, 5200, 5100, 5300, 5400, 5500],
        'expenses': [4000, 3800, 4200, 4100, 4300, 4000]
    }
    
    return jsonify(data)


# Error handlers
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)