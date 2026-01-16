# 💰 MoneyWise - Personal Finance Tracker

A full-stack web application to help you track expenses, manage budgets, and achieve your financial goals.

![MoneyWise](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- 🔐 **Secure Authentication** - User signup/login with password hashing
- 📊 **Interactive Dashboard** - Real-time statistics and expense charts
- 💳 **Transaction Management** - Track income and expenses with categories
- 💰 **Budget Tracking** - Set limits and monitor spending with alerts
- 📈 **Visual Analytics** - Beautiful charts using Chart.js
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🎨 **Modern UI** - Clean and professional interface

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Extract the ZIP file**
   ```bash
   # Extract to your desired location
   ```

2. **Navigate to the project directory**
   ```bash
   cd moneywise-finance-tracker
   ```

3. **Create virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   ```
   Navigate to: http://127.0.0.1:5000
   ```

## 📁 Project Structure

```
moneywise-finance-tracker/
│
├── app.py                 # Main Flask application
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore file
├── README.md             # This file
│
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Landing page
│   ├── login.html        # Login page
│   ├── signup.html       # Signup page
│   ├── dashboard.html    # Dashboard
│   ├── transactions.html # Transaction management
│   ├── budgets.html      # Budget tracking
│   ├── categories.html   # Category management
│   └── profile.html      # User profile
│
├── static/               # Static files
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   └── js/
│       └── script.js     # JavaScript
│
└── instance/             # Instance folder (auto-created)
    └── moneywise.db      # SQLite database
```

## 🛠️ Tech Stack

### Backend
- **Flask 3.1.2** - Web framework
- **SQLAlchemy** - ORM
- **Flask-Login** - User authentication
- **Werkzeug** - Password hashing

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling
- **JavaScript (ES6+)** - Interactivity
- **Chart.js** - Data visualization

### Database
- **SQLite** - Development database
- **PostgreSQL** - Production ready

## 📖 Usage

### 1. Create an Account
- Click "Get Started Free" on the landing page
- Fill in your details (username, email, password)
- Choose your currency
- Click "Create Account"

### 2. Add Transactions
- Go to "Transactions" page
- Click "+ Add Transaction"
- Select type (Income/Expense)
- Choose category
- Enter amount, date, and description
- Click "Save Transaction"

### 3. Set Budgets
- Go to "Budgets" page
- Click "+ Add Budget"
- Select category
- Set budget amount
- Set alert threshold
- Click "Set Budget"

### 4. View Dashboard
- See your financial overview
- View income, expenses, and balance
- Analyze spending with pie charts
- Track recent transactions

## 🔒 Security Features

- Password hashing with bcrypt
- Session-based authentication
- CSRF protection
- SQL injection prevention (using ORM)
- User data isolation

## 🚢 Deployment

### Deploy to Render

1. Create a Render account
2. Create a new Web Service
3. Connect your GitHub repository
4. Set environment variables:
   - `SECRET_KEY` - Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`
   - `DATABASE_URL` - Automatically provided by Render PostgreSQL
5. Deploy!

## 📝 Environment Variables

Create a `.env` file for local development:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///moneywise.db
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

**Yash Khobragade**
- GitHub: [@yas0h00](https://github.com/yas0h00)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/your-profile)

## 🙏 Acknowledgments

- Flask documentation
- Chart.js for beautiful charts
- Font Awesome for icons

---

**Built with ❤️ by Yash Khobragade**
