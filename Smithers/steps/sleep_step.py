# steps/sleep_step.py
import tkinter as tk
from tkinter import ttk
from steps import Step
from helpers.error_handlers import ErrorHandler
from helpers.validation import ValidationHelper
from helpers.ui_helpers import UIHelper
from styles import StyleConfig

class SleepStep(Step):
    _order = 8

    def __init__(self, frame, title):
        super().__init__(frame, title)
        self.sleep_container = None
        self.sleep_label = None
        self.sleep_var = None
        self.sleep_options = {}
        self.sleep_dropdown = None
        self.sleep_info_label = None

    @ErrorHandler.handle_exception_decorator
    def create_widgets(self) -> ttk.Frame:
        """
        Create and return the main widget container for the step.
        Required implementation of abstract method from Step base class.
        """
        # Create main container with reduced padding
        self.sleep_container = ttk.Frame(self.frame)
        self.sleep_container.pack(pady=5, fill=tk.BOTH, expand=True, padx=5)

        # Create a central content frame for vertical centering
        spacer_top = ttk.Frame(self.sleep_container)
        spacer_top.pack(expand=True)

        content_frame = ttk.Frame(self.sleep_container)
        content_frame.pack(expand=False)

        # Create sleep label with reduced padding
        self.sleep_label = ttk.Label(
            content_frame,
            text="Sleep Pattern:",
            style="Header.TLabel"
        )
        self.sleep_label.pack(pady=(0, 3))

        # Create sleep options dropdown with specific width
        self.sleep_var = tk.StringVar()
        self.sleep_dropdown = ttk.Combobox(
            content_frame,
            textvariable=self.sleep_var,
            state='readonly',
            width=25  # Set specific width
        )
        self.sleep_dropdown.pack(pady=3)

        # Populate sleep options
        self.sleep_options = {
            "🌙 Less than 6 hours": {
                "factor": 0.8,
                "desc": "Short sleep duration",
                "impact": "10% decrease in regularity",
                "recommendation": "Consider improving sleep hygiene",
                "details": "Short sleep may affect digestion",
                "tips": "Aim for 7-9 hours of sleep per night"
            },
            "🌙 6-8 hours": {
                "factor": 1.0,
                "desc": "Average sleep duration",
                "impact": "No significant impact",
                "recommendation": "Maintain consistent sleep schedule",
                "details": "Average sleep aligns with health guidelines",
                "tips": "Stick to a regular bedtime routine"
            },
            "🌙 More than 8 hours": {
                "factor": 1.2,
                "desc": "Extended sleep duration",
                "impact": "5% increase in regularity",
                "recommendation": "Monitor energy levels",
                "details": "Longer sleep may improve digestion",
                "tips": "Ensure sleep quality remains good"
            }
        }

        self.sleep_dropdown['values'] = list(self.sleep_options.keys())
        self.sleep_var.set(list(self.sleep_options.keys())[1])  # Default to "6-8 hours"

        # Create sleep tips label with specific width and reduced padding
        self.sleep_info_label = UIHelper.create_info_label(
            content_frame,
            "🌟 Tips for better sleep:\n"
            "• Maintain a consistent schedule\n"
            "• Avoid screens before bedtime\n"
            "• Create a relaxing bedtime routine",
            wraplength=300
        )
        self.sleep_info_label.pack(pady=5)

        spacer_bottom = ttk.Frame(self.sleep_container)
        spacer_bottom.pack(expand=True)

        # Bind dropdown change event
        self.sleep_dropdown.bind('<<ComboboxSelected>>', self.on_sleep_change)

        return self.sleep_container

    @ErrorHandler.handle_exception_decorator
    def on_sleep_change(self, event):
        selected_option = self.sleep_var.get()
        option_data = self.sleep_options.get(selected_option, {})
        if option_data:
            # Display additional information with simplified format
            info_text = (
                f"{selected_option}\n"  # Removed "Selected:" prefix
                f"{option_data['desc']}\n"  # Removed "Description:" prefix
                f"Impact: {option_data['impact']}\n"
                f"Tip: {option_data['recommendation']}"  # Changed "Recommendation:" to "Tip:"
            )
            self.sleep_info_label.configure(text=info_text)

    @ErrorHandler.handle_exception_decorator
    def store_input(self) -> dict:
        """Store and return the step's input data."""
        selected_option = self.sleep_var.get()
        return {
            "sleep_pattern": {
                "selection": selected_option,
                "data": self.sleep_options[selected_option]
            }
        }

    def validate(self) -> bool:
        """Validate the sleep pattern selection."""
        is_valid, message = ValidationHelper.validate_selection(
            self.sleep_var.get(),
            list(self.sleep_options.keys()),
            "sleep pattern"
        )
        
        if not is_valid:
            ErrorHandler.show_error(message)
            return False
        return True