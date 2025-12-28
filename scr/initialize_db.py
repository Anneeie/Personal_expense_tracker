#!/usr/bin/env python3
"""
Quick database initialization script
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 50)
    print("🔧 INITIALIZING EXPENSE TRACKER DATABASE")
    print("=" * 50)
    
    try:
        # Create data directory
        os.makedirs("data", exist_ok=True)
        print("✅ Created data/ directory")
        
        # Try to import and create database
        from expense_tracker.database import Database
        
        db_path = "data/expenses.db"
        print(f"📁 Database path: {db_path}")
        
        # This creates tables automatically
        db = Database(db_path)
        print("✅ Database initialized successfully!")
        
        # Simple verification
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall() if not row[0].startswith('sqlite_')]
        
        print(f"📊 Tables created: {', '.join(tables)}")
        conn.close()
        
        print("\n" + "=" * 50)
        print("🎉 DATABASE READY!")
        print("=" * 50)
        print("\nYou can now:")
        print("  • Run the API: python run.py (choose option 3)")
        print("  • Use the CLI: python run.py (choose option 2)")
        print("  • Seed data: python run.py (choose option 4)")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the project root and packages are installed")
        print("Try: pip install -e .")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)