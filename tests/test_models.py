# tests/test_models.py
import pytest
from datetime import date, datetime
from expense_tracker.models import Expense, Category, StatisticsManager
from decimal import Decimal


class TestExpenseModel:
    """Test Expense model."""
    
    def test_expense_creation(self):
        """Test creating an expense with valid data."""
        expense = Expense(100.50, "Food", "Lunch", date(2024, 1, 15))
        
        assert expense.amount == 100.50
        assert expense.category == "Food"
        assert expense.description == "Lunch"
        assert expense.date == date(2024, 1, 15)
        assert isinstance(expense.id, str)
        assert len(expense.id) > 0
    
    def test_expense_amount_validation(self):
        """Test amount validation."""
        # Valid amounts
        expense1 = Expense(0, "Food", "Free meal")
        assert expense1.amount == 0
        
        expense2 = Expense(1000.99, "Food", "Expensive meal")
        assert expense2.amount == 1000.99
        
        # Invalid amounts
        with pytest.raises(ValueError, match="Amount must be a number"):
            Expense("invalid", "Food", "Test")
        
        with pytest.raises(ValueError, match="Amount must be non-negative"):
            Expense(-100, "Food", "Test")
    
    def test_expense_date_parsing(self):
        """Test date parsing from different formats."""
        # Date object
        expense1 = Expense(100, "Food", "Test", date(2024, 1, 15))
        assert expense1.date == date(2024, 1, 15)
        
        # Date string (YYYY-MM-DD)
        expense2 = Expense(100, "Food", "Test", "2024-01-15")
        assert expense2.date == date(2024, 1, 15)
        
        # Datetime string
        expense3 = Expense(100, "Food", "Test", "2024-01-15T10:30:00")
        assert expense3.date == date(2024, 1, 15)
        
        # Invalid date
        with pytest.raises(ValueError):
            Expense(100, "Food", "Test", "invalid-date")
    
    def test_expense_category_default(self):
        """Test default category when none provided."""
        expense = Expense(100, None, "Test")
        assert expense.category == "Uncategorized"
        
        expense2 = Expense(100, "", "Test")
        assert expense2.category == "Uncategorized"
    
    def test_expense_serialization(self):
        """Test to_serializable() method."""
        expense = Expense(100.50, "Food", "Lunch", date(2024, 1, 15), "test_id")
        
        serialized = expense.to_serializable()
        
        assert serialized == {
            'id': 'test_id',
            'amount': 100.50,
            'category': 'Food',
            'description': 'Lunch',
            'date': '2024-01-15'
        }
    
    def test_expense_from_serializable(self):
        """Test from_serializable() class method."""
        data = {
            'id': 'test_id',
            'amount': 100.50,
            'category': 'Food',
            'description': 'Lunch',
            'date': '2024-01-15'
        }
        
        expense = Expense.from_serializable(data)
        
        assert expense.id == 'test_id'
        assert expense.amount == 100.50
        assert expense.category == 'Food'
        assert expense.description == 'Lunch'
        assert expense.date == date(2024, 1, 15)
    
    def test_expense_equality(self):
        """Test equality comparison."""
        expense1 = Expense(100, "Food", "Lunch", date(2024, 1, 15), "id1")
        expense2 = Expense(100, "Food", "Lunch", date(2024, 1, 15), "id2")
        expense3 = Expense(200, "Food", "Lunch", date(2024, 1, 15), "id1")
        
        # Different IDs but same data should NOT be equal
        # Because Expense equality includes ID comparison
        assert expense1 != expense2
        
        # Same ID but different data should NOT be equal
        assert expense1 != expense3
        
        # Same data and same ID should be equal
        expense4 = Expense(100, "Food", "Lunch", date(2024, 1, 15), "id1")
        assert expense1 == expense4
    
    def test_expense_repr(self):
        """Test string representation."""
        expense = Expense(100.50, "Food", "Lunch", date(2024, 1, 15), "test_id")
        
        repr_str = repr(expense)
        assert "Expense" in repr_str
        assert "test_id" in repr_str
        assert "100.50" in repr_str
        assert "Food" in repr_str


