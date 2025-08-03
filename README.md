# Inventory Management System

A sophisticated desktop application for managing solar panel inventory with a **Pure Black & White Monochromatic Design System**, featuring ultra-modern glass effects and minimalist elegance.

## Features

- **Pure Monochromatic Design**: Sophisticated black and white theme with ultra-subtle glass effects
- **Inventory Management**: Add, edit, delete, and search inventory items
- **Billing System**: Create and manage billing records with payment tracking
- **Dashboard**: Real-time statistics and overview of your business
- **User Management**: Secure login system with user settings
- **Responsive UI**: Modern, intuitive interface with smooth animations

## Screenshots

The application features:
- Splash screen with solar panel branding
- Modern login interface with glass effects
- Dashboard with real-time statistics
- Inventory management with search and filtering
- Billing system with payment tracking
- Settings page for user management

## Installation

### Prerequisites

- Python 3.8 or higher
- Windows 10/11 (for desktop build)

### Setup

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd inventory-management-desktop
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python inv_app.py
   ```

## Building the Application

### Quick Build (Windows)
Simply double-click the `build.bat` file to automatically build the application.

### Manual Build
```bash
python build.py
```

The executable will be created in the `dist` folder.

## Usage

### Login
- Default credentials: `admin` / `admin`
- The system uses SQLite database for data storage

### Navigation
- **Dashboard**: Overview of sales, profit, and inventory statistics
- **Inventory**: Manage your solar panel inventory items
- **Billing**: Create and manage customer billing records
- **Settings**: Update user credentials and account information

### Key Features
- **Search**: Use the search bar to quickly find items or bills
- **Add Items**: Click "Add New Item" to add inventory items
- **Edit/Delete**: Use the action buttons in tables to modify records
- **Real-time Updates**: All changes are immediately reflected in the UI

## Project Structure

```
inventory-management-desktop/
├── inv_app.py              # Main application entry point
├── view_handler.py         # Route management
├── screens/                # UI screens
│   ├── theme.py           # iOS 26 design system
│   ├── login.py           # Login screen
│   ├── home.py            # Dashboard
│   ├── inv.py             # Inventory management
│   ├── billing.py         # Billing system
│   └── settings.py        # User settings
├── db/                    # Database handlers
│   ├── db_handler.py      # Main database operations
│   ├── inv_handler.py     # Inventory operations
│   └── billing_handler.py # Billing operations
├── png/                   # Images and assets
├── requirements.txt       # Python dependencies
├── build.py              # Build script
└── build.bat             # Windows build script
```

## Design System

The application uses a custom iOS 26-inspired design system with:

- **Colors**: Pure black backgrounds (#000000) with white text (#FFFFFF)
- **Glass Effects**: Semi-transparent containers with blur effects
- **Typography**: Modern, clean fonts with proper hierarchy
- **Icons**: Material Design icons with consistent styling
- **Animations**: Smooth transitions and hover effects

## Database

The application uses SQLite for data storage:
- **Users**: User authentication and management
- **Inventory**: Product information, quantities, and costs
- **Billing**: Customer records, payments, and status tracking

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Errors**: The application will create the database automatically on first run

3. **Build Errors**: Ensure PyInstaller is installed
   ```bash
   pip install pyinstaller
   ```

4. **Image Loading**: Make sure the `png` folder is in the same directory as the executable

### Support

If you encounter any issues:
1. Check that all dependencies are installed
2. Ensure you're using Python 3.8 or higher
3. Verify the database file has proper permissions
4. Check the console output for error messages

## Development

### Adding New Features
1. Create new screen files in the `screens/` directory
2. Update `view_handler.py` to include new routes
3. Follow the existing design patterns in `theme.py`

### Customizing the Design
- Modify `screens/theme.py` to change colors, fonts, and styling
- Update individual screen files to customize specific components
- Add new theme functions for consistent styling

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Note**: This application is designed for solar panel inventory management but can be easily adapted for other inventory types by modifying the database schema and UI text. 