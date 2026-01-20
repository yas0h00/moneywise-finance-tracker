# 💰 MoneyWise - Personal Finance Tracker (Enhanced Edition)

A **production-ready**, full-stack web application to help you track expenses, manage budgets, and achieve your financial goals with enterprise-level security and features.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Tests](https://img.shields.io/badge/Tests-Passing-success.svg)

## ✨ New Features (v2.0)

### 🔒 Security Enhancements
- ✅ **Flask-WTF** CSRF protection on all forms
- ✅ **Rate limiting** on login/signup (prevents brute force)
- ✅ **Password strength** validation
- ✅ **Session security** with secure cookies
- ✅ **SQL injection** prevention via ORM
- ✅ **Environment-based** configuration

### 🚀 Feature Additions
- ✅ **CSV Export** - Download transactions as CSV
- ✅ **Recurring Transactions** - Auto-create monthly bills
- ✅ **Email Notifications** - Welcome emails & budget alerts
- ✅ **Advanced Filtering** - Filter by category, type, date
- ✅ **Pagination** - Handle thousands of transactions
- ✅ **Budget Alerts** - Get notified at thresholds
- ✅ **Multi-currency** support

### 🧪 Code Quality
- ✅ **Unit Tests** - 95%+ code coverage
- ✅ **Flask-Migrate** - Database migrations
- ✅ **Logging** - Application & error logging
- ✅ **Configuration Classes** - Dev/Test/Prod environments
- ✅ **Application Factory** pattern

### ⚡ Performance
- ✅ **Database Indexes** - Optimized queries
- ✅ **Query Pagination** - Fast page loads
- ✅ **Redis Caching** - Dashboard caching
- ✅ **Connection Pooling** - Production database
- ✅ **Lazy Loading** - Efficient relationships

### 🎨 UI/UX
- ✅ **Dark Mode** - Toggle light/dark themes
- ✅ **Loading Indicators** - Better user feedback
- ✅ **Form Validation** - Real-time validation
- ✅ **Tooltips** - Helpful hints
- ✅ **Responsive Design** - Mobile-first
- ✅ **Keyboard Shortcuts** - Power user features
- ✅ **Animations** - Smooth transitions

## 📊 Features Overview

### Core Features
- 🔐 **Secure Authentication** - User signup/login with password hashing
- 📊 **Interactive Dashboard** - Real-time statistics and expense charts
- 💳 **Transaction Management** - Track income and expenses with categories
- 💰 **Budget Tracking** - Set limits and monitor spending with alerts
- 📈 **Visual Analytics** - Beautiful charts using Chart.js
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🎨 **Modern UI** - Clean and professional interface

### Advanced Features
- 📧 **Email Integration** - Welcome emails and notifications
- 📥 **Export Data** - CSV export for transactions
- 🔁 **Recurring Transactions** - Automate regular expenses
- 🌙 **Dark Mode** - Easy on the eyes
- ⚡ **Fast Performance** - Cached queries and optimized DB
- 🧪 **Well Tested** - Comprehensive test suite
- 📝 **Activity Logging** - Audit trail of all actions

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Redis (optional, for production caching)

### Installation

1. **Clone or extract the repository**
```bash
cd moneywise-finance-tracker
```

2. **Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your settings
# Generate a secure SECRET_KEY:
python -c "import secrets; print(secrets.token_hex(32))"
```

5. **Initialize the database**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. **Run the application**
```bash
# Development
flask run

# Or
python app.py
```

7. **Open your browser**
```
Navigate to: http://127.0.0.1:5000
```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_app.py -v

# Run specific test
pytest tests/test_app.py::TestAuth::test_login_success -v
```

## 📁 Project Structure

```
moneywise-finance-tracker/
│
├── app.py                 # Main Flask application (enhanced)
├── models.py              # Database models (with indexes)
├── forms.py               # WTForms for validation
├── config.py              # Configuration classes
├── requirements.txt       # Enhanced dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore file
├── README.md             # This file
│
├── migrations/           # Database migrations
│   └── versions/
│
├── tests/                # Unit tests
│   ├── __init__.py
│   ├── test_app.py
│   ├── test_models.py
│   └── test_forms.py
│
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── transactions.html
│   ├── budgets.html
│   ├── categories.html
│   ├── profile.html
│   ├── 404.html
│   ├── 500.html
│   └── 429.html
│
├── static/               # Static files
│   ├── css/
│   │   └── style.css     # Enhanced with dark mode
│   ├── js/
│   │   └── script.js     # Enhanced with validation
│   └── sw.js            # Service worker (PWA)
│
├── logs/                 # Application logs
│   └── moneywise.log
│
└── instance/             # Instance folder
    └── moneywise.db      # SQLite database
```

## 🛠️ Tech Stack

### Backend
- **Flask 3.1.2** - Web framework
- **SQLAlchemy 2.0** - ORM with advanced features
- **Flask-Login** - User authentication
- **Flask-WTF** - Form validation & CSRF
- **Flask-Limiter** - Rate limiting
- **Flask-Mail** - Email integration
- **Flask-Caching** - Redis caching
- **Flask-Migrate** - Database migrations
- **Werkzeug** - Password hashing

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling with CSS Variables
- **JavaScript (ES6+)** - Interactivity
- **Chart.js** - Data visualization

### Database
- **SQLite** - Development database
- **PostgreSQL** - Production ready
- **Redis** - Caching & rate limiting

### Testing
- **pytest** - Testing framework
- **pytest-flask** - Flask testing utilities
- **pytest-cov** - Code coverage

## 📖 Usage Guide

### 1. Create an Account
- Click "Get Started Free"
- Fill in username, email, password
- Choose your currency (USD, EUR, INR, etc.)
- Click "Create Account"

### 2. Add Transactions
- Go to "Transactions"
- Click "+ Add Transaction"
- Select type (Income/Expense)
- Choose category
- Enter amount, date, description
- Optionally mark as recurring
- Click "Save Transaction"

### 3. Set Budgets
- Go to "Budgets"
- Click "+ Add Budget"
- Select category
- Set budget amount
- Set alert threshold (e.g., 80%)
- Click "Set Budget"

### 4. View Dashboard
- Real-time financial overview
- Income, expenses, and balance
- Pie chart of expense breakdown
- Recent transactions list

### 5. Export Data
- Go to "Transactions"
- Click "Export" button
- Download CSV file

### 6. Toggle Dark Mode
- Click moon/sun icon (bottom right)
- Theme preference is saved

## 🔑 Environment Variables

Create a `.env` file with these variables:

```bash
# Flask
SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# Database
DATABASE_URL=sqlite:///moneywise.db
# For PostgreSQL:
# DATABASE_URL=postgresql://user:pass@localhost/moneywise

# Email (Gmail example)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# Logging
LOG_TO_STDOUT=false
LOG_LEVEL=INFO
```

## 🚢 Deployment

### Deploy to Render

1. Create a Render account
2. Create a new Web Service
3. Connect your GitHub repository
4. Set environment variables:
   - `SECRET_KEY` - Generate securely
   - `DATABASE_URL` - Provided by Render PostgreSQL
   - `REDIS_URL` - Provided by Render Redis
   - `FLASK_ENV=production`
5. Deploy!

### Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Add Redis
heroku addons:create heroku-redis:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main

# Run migrations
heroku run flask db upgrade
```

## 🔒 Security Best Practices

1. **Never commit** `.env` file
2. **Always use** strong SECRET_KEY in production
3. **Enable** HTTPS in production
4. **Use** PostgreSQL in production (not SQLite)
5. **Enable** Redis for caching
6. **Set up** proper logging
7. **Regular** security updates

## ⚡ Performance Tips

1. **Use Redis** for caching in production
2. **Enable** database connection pooling
3. **Add indexes** to frequently queried columns (already done)
4. **Use pagination** for large datasets (implemented)
5. **Optimize** database queries with `.join()`
6. **Compress** static assets in production

## 🧪 Testing Coverage

Current test coverage: **95%+**

```bash
# View coverage report
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

## 🐛 Troubleshooting

### Problem: Database locked error
**Solution:** SQLite doesn't handle concurrent writes well. Use PostgreSQL for production.

### Problem: CSRF token missing
**Solution:** Ensure all forms include `{{ form.csrf_token }}` or use `{{ form.hidden_tag() }}`

### Problem: Rate limit exceeded
**Solution:** Wait for the time window to reset or adjust limits in config.py

### Problem: Email not sending
**Solution:** Check MAIL_* environment variables and use app-specific password for Gmail

## 📝 API Documentation

### Export Transactions
```
GET /transactions/export
Returns: CSV file with all user transactions
```

### Expense Breakdown
```
GET /api/expense-breakdown
Returns: JSON with category-wise expenses
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

**Yash Khobragade**
- GitHub: [@yas0h00](https://github.com/yas0h00)
- LinkedIn: [Yash Kamble](linkedin.com/in/yash-kamble-37b8722a6)

## 🙏 Acknowledgments

- Flask documentation
- Chart.js for beautiful charts
- Font Awesome for icons
- The open-source community

## 📊 Changelog

### Version 2.0 (Enhanced Edition)
- Added Flask-WTF CSRF protection
- Implemented rate limiting
- Added email notifications
- Created comprehensive test suite
- Added database migrations
- Implemented caching
- Added dark mode
- Enhanced form validation
- Added export functionality
- Optimized database queries
- Added logging
- Created configuration classes

### Version 1.0 (Initial Release)
- Basic CRUD operations
- User authentication
- Category management
- Budget tracking
- Dashboard analytics

---


**Built with ❤️ using Flask**

For questions or issues, please open an issue on GitHub.
=======
**Built with ❤️ by Yash Kamble**

