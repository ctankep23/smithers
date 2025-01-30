# helpers/validation.py
from typing import Tuple, Any, List, Dict, Optional
from helpers.error_handlers import ErrorHandler

class ValidationHelper:
    """
    Provides validation methods for various input types throughout the application.
    """

    @staticmethod
    def validate_selection(value: Any, valid_options: List[Any], field_name: str) -> Tuple[bool, str]:
        """
        Validate that a selection is within valid options.
        
        Args:
            value: The selected value
            valid_options: List of valid options
            field_name: Name of the field being validated
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not value:
            return False, f"Please select a {field_name}"
        if value not in valid_options:
            return False, f"Invalid {field_name} selection"
        return True, ""

    @staticmethod
    def validate_number(
        value: str,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        field_name: str = "number"
    ) -> Tuple[bool, str]:
        """
        Validate that a number is within specified range.
        
        Args:
            value: The number to validate
            min_value: Minimum allowed value
            max_value: Maximum allowed value
            field_name: Name of the field being validated
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        try:
            num = float(value)
            if min_value is not None and num < min_value:
                return False, f"{field_name.capitalize()} must be at least {min_value}"
            if max_value is not None and num > max_value:
                return False, f"{field_name.capitalize()} must be no more than {max_value}"
            return True, ""
        except ValueError:
            return False, f"Please enter a valid number for {field_name}"

    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> Tuple[bool, str]:
        """
        Validate that all required fields are present and not empty.
        
        Args:
            data: Dictionary containing field values
            required_fields: List of required field names
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        missing_fields = []
        for field in required_fields:
            if field not in data or not data[field]:
                missing_fields.append(field)
        
        if missing_fields:
            fields_str = ", ".join(missing_fields)
            return False, f"Please fill in the following required fields: {fields_str}"
        return True, ""

    @staticmethod
    def validate_range(
        value: float,
        ranges: Dict[str, Tuple[float, float]],
        field_name: str
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Validate a value against multiple ranges and return the matching range key.
        
        Args:
            value: Value to validate
            ranges: Dictionary of range names and their (min, max) values
            field_name: Name of the field being validated
        
        Returns:
            Tuple[bool, str, Optional[str]]: (is_valid, error_message, range_key)
        """
        for range_key, (min_val, max_val) in ranges.items():
            if min_val <= value <= max_val:
                return True, "", range_key
        
        return False, f"{field_name} is outside of valid ranges", None

    @staticmethod
    @ErrorHandler.handle_exception_decorator
    def validate_step_data(step_data: Dict[str, Any], step_name: str) -> Tuple[bool, str]:
        """
        Validate data for a specific step.
        
        Args:
            step_data: Dictionary containing step data
            step_name: Name of the step being validated
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not step_data:
            return False, f"No data provided for {step_name}"
        
        # Add specific validation rules for each step
        if step_name == "poop_size":
            required_fields = ["size"]
            return ValidationHelper.validate_required_fields(step_data, required_fields)
        
        elif step_name == "poops_per_week":
            if "frequency" not in step_data:
                return False, "Please select your weekly frequency"
            
            return ValidationHelper.validate_number(
                step_data["frequency"],
                min_value=0,
                max_value=50,
                field_name="weekly frequency"
            )
        
        # Add more step validations as needed
        
        return True, ""

    @staticmethod
    def validate_calculation_input(data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate all required data before calculation.
        
        Args:
            data: Dictionary containing all input data
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        required_steps = ["poop_size", "poops_per_week"]
        
        for step in required_steps:
            if step not in data:
                return False, f"Missing data for {step.replace('_', ' ')} step"
            
            is_valid, message = ValidationHelper.validate_step_data(data[step], step)
            if not is_valid:
                return False, message
        
        return True, ""