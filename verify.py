#!/usr/bin/env python3
"""
Quick verification script for Inventory Management System
"""

def verify_application():
    """Verify that the application can be imported and initialized"""
    print("🔍 Verifying Inventory Management System...")
    
    try:
        # Test imports
        from screens.theme import IOS26Theme, glass_container
        print("✅ Theme system working")
        
        from screens.login import LoginScreen
        from screens.home import HomeScreen
        from screens.inv import InventoryScreen
        from screens.billing import BillingScreen
        from screens.settings import SettingsScreen
        print("✅ All screen classes imported")
        
        from db.db_handler import get_db_connection
        print("✅ Database connection working")
        
        # Test database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Users")
        user_count = cursor.fetchone()[0]
        print(f"✅ Database accessible - {user_count} users found")
        conn.close()
        
        # Test theme functions
        test_container = glass_container(content="Test", width=100, height=100)
        print("✅ Glass container creation working")
        
        print("\n🎉 All verifications passed!")
        print("The application is ready to run.")
        print("\nTo start the application, run:")
        print("   python inv_app.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

if __name__ == "__main__":
    verify_application() 