# steps/diet_step.py
import tkinter as tk
from tkinter import ttk
from steps import Step
from helpers.error_handlers import ErrorHandler
from helpers.validation import ValidationHelper
from helpers.ui_helpers import UIHelper
from styles import StyleConfig

class DietStep(Step):
    _order = 4

    def __init__(self, frame, title):
        super().__init__(frame, title)
        self.diet_container = None
        self.diet_options = None
        self.selected_diet = tk.StringVar()
        self.diet_info_label = None

    @ErrorHandler.handle_exception_decorator
    def create_widgets(self) -> ttk.Frame:
        """
        Create and return the main widget container for the step.
        Required implementation of abstract method from Step base class.
        """
        # Create main container with reduced padding
        self.diet_container = ttk.Frame(self.frame)
        self.diet_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create a central content frame for vertical centering
        spacer_top = ttk.Frame(self.diet_container)
        spacer_top.pack(expand=True)

        content_frame = ttk.Frame(self.diet_container)
        content_frame.pack(expand=False)

        # Create header label with reduced padding
        header_label = ttk.Label(
            content_frame,
            text="Select Your Diet Type:",
            style="Header.TLabel"
        )
        header_label.pack(pady=(0, 3))

        # Create radio buttons for diet options
        self.diet_options = {
            "Balanced diet": {
                "factor": 1.0,
                "desc": "Normal bowel movement frequency",
                "icon": "🥗",
                "details": "High in fiber, fruits, and vegetables",
                "impact": "Supports regular bowel movements",
                "tips": "Maintain a variety of whole foods"
            },
            "High fiber diet": {
                "factor": 1.2,
                "desc": "Increase due to high fiber content",
                "icon": "🥕",
                "details": "High in vegetables, fruits, and whole grains",
                "impact": "May increase bowel movements",
                "tips": "Gradually increase fiber intake"
            },
            "Low fiber diet": {
                "factor": 0.8,
                "desc": "Decrease due to low fiber content",
                "icon": "🥩",
                "details": "Low in fiber, high in processed foods",
                "impact": "May cause irregular bowel movements",
                "tips": "Try to incorporate more whole foods"
            }
        }

        # Create radio buttons frame with compact spacing
        radio_frame = ttk.Frame(content_frame)
        radio_frame.pack(fill=tk.X, pady=3)

        for diet, details in self.diet_options.items():
            radio_btn = ttk.Radiobutton(
                radio_frame,
                text=f"{details['icon']} {diet}",
                variable=self.selected_diet,
                value=diet,
                command=self.on_diet_change
            )
            radio_btn.pack(anchor=tk.W, pady=1)  # Reduced padding between radio buttons

        # Create info label with specific width and reduced padding
        self.diet_info_label = UIHelper.create_info_label(
            content_frame,
            "Select your typical diet type.\n"
            "This helps us understand your digestive patterns.",
            wraplength=300
        )
        self.diet_info_label.pack(pady=5)

        spacer_bottom = ttk.Frame(self.diet_container)
        spacer_bottom.pack(expand=True)

        # Set default selection
        self.selected_diet.set("Balanced diet")
        self.on_diet_change()

        return self.diet_container

    @ErrorHandler.handle_exception_decorator
    def on_diet_change(self):
        """Handle diet selection changes."""
        selected_diet = self.selected_diet.get()
        if selected_diet in self.diet_options:
            details = self.diet_options[selected_diet]
            info_text = (
                f"{details['icon']} {selected_diet}\n"  # Simplified header
                f"{details['desc']}\n"  # Removed "Description:" prefix
                f"Impact: {details['impact']}\n"
                f"Tip: {details['tips']}"  # Changed "Tips:" to "Tip:"
            )
            self.diet_info_label.configure(text=info_text)

    @ErrorHandler.handle_exception_decorator
    def store_input(self) -> dict:
        """Store and return the step's input data."""
        selected_diet = self.selected_diet.get()
        return {
            "diet": {
                "selection": selected_diet,
                "factor": self.diet_options[selected_diet]["factor"],
                "details": self.diet_options[selected_diet]
            }
        }

    def validate(self) -> bool:
        """Validate the diet selection."""
        if not self.selected_diet.get():
            ErrorHandler.show_error("Please select a diet type")
            return False
        return True