# steps/birth_date_step.py
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from steps import Step
from helpers.error_handlers import ErrorHandler
from helpers.validation import ValidationHelper
from helpers.ui_helpers import UIHelper
from styles import StyleConfig
from datetime import datetime

class BirthDateStep(Step):
    _order = 1

    def __init__(self, frame, title):
        super().__init__(frame, title)
        self.birth_date_container = None
        self.birth_date_label = None
        self.birth_date_entry = None
        self.birth_date_info_label = None

    @ErrorHandler.handle_exception_decorator
    def create_widgets(self) -> ttk.Frame:
        """
        Create and return the main widget container for the step.
        Required implementation of abstract method from Step base class.
        """
        # Create main container with reduced padding
        self.birth_date_container = ttk.Frame(self.frame)
        self.birth_date_container.pack(pady=5, fill=tk.BOTH, expand=True, padx=5)

        # Create a central content frame for vertical centering
        spacer_top = ttk.Frame(self.birth_date_container)
        spacer_top.pack(expand=True)

        content_frame = ttk.Frame(self.birth_date_container)
        content_frame.pack(expand=False)

        # Create birth date label with reduced padding
        self.birth_date_label = ttk.Label(
            content_frame,
            text="Date of Birth:",
            style="Header.TLabel"
        )
        self.birth_date_label.pack(pady=(0, 3))

        # Create calendar widget with specific size and styling
        self.birth_date_entry = DateEntry(
            content_frame,
            width=15,  # Slightly wider for better visibility
            background=StyleConfig.COLOR_PRIMARY,
            foreground='white',
            borderwidth=1,  # Reduced border
            year=2000,  # Default year
            date_pattern='yyyy-mm-dd',
            maxdate=datetime.now(),  # Can't select future dates
            font=('Arial', 10)  # Specific font size
        )
        self.birth_date_entry.pack(pady=3)

        # Create birth date info label with reduced padding and specific width
        self.birth_date_info_label = UIHelper.create_info_label(
            content_frame,
            "📅 Select your birth date using the calendar.\n"
            "This helps us provide age-appropriate recommendations.",
            wraplength=300  # Set specific wrap length
        )
        self.birth_date_info_label.pack(pady=5)

        spacer_bottom = ttk.Frame(self.birth_date_container)
        spacer_bottom.pack(expand=True)

        # Bind date change event
        self.birth_date_entry.bind("<<DateEntrySelected>>", self.on_birth_date_change)

        return self.birth_date_container

    @ErrorHandler.handle_exception_decorator
    def on_birth_date_change(self, event):
        """Handle birth date selection changes."""
        selected_date = self.birth_date_entry.get_date()
        age = (datetime.now() - datetime.combine(selected_date, datetime.min.time())).days // 365

        # Update info label with more concise formatting
        self.birth_date_info_label.configure(
            text=f"Age: {age} years\n"
            f"Date: {selected_date.strftime('%Y-%m-%d')}"
        )

    @ErrorHandler.handle_exception_decorator
    def store_input(self) -> dict:
        """Store and return the step's input data."""
        selected_date = self.birth_date_entry.get_date()
        age = (datetime.now() - datetime.combine(selected_date, datetime.min.time())).days // 365

        return {
            "birth_date": {
                "date": selected_date.strftime('%Y-%m-%d'),
                "age": age
            }
        }

    def validate(self) -> bool:
        """Validate the birth date input."""
        try:
            selected_date = self.birth_date_entry.get_date()
            
            # Check if date is not in the future
            if selected_date > datetime.now().date():
                ErrorHandler.show_error("Birth date cannot be in the future")
                return False
                
            # Check if age is reasonable (e.g., less than 120 years)
            age = (datetime.now().date() - selected_date).days // 365
            if age > 120:
                ErrorHandler.show_error("Please enter a valid birth date")
                return False
                
            return True
            
        except Exception:
            ErrorHandler.show_error("Please select a valid birth date")
            return False