#!/usr/bin/env python3
"""
Test script to verify the monochromatic theme implementation
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_theme_import():
    """Test if the theme module can be imported"""
    try:
        from screens.theme import IOS26Theme
        print("✅ Theme module imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import theme module: {e}")
        return False

def test_theme_colors():
    """Test if the monochromatic colors are properly defined"""
    try:
        from screens.theme import IOS26Theme
        
        # Check background colors
        assert IOS26Theme.BACKGROUND_PRIMARY == "#000000", "Background primary should be pure black"
        assert IOS26Theme.BACKGROUND_SECONDARY == "#0A0A0A", "Background secondary should be very dark gray"
        
        # Check text colors
        assert IOS26Theme.TEXT_PRIMARY == "#FFFFFF", "Text primary should be pure white"
        assert IOS26Theme.TEXT_SECONDARY == "#E0E0E0", "Text secondary should be light gray"
        
        # Check accent colors
        assert IOS26Theme.ACCENT_PRIMARY == "#FFFFFF", "Accent primary should be pure white"
        assert IOS26Theme.ACCENT_SECONDARY == "#F0F0F0", "Accent secondary should be off-white"
        
        print("✅ All monochromatic colors are properly defined")
        return True
    except Exception as e:
        print(f"❌ Theme colors test failed: {e}")
        return False

def test_theme_components():
    """Test if theme components can be created"""
    try:
        from screens.theme import (
            glass_container, primary_button, secondary_button,
            modern_text_field, modern_card, heading_text, body_text,
            modern_icon, modern_data_table, stat_card
        )
        
        # Test creating components
        text = heading_text("Test")
        button = primary_button("Test")
        card = modern_card(text)
        
        print("✅ All theme components can be created successfully")
        return True
    except Exception as e:
        print(f"❌ Theme components test failed: {e}")
        return False

def test_screen_imports():
    """Test if screens can import the theme"""
    try:
        from screens.home import HomeScreen
        from screens.inv import InventoryScreen
        from screens.billing import BillingScreen
        from screens.settings import SettingsScreen
        
        print("✅ All screens can import theme components")
        return True
    except Exception as e:
        print(f"❌ Screen imports test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🎨 Testing Monochromatic Theme Implementation")
    print("=" * 50)
    
    tests = [
        test_theme_import,
        test_theme_colors,
        test_theme_components,
        test_screen_imports
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Monochromatic theme is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 