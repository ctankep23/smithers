# steps/gender_step.py
import tkinter as tk
from tkinter import ttk
from steps import Step
from helpers.error_handlers import ErrorHandler
from helpers.validation import ValidationHelper
from helpers.ui_helpers import UIHelper
from styles import StyleConfig

class GenderStep(Step):
    _order = 6

    def __init__(self, frame, title):
        super().__init__(frame, title)
        self.gender_container = None
        self.gender_label = None
        self.gender_var = None
        self.gender_options = {}
        self.gender_dropdown = None
        self.gender_info_label = None

    @ErrorHandler.handle_exception_decorator
    def create_widgets(self) -> ttk.Frame:
        """
        Create and return the main widget container for the step.
        Required implementation of abstract method from Step base class.
        """
        # Create main container with reduced padding
        self.gender_container = ttk.Frame(self.frame)
        self.gender_container.pack(pady=5, fill=tk.BOTH, expand=True, padx=5)

        # Create a central content frame for vertical centering
        spacer_top = ttk.Frame(self.gender_container)
        spacer_top.pack(expand=True)

        content_frame = ttk.Frame(self.gender_container)
        content_frame.pack(expand=False)

        # Create gender label with reduced padding
        self.gender_label = ttk.Label(
            content_frame,
            text="Gender:",
            style="Header.TLabel"
        )
        self.gender_label.pack(pady=(0, 3))

        # Create gender options dropdown with specific width
        self.gender_var = tk.StringVar()
        self.gender_dropdown = ttk.Combobox(
            content_frame,
            textvariable=self.gender_var,
            state='readonly',
            width=25  # Set specific width
        )
        self.gender_dropdown.pack(pady=3)

        # Populate gender options
        self.gender_options = {
            "♂ Male": {
                "factor": 1.0,
                "desc": "Male",
                "impact": "No significant impact",
                "recommendation": "Maintain a balanced diet",
                "details": "Male digestion typically aligns with general guidelines",
                "tips": "Stay hydrated and maintain a varied diet"
            },
            "♀ Female": {
                "factor": 1.0,
                "desc": "Female",
                "impact": "No significant impact",
                "recommendation": "Monitor hormonal changes",
                "details": "Female digestion may vary with hormonal cycles",
                "tips": "Consider dietary adjustments during different phases"
            },
            "⚧ Non-Binary/Other": {
                "factor": 1.0,
                "desc": "Non-Binary/Other",
                "impact": "No significant impact",
                "recommendation": "Focus on personal health needs",
                "details": "Individual digestion varies regardless of gender",
                "tips": "Personalize your diet based on your specific needs"
            }
        }

        self.gender_dropdown['values'] = list(self.gender_options.keys())
        self.gender_var.set(list(self.gender_options.keys())[0])  # Default to "Male"

        # Create gender tips label with specific width and reduced padding
        self.gender_info_label = UIHelper.create_info_label(
            content_frame,
            "💡 General dietary tips:\n"
            "• Stay hydrated\n"
            "• Eat a balanced diet\n"
            "• Incorporate fiber-rich foods",
            wraplength=300
        )
        self.gender_info_label.pack(pady=5)

        spacer_bottom = ttk.Frame(self.gender_container)
        spacer_bottom.pack(expand=True)

        # Bind dropdown change event
        self.gender_dropdown.bind('<<ComboboxSelected>>', self.on_gender_change)

        return self.gender_container

    @ErrorHandler.handle_exception_decorator
    def on_gender_change(self, event):
        selected_option = self.gender_var.get()
        option_data = self.gender_options.get(selected_option, {})
        if option_data:
            # Display additional information with simplified format
            info_text = (
                f"{selected_option}\n"  # Removed "Selected:" prefix
                f"{option_data['desc']}\n"  # Removed "Description:" prefix
                f"Impact: {option_data['impact']}\n"
                f"Tip: {option_data['recommendation']}"  # Changed "Recommendation:" to "Tip:"
            )
            self.gender_info_label.configure(text=info_text)

    @ErrorHandler.handle_exception_decorator
    def store_input(self) -> dict:
        """Store and return the step's input data."""
        selected_option = self.gender_var.get()
        return {
            "gender": {
                "selection": selected_option,
                "data": self.gender_options[selected_option]
            }
        }

    def validate(self) -> bool:
        """Validate the gender selection."""
        is_valid, message = ValidationHelper.validate_selection(
            self.gender_var.get(),
            list(self.gender_options.keys()),
            "gender"
        )
        
        if not is_valid:
            ErrorHandler.show_error(message)
            return False
        return True