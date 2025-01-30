# steps/stress_step.py
import tkinter as tk
from tkinter import ttk
from steps import Step
from helpers.error_handlers import ErrorHandler
from helpers.validation import ValidationHelper
from helpers.ui_helpers import UIHelper
from styles import StyleConfig

class StressStep(Step):
    _order = 9

    def __init__(self, frame, title):
        super().__init__(frame, title)
        self.stress_container = None
        self.stress_label = None
        self.stress_var = None
        self.stress_options = {}
        self.stress_dropdown = None
        self.stress_info_label = None

    @ErrorHandler.handle_exception_decorator
    def create_widgets(self) -> ttk.Frame:
        """
        Create and return the main widget container for the step.
        Required implementation of abstract method from Step base class.
        """
        # Create main container with reduced padding
        self.stress_container = ttk.Frame(self.frame)
        self.stress_container.pack(pady=5, fill=tk.BOTH, expand=True, padx=5)

        # Create a central content frame for vertical centering
        spacer_top = ttk.Frame(self.stress_container)
        spacer_top.pack(expand=True)

        content_frame = ttk.Frame(self.stress_container)
        content_frame.pack(expand=False)

        # Create stress label with reduced padding
        self.stress_label = ttk.Label(
            content_frame,
            text="Stress Level:",
            style="Header.TLabel"
        )
        self.stress_label.pack(pady=(0, 3))

        # Create stress options dropdown with specific width
        self.stress_var = tk.StringVar()
        self.stress_dropdown = ttk.Combobox(
            content_frame,
            textvariable=self.stress_var,
            state='readonly',
            width=25  # Set specific width
        )
        self.stress_dropdown.pack(pady=3)

        # Populate stress options
        self.stress_options = {
            "😐 Low": {
                "factor": 0.9,
                "desc": "Low stress levels",
                "impact": "5% increase in regularity",
                "recommendation": "Maintain current stress management",
                "details": "Low stress promotes healthy digestion",
                "tips": "Continue with stress-reducing activities"
            },
            "🙂 Moderate": {
                "factor": 1.0,
                "desc": "Average stress levels",
                "impact": "No significant impact",
                "recommendation": "Monitor stress levels",
                "details": "Moderate stress is common and manageable",
                "tips": "Practice relaxation techniques as needed"
            },
            "😰 High": {
                "factor": 1.1,
                "desc": "High stress levels",
                "impact": "10% decrease in regularity",
                "recommendation": "Implement stress management techniques",
                "details": "High stress can negatively affect digestion",
                "tips": "Consider mindfulness, exercise, or professional support"
            },
            "😱 Very High": {
                "factor": 1.2,
                "desc": "Constant stress",
                "impact": "15% decrease in regularity",
                "recommendation": "Seek professional support",
                "details": "Chronic stress significantly impacts health",
                "tips": "Prioritize stress management and consult experts"
            }
        }

        self.stress_dropdown['values'] = list(self.stress_options.keys())
        self.stress_var.set(list(self.stress_options.keys())[1])  # Default to "Moderate"

        # Create stress tips label with specific width and reduced padding
        self.stress_info_label = UIHelper.create_info_label(
            content_frame,
            "🧘 Tips for managing stress:\n"
            "• Practice mindfulness or meditation\n"
            "• Engage in regular physical activity\n"
            "• Maintain a healthy work-life balance",
            wraplength=300
        )
        self.stress_info_label.pack(pady=5)

        spacer_bottom = ttk.Frame(self.stress_container)
        spacer_bottom.pack(expand=True)

        # Bind dropdown change event
        self.stress_dropdown.bind('<<ComboboxSelected>>', self.on_stress_change)

        return self.stress_container

    @ErrorHandler.handle_exception_decorator
    def on_stress_change(self, event):
        selected_option = self.stress_var.get()
        option_data = self.stress_options.get(selected_option, {})
        if option_data:
            # Display additional information with simplified format
            info_text = (
                f"{selected_option}\n"  # Removed "Selected:" prefix
                f"{option_data['desc']}\n"  # Removed "Description:" prefix
                f"Impact: {option_data['impact']}\n"
                f"Tip: {option_data['recommendation']}"  # Changed "Recommendation:" to "Tip:"
            )
            self.stress_info_label.configure(text=info_text)

    @ErrorHandler.handle_exception_decorator
    def store_input(self) -> dict:
        """Store and return the step's input data."""
        selected_option = self.stress_var.get()
        return {
            "stress_level": {
                "selection": selected_option,
                "data": self.stress_options[selected_option]
            }
        }

    def validate(self) -> bool:
        """Validate the stress level selection."""
        is_valid, message = ValidationHelper.validate_selection(
            self.stress_var.get(),
            list(self.stress_options.keys()),
            "stress level"
        )
        
        if not is_valid:
            ErrorHandler.show_error(message)
            return False
        return True