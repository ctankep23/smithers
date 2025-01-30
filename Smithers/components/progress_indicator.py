# components/progress_indicator.py
import tkinter as tk
from tkinter import ttk
from styles import StyleConfig

class ProgressIndicator(ttk.Frame):
    def __init__(self, parent, total_steps):
        """
        Initialize the progress indicator.
        
        Args:
            parent: Parent widget
            total_steps: Total number of steps in the wizard
        """
        super().__init__(parent)
        self.total_steps = total_steps if total_steps > 0 else 1  # Prevent division by zero
        self.current_step = 1
        self.create_progress_bar()

    def create_progress_bar(self):
        """Create and configure all progress indicator widgets."""
        # Create container for progress elements with reduced padding
        self.progress_container = ttk.Frame(self)
        self.progress_container.pack(fill=tk.X, padx=10, pady=5)  # Reduced padding

        # Create step counter label with reduced padding
        self.step_label = ttk.Label(
            self.progress_container,
            text=f"Step {self.current_step} of {self.total_steps}",
            style='Progress.TLabel'
        )
        self.step_label.pack(pady=(0, 2))  # Reduced padding

        # Create progress bar with reduced height
        self.progress_bar = ttk.Progressbar(
            self.progress_container,
            orient="horizontal",
            length=200,  # Reduced length
            mode="determinate",
            style="TProgressbar"
        )
        self.progress_bar.pack(fill=tk.X)

        # Create step description with reduced padding
        self.step_description = ttk.Label(
            self.progress_container,
            text="",
            style='Description.TLabel',
            justify=tk.CENTER
        )
        self.step_description.pack(pady=(2, 0))  # Reduced padding

    def update_progress(self, current_step, step_title=""):
        """
        Update the progress indicator.
        
        Args:
            current_step: Current step number
            step_title: Title of the current step
        """
        self.current_step = current_step
        
        # Calculate progress percentage
        progress = ((current_step - 1) / max(self.total_steps - 1, 1)) * 100
        
        # Ensure step 1 shows some progress
        if current_step == 1:
            progress = (1 / self.total_steps) * 100

        # Update progress bar
        self.progress_bar["value"] = progress

        # Update step counter with percentage
        self.step_label.config(
            text=f"Step {current_step} of {self.total_steps} ({progress:.0f}%)"
        )

        # Update description with reduced font size if needed
        if step_title:
            self.step_description.config(text=step_title)

    def reset(self):
        """Reset the progress indicator to initial state."""
        self.current_step = 1
        self.progress_bar["value"] = 0
        self.update_progress(1, "")