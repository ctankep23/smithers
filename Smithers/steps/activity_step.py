# steps/activity_step.py
import tkinter as tk
from tkinter import ttk
from steps import Step
from helpers.error_handlers import ErrorHandler
from helpers.validation import ValidationHelper
from helpers.ui_helpers import UIHelper
from styles import StyleConfig

class ActivityStep(Step):
    _order = 11

    def __init__(self, frame, title):
        super().__init__(frame, title)
        self.activity_container = None
        self.activity_label = None
        self.activity_var = None
        self.activity_options = {}
        self.activity_dropdown = None
        self.activity_info_label = None

    @ErrorHandler.handle_exception_decorator
    def create_widgets(self) -> ttk.Frame:
        """
        Create and return the main widget container for the step.
        Required implementation of abstract method from Step base class.
        """
        # Create main container with reduced padding
        self.activity_container = ttk.Frame(self.frame)
        self.activity_container.pack(pady=5, fill=tk.BOTH, expand=True, padx=5)

        # Create top spacer for vertical centering
        spacer_top = ttk.Frame(self.activity_container)
        spacer_top.pack(expand=True)

        # Create central content frame
        content_frame = ttk.Frame(self.activity_container)
        content_frame.pack(expand=False)

        # Create activity label with reduced padding
        self.activity_label = ttk.Label(
            content_frame,  # Changed parent to content_frame
            text="Activity Level:",
            style="Header.TLabel"
        )
        self.activity_label.pack(pady=(0, 3))

        # Create activity options dropdown with specific width
        self.activity_var = tk.StringVar()
        self.activity_dropdown = ttk.Combobox(
            content_frame,  # Changed parent to content_frame
            textvariable=self.activity_var,
            state='readonly',
            width=25
        )
        self.activity_dropdown.pack(pady=3)

        # Populate activity options
        self.activity_options = {
            "🧘 Sedentary": {
                "factor": 0.8,
                "desc": "Low physical activity",
                "impact": "10% decrease in regularity",
                "recommendation": "Consider light exercise",
                "details": "Low activity may slow digestion",
                "tips": "Take short walks throughout the day"
            },
            "🏃 Active": {
                "factor": 1.0,
                "desc": "Moderate physical activity",
                "impact": "No significant impact",
                "recommendation": "Maintain current activity level",
                "details": "Regular exercise supports healthy digestion",
                "tips": "Incorporate daily exercise routines"
            },
            "🏋️ Very Active": {
                "factor": 1.2,
                "desc": "High physical activity",
                "impact": "15% increase in regularity",
                "recommendation": "Stay hydrated",
                "details": "High activity promotes efficient digestion",
                "tips": "Ensure adequate hydration during workouts"
            }
        }

        self.activity_dropdown['values'] = list(self.activity_options.keys())
        self.activity_var.set(list(self.activity_options.keys())[1])  # Default to "Active"

        # Create activity tips label
        self.activity_info_label = UIHelper.create_info_label(
            content_frame,  # Changed parent to content_frame
            "🏃 Tips for maintaining activity:\n"
            "• Incorporate daily exercise\n"
            "• Take regular breaks during work\n"
            "• Stay hydrated",
            wraplength=300
        )
        self.activity_info_label.pack(pady=5)

        # Create bottom spacer for vertical centering
        spacer_bottom = ttk.Frame(self.activity_container)
        spacer_bottom.pack(expand=True)

        # Bind dropdown change event
        self.activity_dropdown.bind('<<ComboboxSelected>>', self.on_activity_change)

        return self.activity_container

    @ErrorHandler.handle_exception_decorator
    def on_activity_change(self, event):
        selected_option = self.activity_var.get()
        option_data = self.activity_options.get(selected_option, {})
        if option_data:
            # Display additional information with simplified format
            info_text = (
                f"{selected_option}\n"  # Removed "Selected:" prefix
                f"{option_data['desc']}\n"  # Removed "Description:" prefix
                f"Impact: {option_data['impact']}\n"
                f"Tip: {option_data['recommendation']}"  # Changed "Recommendation:" to "Tip:"
            )
            self.activity_info_label.configure(text=info_text)

    @ErrorHandler.handle_exception_decorator
    def store_input(self) -> dict:
        """Store and return the step's input data."""
        selected_option = self.activity_var.get()
        return {
            "activity_level": {
                "selection": selected_option,
                "data": self.activity_options[selected_option]
            }
        }

    def validate(self) -> bool:
        """Validate the activity level selection."""
        is_valid, message = ValidationHelper.validate_selection(
            self.activity_var.get(),
            list(self.activity_options.keys()),
            "activity level"
        )
        
        if not is_valid:
            ErrorHandler.show_error(message)
            return False
        return True