import PyInstaller.__main__
import os
import sys

def build_app():
    """Build the inventory management application using PyInstaller"""
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the main script path
    main_script = os.path.join(current_dir, "inv_app.py")
    
    # Define the output directory
    output_dir = os.path.join(current_dir, "dist")
    
    # PyInstaller arguments
    args = [
        main_script,
        '--onefile',  # Create a single executable file
        '--windowed',  # Don't show console window on Windows
        '--name=InventoryManagementSystem',  # Name of the executable
        f'--distpath={output_dir}',  # Output directory
        '--add-data=png;png',  # Include PNG images
        '--add-data=db;db',  # Include database files
        '--icon=png/Blue Black Minimalist Solar Panel Logo.png',  # Application icon
        '--clean',  # Clean cache before building
        '--noconfirm',  # Don't ask for confirmation
    ]
    
    # Add hidden imports that might be needed
    hidden_imports = [
        '--hidden-import=flet',
        '--hidden-import=flet_desktop',
        '--hidden-import=sqlite3',
        '--hidden-import=asyncio',
    ]
    
    args.extend(hidden_imports)
    
    print("Starting build process...")
    print(f"Main script: {main_script}")
    print(f"Output directory: {output_dir}")
    
    try:
        # Run PyInstaller
        PyInstaller.__main__.run(args)
        print("Build completed successfully!")
        print(f"Executable created at: {output_dir}")
    except Exception as e:
        print(f"Build failed with error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = build_app()
    if success:
        print("Application built successfully!")
    else:
        print("Build failed!")
        sys.exit(1) 