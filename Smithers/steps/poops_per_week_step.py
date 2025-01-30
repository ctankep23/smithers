# steps/poops_per_week_step.py
import tkinter as tk
from tkinter import ttk
from steps import Step
from helpers.error_handlers import ErrorHandler
from helpers.validation import ValidationHelper
from helpers.ui_helpers import UIHelper
from styles import StyleConfig

class PoopsPerWeekStep(Step):
    _order = 2

    def __init__(self, frame, title):
        super().__init__(frame, title)
        self.poops_per_week_container = None
        self.poops_per_week_label = None
        self.poops_per_week_var = None
        self.poops_per_week_options = {}
        self.poops_per_week_dropdown = None
        self.poops_per_week_info_label = None

    @ErrorHandler.handle_exception_decorator
    def create_widgets(self) -> ttk.Frame:
        """
        Create and return the main widget container for the step.
        Required implementation of abstract method from Step base class.
        """
        # Create main container with reduced padding
        self.poops_per_week_container = ttk.Frame(self.frame)
        self.poops_per_week_container.pack(pady=5, fill=tk.BOTH, expand=True, padx=5)

        # Create a central content frame for vertical centering
        spacer_top = ttk.Frame(self.poops_per_week_container)
        spacer_top.pack(expand=True)

        content_frame = ttk.Frame(self.poops_per_week_container)
        content_frame.pack(expand=False)

        # Create poops per week label with reduced padding
        self.poops_per_week_label = ttk.Label(
            content_frame,
            text="Poops Per Week:",
            style="Header.TLabel"
        )
        self.poops_per_week_label.pack(pady=(0, 3))

        # Create poops per week options dropdown with specific width
        self.poops_per_week_var = tk.StringVar()
        self.poops_per_week_dropdown = ttk.Combobox(
            content_frame,
            textvariable=self.poops_per_week_var,
            state='readonly',
            width=25  # Set specific width
        )
        self.poops_per_week_dropdown.pack(pady=3)

        # Populate poops per week options
        self.poops_per_week_options = {
            "💩 1-2 times": {
                "factor": 0.8,
                "desc": "Infrequent bowel movements",
                "impact": "10% decrease in regularity",
                "recommendation": "Increase fiber intake",
                "details": "Infrequent poops may indicate constipation",
                "tips": "Add more fruits, vegetables, and whole grains to your diet"
            },
            "💩 3-5 times": {
                "factor": 1.0,
                "desc": "Average bowel movements",
                "impact": "No significant impact",
                "recommendation": "Maintain current diet",
                "details": "Average poops align with healthy digestion",
                "tips": "Continue with a varied and fiber-rich diet"
            },
            "💩 6+ times": {
                "factor": 1.2,
                "desc": "Frequent bowel movements",
                "impact": "15% increase in regularity",
                "recommendation": "Stay hydrated",
                "details": "Frequent poops may indicate efficient digestion",
                "tips": "Ensure adequate hydration and monitor bowel movements"
            }
        }

        self.poops_per_week_dropdown['values'] = list(self.poops_per_week_options.keys())
        self.poops_per_week_var.set(list(self.poops_per_week_options.keys())[1])  # Default to "3-5 times"

        # Create poops per week tips label with specific width and reduced padding
        self.poops_per_week_info_label = UIHelper.create_info_label(
            content_frame,
            "💩 Tips for maintaining healthy bowel movements:\n"
            "• Stay hydrated\n"
            "• Eat a fiber-rich diet\n"
            "• Exercise regularly",
            wraplength=300
        )
        self.poops_per_week_info_label.pack(pady=5)

        spacer_bottom = ttk.Frame(self.poops_per_week_container)
        spacer_bottom.pack(expand=True)

        # Bind dropdown change event
        self.poops_per_week_dropdown.bind('<<ComboboxSelected>>', self.on_poops_per_week_change)

        return self.poops_per_week_container

    @ErrorHandler.handle_exception_decorator
    def on_poops_per_week_change(self, event):
        selected_option = self.poops_per_week_var.get()
        option_data = self.poops_per_week_options.get(selected_option, {})
        if option_data:
            # Display additional information with simplified format
            info_text = (
                f"{selected_option}\n"  # Removed "Selected:" prefix
                f"{option_data['desc']}\n"  # Removed "Description:" prefix
                f"Impact: {option_data['impact']}\n"
                f"Tip: {option_data['recommendation']}"  # Changed "Recommendation:" to "Tip:"
            )
            self.poops_per_week_info_label.configure(text=info_text)

    @ErrorHandler.handle_exception_decorator
    def store_input(self) -> dict:
        """Store and return the step's input data."""
        selected_option = self.poops_per_week_var.get()
        return {
            "poops_per_week": {
                "selection": selected_option,
                "data": self.poops_per_week_options[selected_option]
            }
        }

    def validate(self) -> bool:
        """Validate the poops per week selection."""
        is_valid, message = ValidationHelper.validate_selection(
            self.poops_per_week_var.get(),
            list(self.poops_per_week_options.keys()),
            "poops per week"
        )
        
        if not is_valid:
            ErrorHandler.show_error(message)
            return False
        return True