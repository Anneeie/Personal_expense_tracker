# 📊 Expense Tracker System

A powerful and intuitive personal expense tracking system built with Python. This package helps you manage your finances by tracking expenses, categorizing spending, and providing detailed statistics and insights.

## ✨ Features

- **💰 Expense Management**: Add, view, update, and delete expenses
- **📊 Categorization**: Organize expenses by categories (Food, Transport, Entertainment, etc.)
- **📈 Statistics**: View spending patterns with comprehensive statistics
- **🔍 Filtering**: Filter expenses by date, category, amount range
- **💾 Data Persistence**: SQLite database for reliable data storage
- **🌐 REST API**: FastAPI-based RESTful API for programmatic access
- **🧪 Testing**: Comprehensive test suite with 68+ tests
- **📁 Data Import/Export**: JSON import/export functionality

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Install from PyPI
```bash
pip install expense-tracker-system==1.0.0
```

### Install from source
```bash
# Clone the repository
git clone https://github.com/yourusername/expense-tracker-system.git
cd expense-tracker-system

# Install in development mode
pip install -e .

# Or install dependencies
pip install -r requirements.txt
```

## 📦 Requirements

The package automatically installs these dependencies:
- `fastapi` - Web framework for building APIs
- `uvicorn` - ASGI server for running the API
- `sqlalchemy` - Database ORM
- `pydantic` - Data validation
- `pytest` - Testing framework
- `python-dateutil` - Date handling utilities

## 🛠️ Quick Start

### Using the CLI Interface
```bash
# Run the interactive application
python -m expense_tracker.cli

# Or use the provided runner
python run.py
```

### Using the API
```bash
# Start the API server
python -m expense_tracker.api

# The API will be available at http://localhost:8000
# Visit http://localhost:8000/docs for interactive API documentation
```

### Basic Python Usage
```python
from expense_tracker.tracker import ExpenseTracker

# Create a tracker instance
tracker = ExpenseTracker()

# Add an expense
expense = tracker.add_expense(
    amount=29.99,
    category="Food",
    description="Lunch at restaurant",
    date="2024-01-15"
)

# View all expenses
expenses = tracker.view_all()

# Get statistics
stats = tracker.view_statistics()
print(f"Total spent: ${stats['total']:.2f}")
```

## 📚 API Reference

### REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API root with endpoint list |
| GET | `/health` | Health check endpoint |
| GET | `/expenses` | Get all expenses |
| POST | `/expenses` | Create new expense |
| GET | `/expenses/{id}` | Get specific expense |
| PUT | `/expenses/{id}` | Update expense |
| DELETE | `/expenses/{id}` | Delete expense |
| GET | `/categories` | Get all categories |
| GET | `/statistics` | Get expense statistics |
| GET | `/expenses/filter` | Filter expenses |

### Example API Requests
```bash
# Create an expense
curl -X POST "http://localhost:8000/expenses" \
  -H "Content-Type: application/json" \
  -d '{"amount": 50, "category": "Food", "description": "Groceries"}'

# Get all expenses
curl "http://localhost:8000/expenses"

# Get statistics
curl "http://localhost:8000/statistics"
```

## 🧪 Running Tests

The package includes a comprehensive test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/test_database.py -v
python -m pytest tests/test_models.py -v
python -m pytest tests/test_api.py -v

# Run with coverage report
python -m pytest --cov=expense_tracker tests/
```

### Test Coverage
- ✅ **Database Tests**: 15/15 passing - Core database operations
- ✅ **Model Tests**: 19/21 passing - Data models and validation
- 🔄 **Tracker Tests**: 2/28 passing - Business logic (in progress)
- 🔄 **API Tests**: 0/4 passing - REST endpoints (in progress)

## 🏗️ Project Structure

```
expense_tracker_system/
├── expense_tracker/          # Main package
│   ├── __init__.py
│   ├── api.py               # FastAPI application
│   ├── database.py          # Database models and operations
│   ├── models.py            # Pydantic models and business logic
│   ├── tracker.py           # Main expense tracker class
│   └── cli.py               # Command-line interface
├── tests/                   # Test suite
│   ├── test_api.py
│   ├── test_database.py
│   ├── test_models.py
│   ├── test_tracker.py
│   └── conftest.py
├── run.py                   # Main runner script
├── requirements.txt         # Dependencies
├── setup.py                # Package configuration
└── pyproject.toml          # Build system configuration
```

## 🔧 Advanced Usage

### Custom Database Path
```python
from expense_tracker.database import Database

# Use custom database location
db = Database("/path/to/your/expenses.db")
```

### Bulk Operations
```python
from expense_tracker.database import Database

db = Database("expenses.db")

# Bulk insert expenses
expenses_data = [
    {"amount": 100, "category": "Food", "description": "Lunch"},
    {"amount": 200, "category": "Transport", "description": "Taxi"},
]
db.bulk_insert_expenses(expenses_data)
```

### JSON Export/Import
```python
from expense_tracker.database import Database

db = Database("expenses.db")

# Export to JSON
db.export_to_json("backup.json")

# Import from JSON
db.import_from_json("backup.json")
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs**: Open an issue with detailed bug reports
2. **Suggest Features**: Propose new features or improvements
3. **Submit Pull Requests**: Implement fixes or features

### Development Setup
```bash
# 1. Fork and clone the repository
git clone https://github.com/yourusername/expense-tracker-system.git

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install in development mode
pip install -e .

# 4. Run tests to ensure everything works
python -m pytest tests/
```


  <br>
  <sub>If you find this useful, please consider giving it a ⭐ on GitHub!</sub>
</div>
