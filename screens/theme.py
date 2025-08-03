# Custom Zero-Yellow Color System - Completely Custom Implementation
import flet as ft
from flet import *
from flet import ColorScheme, Brightness

# ABSOLUTE ZERO YELLOW COLOR SYSTEM - Pure Custom Hex Colors
class ZeroYellowTheme:
    """Completely custom color system with ZERO yellow - No Flet theming dependencies"""
    
    # Core Colors - Pure Black and White Base
    PURE_BLACK = "#000000"
    PURE_WHITE = "#FFFFFF"
    
    # Background Hierarchy - All Black/Gray
    BG_PRIMARY = "#000000"      # Pure black background
    BG_SECONDARY = "#0A0A0A"    # Slightly lighter black
    BG_TERTIARY = "#141414"     # Dark gray
    BG_QUATERNARY = "#1E1E1E"   # Lighter dark gray
    BG_GLASS = "#00000080"      # Semi-transparent black
    
    # Text Hierarchy - All White/Gray
    TEXT_PRIMARY = "#FFFFFF"    # Pure white text
    TEXT_SECONDARY = "#E0E0E0"  # Light gray text
    TEXT_TERTIARY = "#C0C0C0"   # Medium gray text
    TEXT_QUATERNARY = "#A0A0A0" # Darker gray text
    TEXT_DISABLED = "#808080"   # Disabled gray text
    
    # Interactive Elements - All Gray Scale
    ACCENT_PRIMARY = "#FFFFFF"   # White for primary actions
    ACCENT_SECONDARY = "#E0E0E0" # Light gray for secondary
    ACCENT_TERTIARY = "#C0C0C0"  # Medium gray for tertiary
    ACCENT_QUATERNARY = "#A0A0A0" # Dark gray for quaternary
    
    # Glass Effects - Enhanced for Elegance
    GLASS_BG = "#FFFFFF08"       # More subtle transparent white
    GLASS_BORDER = "#FFFFFF25"   # Slightly more visible border
    GLASS_SHADOW = "#00000060"   # Deeper shadow for better depth
    GLASS_HIGHLIGHT = "#FFFFFF05" # Subtle highlight effect
    
    # States
    HOVER = "#FFFFFF15"          # Light hover effect
    FOCUS = "#FFFFFF25"          # Focus effect
    SELECTED = "#FFFFFF20"       # Selection effect
    ERROR = "#FF4444"            # Red for errors (no yellow)
    SUCCESS = "#44FF44"          # Green for success (no yellow)
    WARNING = "#FF8844"          # Orange for warnings (no yellow)

# Custom Components with Zero Yellow Guarantee
def zero_yellow_container(content, **kwargs):
    """Container with guaranteed zero yellow and elegant responsive styling"""
    # Handle border_color specially
    border_color = kwargs.pop('border_color', ZeroYellowTheme.GLASS_BORDER)
    border_obj = kwargs.get('border', border.all(1, border_color))
    
    # Auto-sizing: Don't force width/height unless specified
    default_padding = kwargs.get('padding', padding.all(16))  # Responsive padding
    default_margin = kwargs.get('margin', margin.all(8))      # Responsive margin
    
    return Container(
        content=content,
        bgcolor=kwargs.get('bgcolor', ZeroYellowTheme.BG_GLASS),
        border=border_obj,
        border_radius=kwargs.get('border_radius', 16),
        padding=default_padding,
        margin=default_margin,
        # Auto-expand if needed
        expand=kwargs.get('expand', None),  # Let container size naturally
        shadow=BoxShadow(
            spread_radius=2,
            blur_radius=24,
            color=ZeroYellowTheme.GLASS_SHADOW,
            offset=Offset(0, 12)
        ),
        **{k: v for k, v in kwargs.items() if k not in ['bgcolor', 'border', 'border_radius', 'padding', 'margin', 'border_color', 'expand']}
    )

