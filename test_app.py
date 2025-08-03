#!/usr/bin/env python3
"""
Test script for Inventory Management System
This script tests the basic functionality without launching the full UI
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import flet as ft
        print("✅ Flet imported successfully")
    except ImportError as e:
        print(f"❌ Flet import failed: {e}")
        return False
    
    try:
        from screens.theme import IOS26Theme, glass_container, primary_button
        print("✅ Theme module imported successfully")
    except ImportError as e:
        print(f"❌ Theme import failed: {e}")
        return False
    
    try:
        from db.db_handler import get_db_connection
        print("✅ Database handler imported successfully")
    except ImportError as e:
        print(f"❌ Database handler import failed: {e}")
        return False
    
    try:
        from screens.user import User
        print("✅ User module imported successfully")
    except ImportError as e:
        print(f"❌ User import failed: {e}")
        return False
    
    return True

def test_database():
    """Test database connectivity"""
    print("\nTesting database...")
    
    try:
        from db.db_handler import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Test if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"✅ Database connected successfully. Found {len(tables)} tables:")
        
        for table in tables:
            print(f"   - {table[0]}")
        
        # Test user table
        cursor.execute("SELECT COUNT(*) FROM Users")
        user_count = cursor.fetchone()[0]
        print(f"✅ Users table accessible. Found {user_count} users")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_theme_functions():
    """Test theme functions"""
    print("\nTesting theme functions...")
    
    try:
        from screens.theme import glass_container, primary_button, modern_text_field
        
        # Test glass container
        test_container = glass_container(
            content="Test",
            width=100,
            height=100
        )
        print("✅ Glass container created successfully")
        
        # Test primary button
        test_button = primary_button(
            text="Test Button",
            width=100
        )
        print("✅ Primary button created successfully")
        
        # Test text field
        test_field = modern_text_field(
            label="Test Field",
            width=200
        )
        print("✅ Text field created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Theme functions test failed: {e}")
        return False

def test_screen_classes():
    """Test screen class instantiation"""
    print("\nTesting screen classes...")
    
    try:
        from screens.login import LoginScreen
        from screens.home import HomeScreen
        from screens.inv import InventoryScreen
        from screens.billing import BillingScreen
        from screens.settings import SettingsScreen
        
        # Create a mock page object
        class MockPage:
            def __init__(self):
                self.route = "/"
            
            def go(self, route):
                self.route = route
            
            def update(self):
                pass
        
        mock_page = MockPage()
        
        # Test screen instantiation
        login_screen = LoginScreen(mock_page)
        print("✅ LoginScreen instantiated successfully")
        
        home_screen = HomeScreen(mock_page)
        print("✅ HomeScreen instantiated successfully")
        
        inv_screen = InventoryScreen(mock_page)
        print("✅ InventoryScreen instantiated successfully")
        
        billing_screen = BillingScreen(mock_page)
        print("✅ BillingScreen instantiated successfully")
        
        settings_screen = SettingsScreen(mock_page)
        print("✅ SettingsScreen instantiated successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Screen classes test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Inventory Management System - Component Tests")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_database,
        test_theme_functions,
        test_screen_classes
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 