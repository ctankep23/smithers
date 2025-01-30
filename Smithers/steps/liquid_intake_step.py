# steps/liquid_intake_step.py
import tkinter as tk
from tkinter import ttk
from steps import Step
from helpers.error_handlers import ErrorHandler
from helpers.validation import ValidationHelper
from helpers.ui_helpers import UIHelper
from styles import StyleConfig

class LiquidIntakeStep(Step):
    _order = 5

    def __init__(self, frame, title):
        super().__init__(frame, title)
        self.liquid_intake_container = None
        self.liquid_intake_options = None
        self.selected_liquid_intake = tk.StringVar()
        self.liquid_intake_info_label = None

    @ErrorHandler.handle_exception_decorator
    def create_widgets(self) -> ttk.Frame:
        """
        Create and return the main widget container for the step.
        Required implementation of abstract method from Step base class.
        """
        # Create main container with reduced padding
        self.liquid_intake_container = ttk.Frame(self.frame)
        self.liquid_intake_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create a central content frame for vertical centering
        spacer_top = ttk.Frame(self.liquid_intake_container)
        spacer_top.pack(expand=True)

        content_frame = ttk.Frame(self.liquid_intake_container)
        content_frame.pack(expand=False)

        # Create header label with reduced padding
        header_label = ttk.Label(
            content_frame,
            text="Daily Liquid Intake:",
            style="Header.TLabel"
        )
        header_label.pack(pady=(0, 3))

        # Create radio buttons for liquid intake options
        self.liquid_intake_options = {
            "Adequate hydration (8+ cups/day)": {
                "factor": 1.0,
                "desc": "Normal bowel movement support",
                "icon": "💧",
                "details": "Ensures proper stool consistency",
                "impact": "Supports regular bowel movements",
                "tips": "Drink at least 8 glasses of water daily"
            },
            "High hydration (12+ cups/day)": {
                "factor": 1.2,
                "desc": "Improved bowel movement frequency",
                "icon": "💧💧",
                "details": "Optimal hydration for digestion",
                "impact": "May increase bowel movements",
                "tips": "Stay hydrated throughout the day"
            },
            "Low hydration (4-6 cups/day)": {
                "factor": 0.8,
                "desc": "May lead to constipation",
                "icon": "💧",
                "details": "Insufficient hydration for digestion",
                "impact": "May decrease bowel movements",
                "tips": "Increase water intake gradually"
            }
        }

        # Create radio buttons frame with compact spacing
        radio_frame = ttk.Frame(content_frame)
        radio_frame.pack(fill=tk.X, pady=3)

        for option, details in self.liquid_intake_options.items():
            radio_btn = ttk.Radiobutton(
                radio_frame,
                text=f"{details['icon']} {option}",
                variable=self.selected_liquid_intake,
                value=option,
                command=self.on_liquid_intake_change
            )
            radio_btn.pack(anchor=tk.W, pady=1)  # Reduced padding between radio buttons

        # Create info label with specific width and reduced padding
        self.liquid_intake_info_label = UIHelper.create_info_label(
            content_frame,
            "💧 Tips for proper hydration:\n"
            "• Drink water regularly throughout the day\n"
            "• Monitor your urine color\n"
            "• Increase intake during exercise",
            wraplength=300
        )
        self.liquid_intake_info_label.pack(pady=5)

        spacer_bottom = ttk.Frame(self.liquid_intake_container)
        spacer_bottom.pack(expand=True)

        # Set default selection
        self.selected_liquid_intake.set("Adequate hydration (8+ cups/day)")
        self.on_liquid_intake_change()

        return self.liquid_intake_container

    @ErrorHandler.handle_exception_decorator
    def on_liquid_intake_change(self):
        """Handle liquid intake selection changes."""
        selected_option = self.selected_liquid_intake.get()
        if selected_option in self.liquid_intake_options:
            details = self.liquid_intake_options[selected_option]
            info_text = (
                f"{details['icon']} {selected_option}\n"  # Simplified header
                f"{details['desc']}\n"  # Removed "Description:" prefix
                f"Impact: {details['impact']}\n"
                f"Tip: {details['tips']}"  # Changed "Tips:" to "Tip:"
            )
            self.liquid_intake_info_label.configure(text=info_text)

    @ErrorHandler.handle_exception_decorator
    def store_input(self) -> dict:
        """Store and return the step's input data."""
        selected_option = self.selected_liquid_intake.get()
        return {
            "liquid_intake": {
                "selection": selected_option,
                "factor": self.liquid_intake_options[selected_option]["factor"],
                "details": self.liquid_intake_options[selected_option]
            }
        }

    def validate(self) -> bool:
        """Validate the liquid intake selection."""
        if not self.selected_liquid_intake.get():
            ErrorHandler.show_error("Please select your daily liquid intake")
            return False
        return True