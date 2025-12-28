#!/usr/bin/env python3
"""
Expense Tracker - Main Runner Script
"""


import os
import sys
from datetime import datetime
import subprocess

def clear_screen():
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    """Display application header."""
    clear_screen()
    print("=" * 60)
    print("💰 EXPENSE TRACKER SYSTEM")
    print("=" * 60)

def main():
    import os  # ensure module is imported here
    import sys

    # Check virtual environment
    if not os.path.exists("venv") and not os.environ.get("VIRTUAL_ENV"):
        print("⚠️  Virtual environment not detected!")
        print("Please activate the virtual environment first:")
        sys.exit(1)
    
    # Rest of your main function...
    
    # Ստուգել, որ virtual environment-ը ակտիվացված է
    if not os.path.exists("venv") and not os.environ.get("VIRTUAL_ENV"):
        print("⚠️  Warning: Virtual environment not detected.")
        print("   It's recommended to run: venv\\Scripts\\activate")
        response = input("   Continue anyway? (y/N): ").strip().lower()
        if response != 'y':
            print("Exiting...")
            return
    
    # Ստեղծել data թղթապանակը
    os.makedirs("data", exist_ok=True)
    
    while True:
        print("\n📋 MAIN MENU")
        print("=" * 30)
        print("1. Initialize Database (First Time Setup)")
        print("2. Run CLI (Command Line Interface)")
        print("3. Run API Server")
        print("4. Seed Database with Sample Data")
        print("5. Run All Tests")
        print("6. Exit")
        print("=" * 30)
        
        choice = input("\nChoose option (1-6): ").strip()
        
        if choice == "1":
            print("\n🔧 Initializing Database...")
            try:
                # Գործարկել ինիցիալիզացիայի սկրիպտը
                from expense_tracker.database import Database
                db = Database("data/expenses.db")
                print("✅ Database initialized successfully!")
                print("📁 Location: data/expenses.db")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif choice == "2":
            print("\n💻 Starting CLI...")
            try:
                from expense_tracker.cli import main as cli_main
                cli_main()
            except ImportError as e:
                print(f"❌ Import Error: {e}")
                print("Make sure you're in the correct directory.")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif choice == "3":
            print("\n🌐 Starting API Server...")
            print("   API will be available at: http://localhost:8000")
            print("   Documentation: http://localhost:8000/docs")
            print("\n   Press Ctrl+C to stop the server")
            print("-" * 50)
            try:
                # Փոփոխություն API-ի համար Pydantic-ի նախազգուշացումները լուծելու համար
                os.environ["PYTHONWARNINGS"] = "ignore"
                from expense_tracker.api import run
                run()
            except KeyboardInterrupt:
                print("\n\n⏹️  API Server stopped.")
            except ImportError as e:
                print(f"❌ Import Error: {e}")
                print("Trying alternative method...")
                try:
                    subprocess.run([sys.executable, "-m", "expense_tracker.api"])
                except Exception as e2:
                    print(f"❌ Error: {e2}")
        
        elif choice == "4":
            print("\n🌱 Seeding Database with Sample Data...")
            print("   This demonstrates threading for I/O-bound operations.")
            print("-" * 50)
            try:
                from expense_tracker.seed import DataSeeder
                seeder = DataSeeder("data/expenses.db")
                seeder.run_seeding_pipeline()
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Using simple fallback seeding...")
                # Simple SQLite fallback
                import sqlite3
                import random
                from datetime import date, timedelta
                
                conn = sqlite3.connect("data/expenses.db")
                cursor = conn.cursor()
                
                # Create table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS expenses (
                        id TEXT PRIMARY KEY,
                        amount REAL NOT NULL,
                        category TEXT,
                        description TEXT,
                        date TEXT NOT NULL
                    )
                """)
                
                categories = ["Food", "Transport", "Entertainment", "Bills"]
                count = 0
                
                for i in range(30):
                    expense_date = date.today() - timedelta(days=random.randint(0, 100))
                    cursor.execute("""
                        INSERT OR IGNORE INTO expenses (id, amount, category, description, date)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        f"DEMO_{i:04d}",
                        round(random.uniform(5, 200), 2),
                        random.choice(categories),
                        f"Demo expense {i}",
                        expense_date.isoformat()
                    ))
                    count += 1
                
                conn.commit()
                conn.close()
                print(f"✅ Added {count} demo expenses to database")
                
        # In your run.py file, add this code to elif choice == "5" section:

        elif choice == "5":
            print("\n" + "="*60)
            print("🧪 RUNNING TESTS")
            print("="*60)
            
            import subprocess
            import sys
            import os
            
            def run_tests_and_display():
                """Run tests and display results."""
                
                # Test categories to run
                test_categories = [
                    ("Database Tests", ["tests/test_database.py", "-k", "not export_import_json"]),
                    ("Model Tests", ["tests/test_models.py"]),
                    ("Tracker Tests", ["tests/test_tracker.py"]),
                    ("API Tests", ["tests/test_api.py"]),
                ]
                
                all_results = []
                total_passed = 0
                total_failed = 0
                total_errors = 0
                
                for category_name, test_args in test_categories:
                    print(f"\n📊 {category_name}")
                    print("-" * 40)
                    
                    # Build command
                    cmd = [sys.executable, "-m", "pytest"] + test_args + ["-v", "--tb=short", "--disable-warnings"]
                    
                    try:
                        result = subprocess.run(
                            cmd,
                            capture_output=True,
                            text=True,
                            encoding='utf-8',
                            errors='replace'
                        )
                        
                        # Parse results
                        output_lines = result.stdout.split('\n')
                        
                        # Count results
                        passed = len([l for l in output_lines if "PASSED" in l])
                        failed = len([l for l in output_lines if "FAILED" in l])
                        error = len([l for l in output_lines if "ERROR" in l])
                        
                        total_passed += passed
                        total_failed += failed
                        total_errors += error
                        
                        # Display summary
                        print(f"   ✅ Passed: {passed}")
                        print(f"   ❌ Failed: {failed}")
                        print(f"   ⚠️  Errors: {error}")
                        
                        # Show first few test results
                        test_lines = [l for l in output_lines if "test_" in l and ("PASSED" in l or "FAILED" in l or "ERROR" in l)]
                        for line in test_lines[:5]:  # Show first 5 test results
                            print(f"   {line}")
                        
                        if failed > 0 or error > 0:
                            all_results.append((category_name, False))
                        else:
                            all_results.append((category_name, True))
                            
                    except FileNotFoundError:
                        print(f"   ⚠️  Test file not found: {test_args[0]}")
                        all_results.append((category_name, False))
                    except Exception as e:
                        print(f"   ❌ Error running tests: {str(e)[:100]}")
                        all_results.append((category_name, False))
                
                # Display overall summary
                print("\n" + "="*60)
                print("📈 OVERALL TEST RESULTS")
                print("="*60)
                
                total_tests = total_passed + total_failed + total_errors
                
                print(f"Total Tests Run: {total_tests}")
                print(f"✅ Passed: {total_passed}")
                print(f"❌ Failed: {total_failed}")
                print(f"⚠️  Errors: {total_errors}")
                
                if total_tests == 0:
                    print("\n⚠️  No tests were executed!")
                elif total_failed == 0 and total_errors == 0:
                    success_rate = 100.0
                    print(f"\n🎉 All tests passed! ({success_rate:.1f}% success rate)")
                else:
                    success_rate = (total_passed / total_tests) * 100 if total_tests > 0 else 0
                    print(f"\n📊 Success Rate: {success_rate:.1f}%")
                
                # Detailed breakdown
                print("\n🔍 Detailed Breakdown:")
                print("-" * 40)
                for category, passed in all_results:
                    status = "✅ PASS" if passed else "❌ FAIL/ERROR"
                    print(f"{category:20} {status}")
                
                # Recommendations
                print("\n💡 Recommendations:")
                print("-" * 40)
                
                if total_failed > 0 or total_errors > 0:
                    if total_errors > 0:
                        print("• Fix import errors in test files")
                    if "Database Tests" in [cat for cat, passed in all_results if not passed]:
                        print("• Check database connection and schema")
                    if "Model Tests" in [cat for cat, passed in all_results if not passed]:
                        print("• Verify model class definitions")
                    if "API Tests" in [cat for cat, passed in all_results if not passed]:
                        print("• Ensure API endpoints are properly defined")
                    if "Tracker Tests" in [cat for cat, passed in all_results if not passed]:
                        print("• Check ExpenseTracker initialization")
                else:
                    print("• All tests are passing! Good job!")
                
                return total_failed + total_errors == 0
            
            # Run tests
            success = run_tests_and_display()
            
            if success:
                print("\n✅ All tests completed successfully!")
            else:
                print("\n⚠️  Some tests failed. See details above.")
            
            print("\nPress Enter to continue...")
            input()
        
        elif choice == "6":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("\n❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()