# steps/__init__.py
import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
from typing import Dict, Any

class Step(ABC):
    _order: int = 999  # Default order

    def __init__(self, frame: ttk.Frame, title: str) -> None:
        self.frame = frame
        self.title = title
        self.inputs: Dict[str, Any] = {}

    @abstractmethod
    def create_widgets(self) -> ttk.Frame:
        """
        Abstract method to create and return the main widget container for the step.
        """
        pass

    @abstractmethod
    def store_input(self) -> None:
        """
        Each step must implement how to store its input.
        """
        pass

    def validate(self) -> bool:
        """
        Optional validation method that steps can override.
        """
        return True

    def get_order(self) -> int:
        """
        Returns the order of the step.
        """
        return self._order

    def destroy_widgets(self) -> None:
        """
        Destroys all widgets created by the step.
        """
        pass