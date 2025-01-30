# core.py
import tkinter as tk
from tkinter import ttk
from helpers.error_handlers import ErrorHandler
from helpers.ui_helpers import UIHelper
from styles import StyleConfig
from steps_manager import StepsManager
from components.progress_indicator import ProgressIndicator

class PoopCalculatorApp:
    def __init__(self, root):
        """
        Initialize the Poop Calculator application.
        
        Args:
            root: The root Tkinter window
        """
        print("Initializing PoopCalculatorApp...")  # Debug print
        
        self.root = root
        self.root.title("Poop Calculator")
        self.root.geometry("600x500")  # Reduced size
        
        # Initialize variables
        self.current_step_index = 0
        self.current_step = None
        self.user_data = {}
        self.prev_button = None  # Initialize button variables
        self.next_button = None
        
        # Configure styles
        StyleConfig.configure_styles()
        
        # Set up the UI first
        print("Setting up UI...")  # Debug print
        self.setup_ui()
        print("UI setup complete")  # Debug print
        
        # Initialize steps manager and get steps
        print("Initializing steps manager...")  # Debug print
        self.steps_manager = StepsManager(self.content_frame)
        self.steps = self.steps_manager.steps
        print(f"Found {len(self.steps)} steps")  # Debug print

        # Update progress indicator with total steps
        self.progress_indicator.total_steps = len(self.steps)
        if self.steps:
            self.progress_indicator.update_progress(1, self.steps[0].title)
        
        # Show first step
        print("Showing first step...")  # Debug print
        self.show_current_step()
        print("Initialization complete")  # Debug print

    @ErrorHandler.handle_exception_decorator
    def setup_ui(self):
        """Set up the main user interface components."""
        print("Starting UI setup...")  # Debug print
        
        # Create main container with reduced padding
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top Section: Header with reduced padding
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.title_label = ttk.Label(
            self.header_frame,
            text="💩 Poop Calculator",
            style="Title.TLabel"
        )
        self.title_label.pack(side=tk.LEFT)
        
        # Progress Section with reduced padding
        self.progress_indicator = ProgressIndicator(self.main_frame, total_steps=0)
        self.progress_indicator.pack(fill=tk.X, pady=(0, 10))
        
        # Middle Section: Content with reduced height
        self.content_frame = ttk.Frame(self.main_frame, height=300)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.content_frame.pack_propagate(False)
        
        # Bottom Section: Navigation
        self.nav_frame = ttk.Frame(self.main_frame)
        self.nav_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Navigation buttons with reduced spacing
        button_frame = ttk.Frame(self.nav_frame)
        button_frame.pack(fill=tk.X, pady=(5, 0))
        
        try:
            print("Creating navigation buttons...")  # Debug print
            
            # Create Previous button with reduced width
            self.prev_button = ttk.Button(
                button_frame,
                text="← Previous",
                command=self.previous_step,
                style="TButton",
                width=15
            )
            print("Previous button created")  # Debug print
            self.prev_button.pack(side=tk.LEFT, padx=(0, 5))
            
            # Create Next button with reduced width
            self.next_button = ttk.Button(
                button_frame,
                text="Next →",
                command=self.next_step,
                style="TButton",
                width=15
            )
            print("Next button created")  # Debug print
            self.next_button.pack(side=tk.RIGHT, padx=(5, 0))
            
        except Exception as e:
            print(f"Error creating buttons: {str(e)}")  # Debug print
            raise
        
        print("UI setup completed")  # Debug print

    @ErrorHandler.handle_exception_decorator
    def show_current_step(self):
        """Display the current step."""
        print(f"Showing step {self.current_step_index + 1}")  # Debug print
        
        if not self.steps:
            print("No steps found!")  # Debug print
            return
            
        # Hide all steps
        for step in self.steps:
            step.frame.pack_forget()
        
        # Show current step
        current_step = self.steps[self.current_step_index]
        current_step.frame.pack(fill=tk.BOTH, expand=True)
        
        # Create widgets for current step if they haven't been created yet
        if not hasattr(current_step, 'widgets_created'):
            current_step.create_widgets()
            current_step.widgets_created = True
        
        print("Updating navigation buttons...")  # Debug print
        # Update navigation buttons
        if hasattr(self, 'prev_button') and self.prev_button:
            self.prev_button.config(
                state='normal' if self.current_step_index > 0 else 'disabled',
                text="← Previous" if self.current_step_index > 0 else ""
            )
        else:
            print("Previous button not found!")  # Debug print
            
        if hasattr(self, 'next_button') and self.next_button:
            self.next_button.config(
                text="Finish →" if self.current_step_index == len(self.steps) - 1 else "Next →"
            )
        else:
            print("Next button not found!")  # Debug print
        
        # Update progress indicator
        self.progress_indicator.update_progress(
            self.current_step_index + 1,
            current_step.title
        )
        print("Step display complete")  # Debug print

    @ErrorHandler.handle_exception_decorator
    def next_step(self):
        """Proceed to the next step if validation passes."""
        current_step = self.steps[self.current_step_index]
        
        if current_step.validate():
            # Store the current step's data
            step_data = current_step.store_input()
            if step_data:
                self.user_data.update(step_data)
            
            if self.current_step_index < len(self.steps) - 1:
                # Move to next step
                self.current_step_index += 1
                self.show_current_step()
            else:
                # Final step completed
                self.finish_calculation()

    @ErrorHandler.handle_exception_decorator
    def previous_step(self):
        """Return to the previous step."""
        if self.current_step_index > 0:
            self.current_step_index -= 1
            self.show_current_step()

    @ErrorHandler.handle_exception_decorator
    def finish_calculation(self):
        """Process final calculations and show results."""
        # Calculate final results
        results = self.calculate_results()
        
        # Show results window
        self.show_results(results)

    def calculate_results(self):
        """Calculate final results based on user input."""
        return {
            "score": 0,
            "recommendations": [],
            "summary": "Results will be calculated here"
        }

    def show_results(self, results):
        """Display the final results to the user."""
        # Create results window with reduced size
        results_window = tk.Toplevel(self.root)
        results_window.title("Your Results")
        results_window.geometry("500x400")
        
        # Add results content with reduced padding
        results_frame = ttk.Frame(results_window, padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add results content here
        ttk.Label(
            results_frame,
            text="Your Results",
            style="Title.TLabel"
        ).pack(pady=(0, 10))