class TestCategoryModel:
    """Test Category model."""
    
    def test_category_creation(self):
        """Test creating a category."""
        category = Category("Food", "Food expenses", 1000.00, 500.00)
        
        assert category.name == "Food"
        assert category.description == "Food expenses"
        assert category.budget_limit == 1000.00
        assert category.monthly_budget == 500.00
    
    def test_category_name_validation(self):
        """Test category name validation."""
        with pytest.raises(ValueError, match="Category name must be non-empty string"):
            Category("", "Test")
        
        with pytest.raises(ValueError, match="Category name must be non-empty string"):
            Category(None, "Test")
    
    def test_budget_limit_validation(self):
        """Test budget limit validation."""
        category = Category("Test", "Test category")
        
        # Valid budget
        category.set_budget(1000.00)
        assert category.budget_limit == 1000.00
        
        # Zero budget
        category.set_budget(0)
        assert category.budget_limit == 0
        
        # Invalid budget
        with pytest.raises(ValueError, match="Budget limit cannot be negative"):
            category.set_budget(-100)
    
    def test_category_equality(self):
        """Test category equality."""
        cat1 = Category("Food", "Food expenses")
        cat2 = Category("Food", "Different description")
        cat3 = Category("Transport", "Transport")
        
        assert cat1 == cat2  # Same name
        assert cat1 != cat3  # Different name
        assert cat1 != "Food"  # Different type
    
    def test_category_serialization(self):
        """Test category serialization."""
        category = Category("Food", "Food expenses", 1000.00, 500.00)
        
        serialized = category.to_serializable()
        
        assert serialized == {
            'name': 'Food',
            'description': 'Food expenses',
            'budget_limit': 1000.00,
            'monthly_budget': 500.00
        }
    
    def test_category_from_dict(self):
        """Test creating category from dictionary."""
        data = {
            'name': 'Food',
            'description': 'Food expenses',
            'budget_limit': 1000.00,
            'monthly_budget': 500.00
        }
        
        category = Category.from_dict(data)
        
        assert category.name == 'Food'
        assert category.description == 'Food expenses'
        assert category.budget_limit == 1000.00
        assert category.monthly_budget == 500.00


class TestStatisticsManager:
    """Test StatisticsManager."""
    
    def test_statistics_manager_initialization(self):
        """Test initialization of StatisticsManager."""
        manager = StatisticsManager()
        
        # Should have default statistics registered
        assert len(manager) > 0
        assert "total" in manager.names()
        assert "average" in manager.names()
        assert "count" in manager.names()
    
    def test_register_statistic(self):
        """Test registering custom statistics."""
        manager = StatisticsManager()
        
        def custom_stat(expenses):
            return len([e for e in expenses if e.amount > 100])
        
        manager.register("expensive_count", custom_stat)
        
        assert "expensive_count" in manager.names()
        assert manager.names()[-1] == "expensive_count"
        
        # Test duplicate registration
        with pytest.raises(ValueError, match="already registered"):
            manager.register("expensive_count", custom_stat)
    
    def test_unregister_statistic(self):
        """Test unregistering statistics."""
        manager = StatisticsManager()
        
        initial_count = len(manager)
        stat_names = manager.names()
        
        if stat_names:
            stat_to_remove = stat_names[0]
            manager.unregister(stat_to_remove)
            
            assert stat_to_remove not in manager.names()
            assert len(manager) == initial_count - 1
            
            # Test unregister non-existent
            with pytest.raises(KeyError):
                manager.unregister("non_existent")
    
    def test_compute_all_statistics(self, sample_expenses, statistics_manager):
        """Test computing all statistics."""
        results = statistics_manager.compute_all(sample_expenses)
        
        assert "total" in results
        assert "average" in results
        assert "count" in results
        assert "by_category" in results
        assert "monthly_total" in results
        
        # Check specific calculations
        assert results["count"] == 5
        assert results["total"] == 800.0  # 100+200+50+300+150
        
        # Check by_category
        category_totals = results["by_category"]
        assert category_totals["Food"] == 300.0  # 100+50+150
        assert category_totals["Transport"] == 200.0
        assert category_totals["Entertainment"] == 300.0
    
    def test_compute_single_statistic(self, sample_expenses, statistics_manager):
        """Test computing a single statistic."""
        total = statistics_manager.compute("total", sample_expenses)
        count = statistics_manager.compute("count", sample_expenses)
        average = statistics_manager.compute("average", sample_expenses)
        
        assert total == 800.0
        assert count == 5
        assert average == 160.0
        
        # Test non-existent statistic
        with pytest.raises(KeyError):
            statistics_manager.compute("non_existent", sample_expenses)
    
    def test_error_handling_in_statistics(self, statistics_manager):
        """Test error handling when computing statistics."""
        # Create a failing statistic
        def failing_stat(expenses):
            raise ValueError("Test error")
        
        statistics_manager.register("failing", failing_stat)
        
        results = statistics_manager.compute_all([])
        
        # Should handle error gracefully
        assert "failing" in results
        assert "error" in str(results["failing"]).lower()