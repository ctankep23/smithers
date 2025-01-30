# helpers/data_processing.py
from datetime import datetime
from typing import Dict, Any, Union, List

class DataProcessor:
    @staticmethod
    def calculate_age(birthdate: datetime) -> int:
        """Calculate age from birthdate"""
        today = datetime.now()
        age = today.year - birthdate.year
        if today.month < birthdate.month or (
            today.month == birthdate.month and 
            today.day < birthdate.day
        ):
            age -= 1
        return age

    @staticmethod
    def calculate_days_alive(birthdate: datetime) -> int:
        """Calculate total days alive"""
        return (datetime.now() - birthdate).days

    @staticmethod
    def calculate_total_poop(
        age_years: float,
        poop_per_day: float,
        grams_per_poop: float,
        adjustment_factor: float = 1.0
    ) -> Dict[str, float]:
        """
        Calculate total poop production with adjustments
        Returns dictionary with various metrics
        """
        days = age_years * 365
        total_poops = days * poop_per_day * adjustment_factor
        total_grams = total_poops * grams_per_poop
        
        return {
            'total_kg': total_grams / 1000,
            'total_poops': int(total_poops),
            'average_per_day': poop_per_day * adjustment_factor,
            'adjusted_grams_per_poop': grams_per_poop
        }

    @staticmethod
    def calculate_adjustment_factor(inputs: Dict[str, Any]) -> float:
        """Calculate overall adjustment factor from all inputs"""
        factors = {
            'diet': inputs.get('diet', {}).get('factor', 1.0),
            'region': inputs.get('region', {}).get('factor', 1.0),
            'gender': inputs.get('gender', {}).get('factor', 1.0),
            'activity': inputs.get('activity', {}).get('factor', 1.0),
            'liquid_intake': inputs.get('liquid_intake', {}).get('total_factor', 1.0),
            'sleep': inputs.get('sleep', {}).get('factor', 1.0),
            'stress': inputs.get('stress', {}).get('factor', 1.0),
            'medications': inputs.get('medications', {}).get('total_factor', 1.0)
        }
        
        total_factor = 1.0
        for factor in factors.values():
            total_factor *= float(factor)
        
        return total_factor

    @staticmethod
    def format_number(
        number: Union[int, float],
        decimal_places: int = 2
    ) -> str:
        """Format numbers with thousand separators and decimal places"""
        if isinstance(number, int):
            return f"{number:,}"
        return f"{number:,.{decimal_places}f}"

    @staticmethod
    def generate_comparisons(total_kg: float) -> List[str]:
        """Generate fun comparisons based on total weight"""
        comparisons = []
        comparison_data = {
            'elephant': {'weight': 4000, 'text': 'elephants'},
            'car': {'weight': 1500, 'text': 'average cars'},
            'whale': {'weight': 140000, 'text': 'blue whales'},
            'pool': {'volume': 2500000, 'text': 'Olympic swimming pools'},
            'bathtub': {'volume': 200, 'text': 'bathtubs'}
        }

        for item, data in comparison_data.items():
            if 'weight' in data:
                amount = total_kg / data['weight']
                comparisons.append(
                    f"Equal to {DataProcessor.format_number(amount)} {data['text']}"
                )
            elif 'volume' in data:
                amount = (total_kg / data['volume']) * 100
                comparisons.append(
                    f"Would fill {DataProcessor.format_number(amount)}% of {data['text']}"
                )

        return comparisons