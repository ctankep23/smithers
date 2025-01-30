# helpers/error_handlers.py
import logging
import traceback
from tkinter import messagebox
from functools import wraps

class ErrorHandler:
    """
    Handles error logging and user notifications for the application.
    Provides both direct error handling methods and decorators.
    """
    
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    
    @classmethod
    def setup_logging(cls):
        """Configure logging settings."""
        logging.basicConfig(
            filename='poop_calculator.log',
            level=logging.ERROR,
            format=cls.LOG_FORMAT
        )

    @staticmethod
    def handle_exception(exception):
        """
        Handle exceptions by logging them and showing an error message to the user.
        
        Args:
            exception: The exception that was raised
        """
        error_message = str(exception)
        
        # Log the error with full traceback
        logging.error(
            f"Error occurred: {error_message}\n"
            f"Traceback:\n{traceback.format_exc()}"
        )
        
        # Show user-friendly error message
        messagebox.showerror(
            "Error",
            f"An error occurred: {error_message}\n\n"
            "The error has been logged. Please try again or contact support."
        )

    @staticmethod
    def show_error(message):
        """
        Show an error message to the user.
        
        Args:
            message: The error message to display
        """
        messagebox.showerror("Error", message)

    @staticmethod
    def show_warning(message):
        """
        Show a warning message to the user.
        
        Args:
            message: The warning message to display
        """
        messagebox.showwarning("Warning", message)

    @staticmethod
    def show_info(message):
        """
        Show an information message to the user.
        
        Args:
            message: The information message to display
        """
        messagebox.showinfo("Information", message)

    @staticmethod
    def handle_exception_decorator(func):
        """
        Decorator for handling exceptions in methods.
        
        Args:
            func: The function to wrap with error handling
        
        Returns:
            The wrapped function with error handling
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                ErrorHandler.handle_exception(e)
                return None
        return wrapper

    @staticmethod
    def validate_input_decorator(validation_func):
        """
        Decorator for validating input before executing a function.
        
        Args:
            validation_func: Function that performs the validation
        
        Returns:
            The wrapped function with input validation
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    is_valid, message = validation_func(*args, **kwargs)
                    if not is_valid:
                        ErrorHandler.show_error(message)
                        return None
                    return func(*args, **kwargs)
                except Exception as e:
                    ErrorHandler.handle_exception(e)
                    return None
            return wrapper
        return decorator

    @staticmethod
    def log_error(error_message, error=None):
        """
        Log an error message with optional exception details.
        
        Args:
            error_message: The message to log
            error: Optional exception object
        """
        if error:
            logging.error(
                f"{error_message}\n"
                f"Error: {str(error)}\n"
                f"Traceback:\n{traceback.format_exc()}"
            )
        else:
            logging.error(error_message)