# steps/medications_step.py
import tkinter as tk
from tkinter import ttk
from steps import Step
from helpers.error_handlers import ErrorHandler
from helpers.validation import ValidationHelper
from helpers.ui_helpers import UIHelper
from styles import StyleConfig

class MedicationsStep(Step):
    _order = 7

    def __init__(self, frame, title):
        super().__init__(frame, title)
        self.medications_container = None
        self.medication_options = None
        self.selected_medication = tk.StringVar()
        self.medication_info_label = None

    @ErrorHandler.handle_exception_decorator
    def create_widgets(self) -> ttk.Frame:
        """
        Create and return the main widget container for the step.
        Required implementation of abstract method from Step base class.
        """
        # Create main container with reduced padding
        self.medications_container = ttk.Frame(self.frame)
        self.medications_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create a central content frame for vertical centering
        spacer_top = ttk.Frame(self.medications_container)
        spacer_top.pack(expand=True)

        content_frame = ttk.Frame(self.medications_container)
        content_frame.pack(expand=False)

        # Create header label with reduced padding
        header_label = ttk.Label(
            content_frame,
            text="Medications:",
            style="Header.TLabel"
        )
        header_label.pack(pady=(0, 3))

        # Create radio buttons for medication options
        self.medication_options = {
            "No medications": {
                "factor": 1.0,
                "desc": "No impact on bowel movements",
                "icon": "💊",
                "details": "No medications that affect digestion",
                "impact": "No significant impact",
                "tips": "Maintain a balanced diet"
            },
            "Fiber supplements": {
                "factor": 1.2,
                "desc": "Increase in bowel movements",
                "icon": "💊",
                "details": "Commonly used to relieve constipation",
                "impact": "May increase bowel movements",
                "tips": "Follow recommended dosage"
            },
            "Diarrhea medications": {
                "factor": 0.8,
                "desc": "Decrease in bowel movements",
                "icon": "💊",
                "details": "May slow down digestion",
                "impact": "May decrease bowel movements",
                "tips": "Consult a healthcare professional"
            }
        }

        # Create radio buttons frame with compact spacing
        radio_frame = ttk.Frame(content_frame)
        radio_frame.pack(fill=tk.X, pady=3)

        for option, details in self.medication_options.items():
            radio_btn = ttk.Radiobutton(
                radio_frame,
                text=f"{details['icon']} {option}",
                variable=self.selected_medication,
                value=option,
                command=self.on_medication_change
            )
            radio_btn.pack(anchor=tk.W, pady=1)  # Reduced padding between radio buttons

        # Create info label with specific width and reduced padding
        self.medication_info_label = UIHelper.create_info_label(
            content_frame,
            "💊 Important medication notes:\n"
            "• Always follow prescribed dosages\n"
            "• Consult healthcare provider about side effects\n"
            "• Report significant changes in bowel movements",
            wraplength=300
        )
        self.medication_info_label.pack(pady=5)

        spacer_bottom = ttk.Frame(self.medications_container)
        spacer_bottom.pack(expand=True)

        # Set default selection
        self.selected_medication.set("No medications")
        self.on_medication_change()

        return self.medications_container

    @ErrorHandler.handle_exception_decorator
    def on_medication_change(self):
        """Handle medication selection changes."""
        selected_option = self.selected_medication.get()
        if selected_option in self.medication_options:
            details = self.medication_options[selected_option]
            info_text = (
                f"{details['icon']} {selected_option}\n"  # Simplified header
                f"{details['desc']}\n"  # Removed "Description:" prefix
                f"Impact: {details['impact']}\n"
                f"Tip: {details['tips']}"  # Changed "Tips:" to "Tip:"
            )
            self.medication_info_label.configure(text=info_text)

    @ErrorHandler.handle_exception_decorator
    def store_input(self) -> dict:
        """Store and return the step's input data."""
        selected_option = self.selected_medication.get()
        return {
            "medication": {
                "selection": selected_option,
                "factor": self.medication_options[selected_option]["factor"],
                "details": self.medication_options[selected_option]
            }
        }

    def validate(self) -> bool:
        """Validate the medication selection."""
        if not self.selected_medication.get():
            ErrorHandler.show_error("Please select your medication status")
            return False
        return True