def zero_yellow_button(text, on_click=None, primary=True, **kwargs):
    """Button with guaranteed zero yellow and elegant styling"""
    # Remove conflicting parameters from kwargs
    kwargs.pop('bgcolor', None)
    kwargs.pop('color', None)
    
    return Container(
        content=Text(
            text,
            color=ZeroYellowTheme.PURE_BLACK if primary else ZeroYellowTheme.TEXT_PRIMARY,
            weight=FontWeight.W_600,
            text_align=TextAlign.CENTER,
            size=14
        ),
        bgcolor=ZeroYellowTheme.ACCENT_PRIMARY if primary else ZeroYellowTheme.BG_TERTIARY,
        border=border.all(1, ZeroYellowTheme.GLASS_BORDER),
        border_radius=12,  # More rounded for elegance
        padding=padding.symmetric(horizontal=24, vertical=14),  # More generous padding
        on_click=on_click,
        ink=False,  # Disable any material ink effects
        shadow=BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color=ZeroYellowTheme.GLASS_SHADOW,
            offset=Offset(0, 4)
        ),
        **kwargs
    )

def zero_yellow_text_field(label="", hint_text="", value="", on_change=None, password=False, **kwargs):
    """Text field with guaranteed zero yellow"""
    return TextField(
        label=label,
        hint_text=hint_text,
        value=value,
        on_change=on_change,
        password=password,
        bgcolor=ZeroYellowTheme.BG_TERTIARY,
        color=ZeroYellowTheme.TEXT_PRIMARY,
        border_color=ZeroYellowTheme.GLASS_BORDER,
        focused_border_color=ZeroYellowTheme.ACCENT_PRIMARY,
        cursor_color=ZeroYellowTheme.ACCENT_PRIMARY,
        selection_color=ZeroYellowTheme.SELECTED,
        border_radius=8,
        text_style=TextStyle(
            color=ZeroYellowTheme.TEXT_PRIMARY,
            size=14
        ),
        label_style=TextStyle(
            color=ZeroYellowTheme.TEXT_SECONDARY,
            size=12
        ),
        hint_style=TextStyle(
            color=ZeroYellowTheme.TEXT_TERTIARY,
            size=14
        ),
        **kwargs
    )

def zero_yellow_text(value, size=14, weight=FontWeight.NORMAL, color=None, **kwargs):
    """Text with guaranteed zero yellow"""
    return Text(
        value,
        size=size,
        weight=weight,
        color=color or ZeroYellowTheme.TEXT_PRIMARY,
        **kwargs
    )

def zero_yellow_heading(text, level=1):
    """Heading with guaranteed zero yellow"""
    sizes = {1: 24, 2: 20, 3: 18, 4: 16}
    return Text(
        text,
        size=sizes.get(level, 16),
        weight=FontWeight.BOLD,
        color=ZeroYellowTheme.TEXT_PRIMARY
    )

def zero_yellow_icon(icon, size=24, color=None):
    """Icon with guaranteed zero yellow"""
    return Icon(
        icon,
        size=size,
        color=color or ZeroYellowTheme.TEXT_PRIMARY
    )

def zero_yellow_icon_button(icon, on_click=None, tooltip="", size=24):
    """Icon button with guaranteed zero yellow"""
    return Container(
        content=Icon(
            icon,
            size=size,
            color=ZeroYellowTheme.TEXT_PRIMARY
        ),
        bgcolor=ZeroYellowTheme.BG_TERTIARY,
        border=border.all(1, ZeroYellowTheme.GLASS_BORDER),
        border_radius=6,
        padding=8,
        on_click=on_click,
        tooltip=tooltip,
        ink=False
    )

def zero_yellow_data_table(columns, rows):
    """Data table with guaranteed zero yellow"""
    return Container(
        content=DataTable(
            columns=columns,
            rows=rows,
            bgcolor=ZeroYellowTheme.BG_SECONDARY,
            heading_row_color=ZeroYellowTheme.BG_TERTIARY,
            data_row_color=ZeroYellowTheme.BG_SECONDARY
        ),
        bgcolor=ZeroYellowTheme.BG_GLASS,
        border=border.all(1, ZeroYellowTheme.GLASS_BORDER),
        border_radius=12,
        padding=10
    )

def zero_yellow_snackbar(message):
    """Snackbar with guaranteed zero yellow"""
    return SnackBar(
        content=Text(message, color=ZeroYellowTheme.TEXT_PRIMARY),
        bgcolor=ZeroYellowTheme.BG_TERTIARY,
        action="OK",
        action_color=ZeroYellowTheme.ACCENT_PRIMARY
    )

