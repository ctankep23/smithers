# helpers/ui_helpers.py
import tkinter as tk
from tkinter import ttk
from styles import StyleConfig

class UIHelper:
    """
    Provides helper methods for creating consistent UI elements throughout the application.
    """

    @staticmethod
    def create_info_label(parent, text, **kwargs):
        """
        Create a formatted information label.
        
        Args:
            parent: Parent widget
            text: Label text
            **kwargs: Additional ttk.Label arguments
        
        Returns:
            ttk.Label: The created label
        """
        label = ttk.Label(
            parent,
            text=text,
            font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZES["regular"]),
            foreground=StyleConfig.COLOR_SECONDARY,
            **kwargs
        )
        return label

    @staticmethod
    def create_button(parent, text, command, **kwargs):
        """
        Create a styled button.
        
        Args:
            parent: Parent widget
            text: Button text
            command: Button command callback
            **kwargs: Additional ttk.Button arguments
        
        Returns:
            ttk.Button: The created button
        """
        # Remove width from kwargs if it exists to avoid conflict
        if 'width' in kwargs:
            width = kwargs.pop('width')
        else:
            width = 15  # Default width

        button = ttk.Button(
            parent,
            text=text,
            command=command,
            style="TButton",
            width=width,
            **kwargs
        )
        return button

    @staticmethod
    def create_dropdown(parent, options, variable, **kwargs):
        """
        Create a styled dropdown menu.
        
        Args:
            parent: Parent widget
            options: List of dropdown options
            variable: StringVar to store selection
            **kwargs: Additional ttk.Combobox arguments
        
        Returns:
            ttk.Combobox: The created dropdown
        """
        dropdown = ttk.Combobox(
            parent,
            textvariable=variable,
            values=options,
            state='readonly',
            width=30,  # Default width
            **kwargs
        )
        return dropdown

    @staticmethod
    def create_frame(parent, **kwargs):
        """
        Create a styled frame.
        
        Args:
            parent: Parent widget
            **kwargs: Additional ttk.Frame arguments
        
        Returns:
            ttk.Frame: The created frame
        """
        frame = ttk.Frame(
            parent,
            padding=10,  # Using a direct value since PADDING_NORMAL isn't defined
            **kwargs
        )
        return frame

    @staticmethod
    def create_scrolled_text(parent, **kwargs):
        """
        Create a scrolled text widget.
        
        Args:
            parent: Parent widget
            **kwargs: Additional Text widget arguments
        
        Returns:
            tuple: (Frame, Text widget, Scrollbar)
        """
        frame = ttk.Frame(parent)
        
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(
            frame,
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD,
            font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZES["regular"]),
            **kwargs
        )
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=text_widget.yview)
        
        return frame, text_widget, scrollbar

    @staticmethod
    def create_header(parent, text, **kwargs):
        """
        Create a styled header label.
        
        Args:
            parent: Parent widget
            text: Header text
            **kwargs: Additional ttk.Label arguments
        
        Returns:
            ttk.Label: The created header label
        """
        header = ttk.Label(
            parent,
            text=text,
            style="Header.TLabel",
            **kwargs
        )
        return header

    @staticmethod
    def create_separator(parent, **kwargs):
        """
        Create a horizontal separator.
        
        Args:
            parent: Parent widget
            **kwargs: Additional ttk.Separator arguments
        
        Returns:
            ttk.Separator: The created separator
        """
        separator = ttk.Separator(
            parent,
            orient='horizontal',
            **kwargs
        )
        return separator

    @staticmethod
    def clear_frame(frame):
        """
        Remove all widgets from a frame.
        
        Args:
            frame: The frame to clear
        """
        for widget in frame.winfo_children():
            widget.destroy()

    @staticmethod
    def create_tooltip(widget, text):
        """
        Create a tooltip for a widget.
        
        Args:
            widget: Widget to add tooltip to
            text: Tooltip text
        """
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = ttk.Label(
                tooltip,
                text=text,
                justify=tk.LEFT,
                background=StyleConfig.COLOR_SECONDARY,
                foreground="white",
                relief="solid",
                borderwidth=1,
                padding=(5, 2)
            )
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            widget.tooltip = tooltip
            widget.bind('<Leave>', lambda e: hide_tooltip())
            
        widget.bind('<Enter>', show_tooltip)