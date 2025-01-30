# steps/region_step.py
import tkinter as tk
from tkinter import ttk
from steps import Step
from helpers.error_handlers import ErrorHandler
from helpers.validation import ValidationHelper
from helpers.ui_helpers import UIHelper
from styles import StyleConfig

class RegionStep(Step):
    _order = 10

    def __init__(self, frame, title):
        super().__init__(frame, title)
        self.region_container = None
        self.region_options = None
        self.selected_region = tk.StringVar()
        self.region_info_label = None

    @ErrorHandler.handle_exception_decorator
    def create_widgets(self) -> ttk.Frame:
        """
        Create and return the main widget container for the step.
        Required implementation of abstract method from Step base class.
        """
        # Create main container with reduced padding
        self.region_container = ttk.Frame(self.frame)
        self.region_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create a central content frame for vertical centering
        spacer_top = ttk.Frame(self.region_container)
        spacer_top.pack(expand=True)

        content_frame = ttk.Frame(self.region_container)
        content_frame.pack(expand=False)

        # Create header label with reduced padding
        header_label = ttk.Label(
            content_frame,
            text="Select Your Region:",
            style="Header.TLabel"
        )
        header_label.pack(pady=(0, 3))

        # Create radio buttons for region options
        self.region_options = {
            "North America": {
                "factor": 1.0,
                "desc": "Average bowel habits in North America",
                "icon": "🌎",
                "details": "Typical diet and lifestyle",
                "impact": "No significant impact",
                "tips": "Maintain a balanced diet"
            },
            "Europe": {
                "factor": 1.1,
                "desc": "Slightly higher regularity in Europe",
                "icon": "🌍",
                "details": "Higher fiber intake in typical diet",
                "impact": "May increase regularity",
                "tips": "Continue with a fiber-rich diet"
            },
            "Asia": {
                "factor": 0.9,
                "desc": "Slightly lower regularity in Asia",
                "icon": "🌏",
                "details": "Different dietary habits",
                "impact": "May decrease regularity",
                "tips": "Consider adding more fiber"
            }
        }

        # Create radio buttons frame with compact spacing
        radio_frame = ttk.Frame(content_frame)
        radio_frame.pack(fill=tk.X, pady=3)

        for option, details in self.region_options.items():
            radio_btn = ttk.Radiobutton(
                radio_frame,
                text=f"{details['icon']} {option}",
                variable=self.selected_region,
                value=option,
                command=self.on_region_change
            )
            radio_btn.pack(anchor=tk.W, pady=1)  # Reduced padding between radio buttons

        # Create info label with specific width and reduced padding
        self.region_info_label = UIHelper.create_info_label(
            content_frame,
            "🌍 Regional dietary patterns can affect:\n"
            "• Bowel movement frequency\n"
            "• Digestive health\n"
            "• Overall regularity",
            wraplength=300
        )
        self.region_info_label.pack(pady=5)

        spacer_bottom = ttk.Frame(self.region_container)
        spacer_bottom.pack(expand=True)

        # Set default selection
        self.selected_region.set("North America")
        self.on_region_change()

        return self.region_container

    @ErrorHandler.handle_exception_decorator
    def on_region_change(self):
        """Handle region selection changes."""
        selected_option = self.selected_region.get()
        if selected_option in self.region_options:
            details = self.region_options[selected_option]
            info_text = (
                f"{details['icon']} {selected_option}\n"  # Simplified header
                f"{details['desc']}\n"  # Removed "Description:" prefix
                f"Impact: {details['impact']}\n"
                f"Tip: {details['tips']}"  # Changed "Tips:" to "Tip:"
            )
            self.region_info_label.configure(text=info_text)

    @ErrorHandler.handle_exception_decorator
    def store_input(self) -> dict:
        """Store and return the step's input data."""
        selected_option = self.selected_region.get()
        return {
            "region": {
                "selection": selected_option,
                "factor": self.region_options[selected_option]["factor"],
                "details": self.region_options[selected_option]
            }
        }

    def validate(self) -> bool:
        """Validate the region selection."""
        if not self.selected_region.get():
            ErrorHandler.show_error("Please select your region")
            return False
        return True