def zero_yellow_alert_dialog(title, content, actions):
    """Alert dialog with guaranteed zero yellow"""
    return AlertDialog(
        modal=True,
        title=Text(title, color=ZeroYellowTheme.TEXT_PRIMARY),
        content=content,
        actions=actions,
        bgcolor=ZeroYellowTheme.BG_TERTIARY,
        title_text_style=TextStyle(color=ZeroYellowTheme.TEXT_PRIMARY),
        content_text_style=TextStyle(color=ZeroYellowTheme.TEXT_PRIMARY)
    )

def zero_yellow_dropdown(options, value=None, on_change=None, label="", **kwargs):
    """Dropdown with guaranteed zero yellow"""
    return Dropdown(
        options=options,
        value=value,
        on_change=on_change,
        label=label,
        bgcolor=ZeroYellowTheme.BG_TERTIARY,
        color=ZeroYellowTheme.TEXT_PRIMARY,
        border_color=ZeroYellowTheme.GLASS_BORDER,
        focused_border_color=ZeroYellowTheme.ACCENT_PRIMARY,
        text_style=TextStyle(color=ZeroYellowTheme.TEXT_PRIMARY),
        label_style=TextStyle(color=ZeroYellowTheme.TEXT_SECONDARY),
        **kwargs
    )

# Nuclear Page Configuration - Completely Custom
def configure_zero_yellow_page(page):
    """Configure page with absolute zero yellow guarantee"""
    # Set basic page properties
    page.bgcolor = ZeroYellowTheme.BG_PRIMARY
    page.theme_mode = ThemeMode.DARK
    
    # Create completely custom theme that overrides EVERYTHING
    page.theme = Theme(
        use_material3=False,  # Disable Material 3 completely
        color_scheme_seed=ZeroYellowTheme.PURE_BLACK,  # Use black instead of any default
        # Create a completely custom color scheme with NO yellow
        color_scheme=ColorScheme(
            primary=ZeroYellowTheme.PURE_WHITE,
            on_primary=ZeroYellowTheme.PURE_BLACK,
            primary_container=ZeroYellowTheme.BG_TERTIARY,
            on_primary_container=ZeroYellowTheme.TEXT_PRIMARY,
            secondary=ZeroYellowTheme.TEXT_SECONDARY,
            on_secondary=ZeroYellowTheme.BG_PRIMARY,
            secondary_container=ZeroYellowTheme.BG_QUATERNARY,
            on_secondary_container=ZeroYellowTheme.TEXT_PRIMARY,
            tertiary=ZeroYellowTheme.TEXT_TERTIARY,
            on_tertiary=ZeroYellowTheme.BG_PRIMARY,
            tertiary_container=ZeroYellowTheme.BG_GLASS,
            on_tertiary_container=ZeroYellowTheme.TEXT_PRIMARY,
            error=ZeroYellowTheme.ERROR,
            on_error=ZeroYellowTheme.PURE_WHITE,
            error_container=ZeroYellowTheme.ERROR,
            on_error_container=ZeroYellowTheme.PURE_WHITE,
            background=ZeroYellowTheme.BG_PRIMARY,
            on_background=ZeroYellowTheme.TEXT_PRIMARY,
            surface=ZeroYellowTheme.BG_SECONDARY,
            on_surface=ZeroYellowTheme.TEXT_PRIMARY,
            surface_variant=ZeroYellowTheme.BG_TERTIARY,
            on_surface_variant=ZeroYellowTheme.TEXT_SECONDARY,
            outline=ZeroYellowTheme.GLASS_BORDER,
            outline_variant=ZeroYellowTheme.GLASS_BORDER,
            shadow=ZeroYellowTheme.GLASS_SHADOW,
            scrim=ZeroYellowTheme.PURE_BLACK,
            inverse_surface=ZeroYellowTheme.PURE_WHITE,
            on_inverse_surface=ZeroYellowTheme.PURE_BLACK,
            inverse_primary=ZeroYellowTheme.TEXT_PRIMARY,
            surface_tint=ZeroYellowTheme.BG_GLASS
        ),
        # Override scrollbar to prevent yellow
        scrollbar_theme=ScrollbarTheme(
            thumb_color=ZeroYellowTheme.TEXT_QUATERNARY,
            track_color=ZeroYellowTheme.BG_TERTIARY,
            track_border_color=ZeroYellowTheme.GLASS_BORDER,
        )
    )
    
    return page

