# styles.py
from tkinter import ttk

class StyleConfig:
    # Color scheme
    COLOR_PRIMARY = "#2563eb"    # Modern blue
    COLOR_SECONDARY = "#1e40af"   # Darker blue
    COLOR_ACCENT = "#3b82f6"     # Lighter blue
    COLOR_BACKGROUND = "#f8fafc"  # Clean white
    COLOR_TEXT = "#1e293b"       # Dark gray

    # Font configurations
    FONT_FAMILY = "Helvetica"
    FONT_SIZES = {
        "small": 9,
        "regular": 10,
        "large": 12,
        "title": 14,
        "xlarge": 16  # Added this for consistency with other code
    }
    
    # Add these for direct access (to match existing code references)
    FONT_SIZE_SMALL = FONT_SIZES["small"]
    FONT_SIZE_NORMAL = FONT_SIZES["regular"]
    FONT_SIZE_LARGE = FONT_SIZES["large"]
    FONT_SIZE_XLARGE = FONT_SIZES["xlarge"]

    @classmethod
    def configure_styles(cls):
        style = ttk.Style()
        
        # Use the built-in 'clam' theme as base
        style.theme_use('clam')

        # Configure main styles
        style.configure('TFrame',
            background=cls.COLOR_BACKGROUND
        )

        # Basic label style
        style.configure('TLabel',
            background=cls.COLOR_BACKGROUND,
            foreground=cls.COLOR_TEXT,
            font=(cls.FONT_FAMILY, cls.FONT_SIZES["regular"])
        )

        # Header label style
        style.configure('Header.TLabel',
            font=(cls.FONT_FAMILY, cls.FONT_SIZES["large"], 'bold')
        )

        # Title label style
        style.configure('Title.TLabel',
            font=(cls.FONT_FAMILY, cls.FONT_SIZES["title"], 'bold')
        )

        # Description label style
        style.configure('Description.TLabel',
            font=(cls.FONT_FAMILY, cls.FONT_SIZES["regular"]),
            wraplength=300,
            justify='left'
        )

        # Button styles
        style.configure('TButton',
            background=cls.COLOR_PRIMARY,
            foreground='white',
            padding=10,
            font=(cls.FONT_FAMILY, cls.FONT_SIZES["regular"]),
            borderwidth=0
        )

        style.map('TButton',
            background=[('active', cls.COLOR_SECONDARY)],
            foreground=[('active', 'white')]
        )

        # Radio button style
        style.configure('TRadiobutton',
            background=cls.COLOR_BACKGROUND,
            foreground=cls.COLOR_TEXT,
            font=(cls.FONT_FAMILY, cls.FONT_SIZES["regular"])
        )

        # Checkbox style
        style.configure('TCheckbutton',
            background=cls.COLOR_BACKGROUND,
            foreground=cls.COLOR_TEXT,
            font=(cls.FONT_FAMILY, cls.FONT_SIZES["regular"])
        )

        # Combobox style
        style.configure('TCombobox',
            background=cls.COLOR_BACKGROUND,
            foreground=cls.COLOR_TEXT,
            fieldbackground=cls.COLOR_BACKGROUND,
            font=(cls.FONT_FAMILY, cls.FONT_SIZES["regular"])
        )

        # Scale (slider) style
        style.configure('TScale',
            background=cls.COLOR_BACKGROUND,
            troughcolor=cls.COLOR_PRIMARY,
            sliderrelief='flat',
            sliderlength=15,
            sliderthickness=15,
            troughheight=10
        )

        # Progress style
        style.configure('Progress.TLabel',
            font=(cls.FONT_FAMILY, cls.FONT_SIZES["small"]),
            foreground=cls.COLOR_SECONDARY
        )

        # Results frame style
        style.configure('Results.TFrame',
            background=cls.COLOR_BACKGROUND,
            relief='solid',
            borderwidth=1
        )

        # Text widget style (for results)
        style.configure('Results.TText',
            background=cls.COLOR_BACKGROUND,
            foreground=cls.COLOR_TEXT,
            font=(cls.FONT_FAMILY, cls.FONT_SIZES["regular"]),
            padx=10,
            pady=10
        )

        # Progress indicator styles
        style.configure('Progress.TLabel',
            font=(cls.FONT_FAMILY, cls.FONT_SIZES["small"]),
            foreground=cls.COLOR_SECONDARY,
            background=cls.COLOR_BACKGROUND
        )

        style.configure('TProgressbar',
            background=cls.COLOR_PRIMARY,
            troughcolor=cls.COLOR_BACKGROUND,
            borderwidth=0,
            thickness=6
        )

    @classmethod
    def get_text_widget_config(cls):
        """Return configuration for Text widgets (which can't use ttk styles)"""
        return {
            'font': (cls.FONT_FAMILY, cls.FONT_SIZES["regular"]),
            'bg': cls.COLOR_BACKGROUND,
            'fg': cls.COLOR_TEXT,
            'padx': 10,
            'pady': 10,
            'wrap': 'word'
        }

    @classmethod
    def get_label_config(cls, style_type="regular"):
        """Return configuration for labels"""
        return {
            'font': (cls.FONT_FAMILY, cls.FONT_SIZES[style_type]),
            'background': cls.COLOR_BACKGROUND,
            'foreground': cls.COLOR_TEXT
        }