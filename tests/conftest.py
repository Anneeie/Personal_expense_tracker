# tests/conftest.py - OPTIMAL VERSION
import pytest
import tempfile
import os
from pathlib import Path
import sys
from datetime import date, datetime
from decimal import Decimal

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from expense_tracker.database import Database, ExpenseDB, CategoryDB
from expense_tracker.models import Expense, Category, StatisticsManager
from expense_tracker.tracker import ExpenseTracker


@pytest.fixture
def temp_db_path():
    """Create a temporary database file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    yield db_path
    # Cleanup after tests
    if os.path.exists(db_path):
        try:
            os.unlink(db_path)
        except:
            pass


@pytest.fixture
def sample_expense_data():
    """Sample expense data for testing."""
    return {
        'id': 'test_exp_001',
        'amount': 100.50,
        'category': 'Food',
        'description': 'Lunch at restaurant',
        'date': date(2024, 1, 15)
    }


@pytest.fixture
def sample_category_data():
    """Sample category data for testing."""
    return {
        'name': 'Test Category',
        'description': 'Test description',
        'budget_limit': 1000.00,
        'monthly_budget': 500.00
    }


@pytest.fixture
def database(temp_db_path):
    """Database instance with temporary database."""
    db = Database(temp_db_path)
    yield db
    # Cleanup session
    try:
        db.engine.dispose()
    except:
        pass


@pytest.fixture
def expense_tracker(database):
    """ExpenseTracker instance with test database."""
    return ExpenseTracker(db_path=database.db_path, auto_load=False)


@pytest.fixture
def sample_expenses():
    """List of sample expenses for testing."""
    return [
        Expense(100, "Food", "Lunch", date(2024, 1, 15), "exp1"),
        Expense(200, "Transport", "Taxi", date(2024, 1, 16), "exp2"),
        Expense(50, "Food", "Coffee", date(2024, 1, 17), "exp3"),
        Expense(300, "Entertainment", "Movie", date(2024, 2, 1), "exp4"),
        Expense(150, "Food", "Dinner", date(2024, 2, 15), "exp5"),
    ]


@pytest.fixture
def sample_categories():
    """List of sample categories for testing."""
    return [
        Category("Food", "Food expenses", 1000.00, 500.00),
        Category("Transport", "Transportation", 500.00, 300.00),
        Category("Entertainment", "Fun activities", 300.00, 200.00),
    ]


# tests/conftest.py - UPDATE statistics_manager fixture
@pytest.fixture
def statistics_manager():
    """StatisticsManager instance for testing."""
    # Create a fresh instance and manually register statistics
    from expense_tracker.models import StatisticsManager
    
    # Reset singleton if it exists
    if hasattr(StatisticsManager, '_instance'):
        StatisticsManager._instance = None
    
    manager = StatisticsManager()
    
    # Manually register the built-in statistics if _register_builtins doesn't exist
    if not hasattr(manager, '_register_builtins'):
        # Register built-in statistics manually
        manager.register("total", lambda expenses: sum(exp.amount for exp in expenses))
        manager.register("average", lambda expenses: sum(exp.amount for exp in expenses) / len(expenses) if expenses else 0)
        manager.register("count", lambda expenses: len(expenses))
        manager.register("by_category", lambda expenses: {})
        manager.register("monthly_total", lambda expenses: {})
        manager.register("total_sum", lambda expenses: sum(exp.amount for exp in expenses))
    
    return manager

@pytest.fixture
def api_client(database):
    """FastAPI test client with dependency override."""
    from fastapi.testclient import TestClient
    from expense_tracker.api import app
    from expense_tracker.tracker import ExpenseTracker
    # Set testing environment

    os.environ["TESTING"] = "true"
    
    # Import and override get_tracker if it exists

    def override_get_tracker():
        return ExpenseTracker(db_path=database.db_path, auto_load=False)
        
    app.dependency_overrides = {}
    
    app.dependency_overrides['get_tracker'] = override_get_tracker
    if "TESTING" in os.environ:
        del os.environ["TESTING"]

    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset all singleton instances between tests."""
    # Reset StatisticsManager
    if hasattr(StatisticsManager, '_instance'):
        StatisticsManager._instance = None
    yield