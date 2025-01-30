# steps/poop_size_step.py
import tkinter as tk
from tkinter import ttk
from steps import Step
from helpers.error_handlers import ErrorHandler
from helpers.validation import ValidationHelper
from helpers.ui_helpers import UIHelper
from styles import StyleConfig

class PoopSizeStep(Step):
    _order = 3

    def __init__(self, frame, title):
        super().__init__(frame, title)
        self.poop_size_container = None
        self.poop_size_label = None
        self.poop_size_var = None
        self.poop_size_options = {}
        self.poop_size_dropdown = None
        self.poop_size_info_label = None

    @ErrorHandler.handle_exception_decorator
    def create_widgets(self) -> ttk.Frame:
        """
        Create and return the main widget container for the step.
        Required implementation of abstract method from Step base class.
        """
        # Create main container with reduced padding
        self.poop_size_container = ttk.Frame(self.frame)
        self.poop_size_container.pack(pady=5, fill=tk.BOTH, expand=True, padx=5)

        # Create a central content frame for vertical centering
        spacer_top = ttk.Frame(self.poop_size_container)
        spacer_top.pack(expand=True)

        content_frame = ttk.Frame(self.poop_size_container)
        content_frame.pack(expand=False)

        # Create poop size label with reduced padding
        self.poop_size_label = ttk.Label(
            content_frame,
            text="Poop Size:",
            style="Header.TLabel"
        )
        self.poop_size_label.pack(pady=(0, 3))

        # Create poop size options dropdown with specific width
        self.poop_size_var = tk.StringVar()
        self.poop_size_dropdown = ttk.Combobox(
            content_frame,
            textvariable=self.poop_size_var,
            state='readonly',
            width=25  # Set specific width
        )
        self.poop_size_dropdown.pack(pady=3)

        # Populate poop size options
        self.poop_size_options = {
            "💩 Small": {
                "factor": 0.8,
                "desc": "Small poop size",
                "impact": "10% decrease in regularity",
                "recommendation": "Increase fiber intake",
                "details": "Small poop may indicate insufficient fiber",
                "tips": "Add more fruits, vegetables, and whole grains to your diet"
            },
            "💩 Average": {
                "factor": 1.0,
                "desc": "Average poop size",
                "impact": "No significant impact",
                "recommendation": "Maintain current diet",
                "details": "Average poop size is typical for a balanced diet",
                "tips": "Continue with a varied and fiber-rich diet"
            },
            "💩 Large": {
                "factor": 1.2,
                "desc": "Large poop size",
                "impact": "15% increase in regularity",
                "recommendation": "Stay hydrated",
                "details": "Large poop may indicate efficient digestion",
                "tips": "Ensure adequate hydration and monitor bowel movements"
            }
        }

        self.poop_size_dropdown['values'] = list(self.poop_size_options.keys())
        self.poop_size_var.set(list(self.poop_size_options.keys())[1])  # Default to "Average"

        # Create poop size tips label with specific width and reduced padding
        self.poop_size_info_label = UIHelper.create_info_label(
            content_frame,
            "💩 Tips for maintaining healthy poop size:\n"
            "• Eat a fiber-rich diet\n"
            "• Stay hydrated\n"
            "• Exercise regularly",
            wraplength=300
        )
        self.poop_size_info_label.pack(pady=5)

        spacer_bottom = ttk.Frame(self.poop_size_container)
        spacer_bottom.pack(expand=True)

        # Bind dropdown change event
        self.poop_size_dropdown.bind('<<ComboboxSelected>>', self.on_poop_size_change)

        return self.poop_size_container

    @ErrorHandler.handle_exception_decorator
    def on_poop_size_change(self, event):
        selected_option = self.poop_size_var.get()
        option_data = self.poop_size_options.get(selected_option, {})
        if option_data:
            # Display additional information with simplified format
            info_text = (
                f"{selected_option}\n"  # Removed "Selected:" prefix
                f"{option_data['desc']}\n"  # Removed "Description:" prefix
                f"Impact: {option_data['impact']}\n"
                f"Tip: {option_data['recommendation']}"  # Changed "Recommendation:" to "Tip:"
            )
            self.poop_size_info_label.configure(text=info_text)

    @ErrorHandler.handle_exception_decorator
    def store_input(self) -> dict:
        """Store and return the step's input data."""
        selected_option = self.poop_size_var.get()
        return {
            "poop_size": {
                "selection": selected_option,
                "data": self.poop_size_options[selected_option]
            }
        }

    def validate(self) -> bool:
        """Validate the poop size selection."""
        is_valid, message = ValidationHelper.validate_selection(
            self.poop_size_var.get(),
            list(self.poop_size_options.keys()),
            "poop size"
        )
        
        if not is_valid:
            ErrorHandler.show_error(message)
            return False
        return True