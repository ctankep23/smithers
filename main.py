# main.py
import tkinter as tk
from tkinter import ttk
from core import PoopCalculatorApp
from helpers.error_handlers import ErrorHandler
from styles import StyleConfig

def main():
    """
    Main entry point for the Poop Calculator application.
    Initializes the root window and starts the application.
    """
    try:
        # Create the root window
        root = tk.Tk()
        root.title("Poop Calculator")
        
        # Configure the style
        StyleConfig.configure_styles()
        
        # Create and start the application
        app = PoopCalculatorApp(root)
        
        # Start the main event loop
        root.mainloop()
        
    except Exception as e:
        ErrorHandler.handle_exception(e)
        print(f"Error starting application: {str(e)}")
        if 'root' in locals():
            root.destroy()

if __name__ == "__main__":
    main()