# Legacy component aliases for backward compatibility
glass_container = zero_yellow_container
primary_button = lambda text, on_click=None, **kwargs: zero_yellow_button(text, on_click, True, **kwargs)
secondary_button = lambda text, on_click=None, **kwargs: zero_yellow_button(text, on_click, False, **kwargs)
modern_text_field = zero_yellow_text_field
def heading_text(text, size=24, color=None, **kwargs):
    """Legacy heading_text function with zero yellow"""
    return zero_yellow_text(
        text,
        size=size,
        weight=FontWeight.BOLD,
        color=color or ZeroYellowTheme.TEXT_PRIMARY,
        **kwargs
    )
def body_text(text, size=14, color=None, **kwargs):
    """Legacy body_text function with zero yellow"""
    return zero_yellow_text(
        text,
        size=size,
        color=color or ZeroYellowTheme.TEXT_PRIMARY,
        **kwargs
    )
def caption_text(text, size=12, color=None, **kwargs):
    """Legacy caption_text function with zero yellow"""
    return zero_yellow_text(
        text,
        size=size,
        color=color or ZeroYellowTheme.TEXT_PRIMARY,
        **kwargs
    )
def modern_icon(name=None, icon=None, size=24, color=None, **kwargs):
    """Legacy modern_icon function with zero yellow"""
    icon_value = name or icon  # Support both 'name' and 'icon' parameters
    return zero_yellow_icon(icon_value, size, color, **kwargs)
modern_data_table = zero_yellow_data_table
modern_card = zero_yellow_container
modern_nav_bar = zero_yellow_container
def stat_card(title, value, icon_name, icon_color):
    """Create a stat card with zero yellow styling"""
    return zero_yellow_container(
        content=Column([
            Row([
                zero_yellow_icon(icon=icon_name, size=24, color=icon_color),
                zero_yellow_text(title, size=14, color=ZeroYellowTheme.TEXT_SECONDARY),
            ], alignment=MainAxisAlignment.SPACE_BETWEEN),
            Container(height=10),
            zero_yellow_text(str(value), size=20, weight=FontWeight.BOLD, color=ZeroYellowTheme.TEXT_PRIMARY),
        ]),
        width=200,
        height=100,
        padding=15
    )

# Update the configure_app_theme to use the new system
configure_app_theme = configure_zero_yellow_page

# Update IOS26Theme to point to ZeroYellowTheme for compatibility
class IOS26Theme:
    """Legacy theme class pointing to ZeroYellowTheme for backward compatibility"""
    BACKGROUND_PRIMARY = ZeroYellowTheme.BG_PRIMARY
    BACKGROUND_SECONDARY = ZeroYellowTheme.BG_SECONDARY
    BACKGROUND_TERTIARY = ZeroYellowTheme.BG_TERTIARY
    BACKGROUND_QUATERNARY = ZeroYellowTheme.BG_QUATERNARY
    
    TEXT_PRIMARY = ZeroYellowTheme.TEXT_PRIMARY
    TEXT_SECONDARY = ZeroYellowTheme.TEXT_SECONDARY
    TEXT_TERTIARY = ZeroYellowTheme.TEXT_TERTIARY
    TEXT_QUATERNARY = ZeroYellowTheme.TEXT_QUATERNARY
    TEXT_DISABLED = ZeroYellowTheme.TEXT_DISABLED
    
    ACCENT_PRIMARY = ZeroYellowTheme.ACCENT_PRIMARY
    ACCENT_SECONDARY = ZeroYellowTheme.ACCENT_SECONDARY
    ACCENT_TERTIARY = ZeroYellowTheme.ACCENT_TERTIARY
    ACCENT_QUATERNARY = ZeroYellowTheme.ACCENT_QUATERNARY
    
    GLASS_BACKGROUND = ZeroYellowTheme.GLASS_BG
    GLASS_BORDER = ZeroYellowTheme.GLASS_BORDER
    GLASS_SHADOW = ZeroYellowTheme.GLASS_SHADOW
    
    HOVER_COLOR = ZeroYellowTheme.HOVER
    FOCUS_COLOR = ZeroYellowTheme.FOCUS
    SELECTION_COLOR = ZeroYellowTheme.SELECTED
    ERROR = ZeroYellowTheme.ERROR
    SUCCESS = ZeroYellowTheme.SUCCESS
    WARNING = ZeroYellowTheme.WARNING