# steps_manager.py
import os
import importlib
import inspect
from pathlib import Path
from typing import List, Type
from steps import Step
import tkinter as tk
from tkinter import ttk
from helpers.error_handlers import ErrorHandler

class StepsManager:
    """
    Manages the loading and organization of all steps in the application.
    """
    
    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the StepsManager.
        
        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.steps: List[Step] = []
        print("\n=== Starting StepsManager Initialization ===")
        self.load_steps()

    @ErrorHandler.handle_exception_decorator
    def load_steps(self) -> None:
        """Dynamically load all step classes from the steps directory"""
        print("\nStarting to load steps...")
        steps_dir = Path(__file__).parent / 'steps'
        print(f"Looking for steps in: {steps_dir}")
        
        step_classes: List[Type[Step]] = []
        
        # Import all python files in the steps directory
        print("\nScanning for step files...")
        for file in steps_dir.glob('*.py'):
            if file.name != '__init__.py':
                module_name = f"steps.{file.stem}"
                print(f"\nAttempting to load: {module_name}")
                try:
                    module = importlib.import_module(module_name)
                    print(f"Successfully imported {module_name}")
                    
                    # Find all Step subclasses in the module
                    for name, obj in inspect.getmembers(module):
                        if (inspect.isclass(obj) and
                            issubclass(obj, Step) and
                            obj != Step):
                            print(f"Found step class: {name}")
                            step_classes.append(obj)
                except Exception as e:
                    print(f"Error loading {module_name}: {str(e)}")
                    continue  # Continue loading other steps even if one fails

        if not step_classes:
            print("\nWarning: No step classes were loaded!")
            return

        print(f"\nFound {len(step_classes)} step classes")
        
        # Sort step classes by their _order attribute
        print("\nSorting step classes...")
        step_classes.sort(key=lambda x: getattr(x, '_order', 999))
        
        # Create instances of each step
        print("\nCreating step instances...")
        for step_class in step_classes:
            try:
                print(f"Creating instance of: {step_class.__name__}")
                frame = ttk.Frame(self.root, padding="20")
                
                # Generate a title from the class name
                title = ' '.join(
                    word.capitalize() 
                    for word in step_class.__name__.replace('Step', '').split('_')
                )
                
                # Create step instance with frame and title
                step = step_class(frame, title)
                self.steps.append(step)
                print(f"Successfully created: {step_class.__name__}")
            except Exception as e:
                print(f"Error creating instance of {step_class.__name__}: {str(e)}")

        print(f"\nFinished loading steps. Total steps loaded: {len(self.steps)}")
        print("=== StepsManager Initialization Complete ===\n")

    def get_inputs(self) -> dict:
        """
        Collect all inputs from all steps.
        
        Returns:
            dict: Combined inputs from all steps
        """
        all_inputs = {}
        for step in self.steps:
            all_inputs.update(step.inputs)
        return all_inputs

    def get_current_step(self, index: int) -> Step:
        """
        Get the step at the specified index.
        
        Args:
            index: Index of the step to retrieve
            
        Returns:
            Step: The requested step
        """
        if 0 <= index < len(self.steps):
            return self.steps[index]
        return None

    def get_step_count(self) -> int:
        """
        Get the total number of steps.
        
        Returns:
            int: Total number of steps
        """
        return len(self.steps)