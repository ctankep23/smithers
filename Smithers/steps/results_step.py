# steps/results_step.py
import tkinter as tk
from tkinter import ttk
from steps import Step
from helpers.error_handlers import ErrorHandler
from styles import StyleConfig

class ResultsStep(Step):
    _order = 12

    def __init__(self, frame, title):
        super().__init__(frame, title)
        self.results_container = None
        self.notebook = None
        self.summary_tab = None
        self.details_tab = None
        self.comparisons_tab = None
        self.factors_tab = None
        self.summary_text = None
        self.details_text = None
        self.comparisons_text = None
        self.factors_frame = None
        self.comparison_data = {}
        self.init_comparison_data()

    @ErrorHandler.handle_exception_decorator
    def create_widgets(self) -> ttk.Frame:
        """
        Create and return the main widget container for the step.
        Required implementation of abstract method from Step base class.
        """
        # Create main container with reduced padding
        self.results_container = ttk.Frame(self.frame)
        self.results_container.pack(pady=5, fill=tk.BOTH, expand=True, padx=5)

        # Create notebook for tabbed display with reduced padding
        self.notebook = ttk.Notebook(self.results_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=3)

        # Create tabs
        self.summary_tab = ttk.Frame(self.notebook, padding=5)
        self.details_tab = ttk.Frame(self.notebook, padding=5)
        self.comparisons_tab = ttk.Frame(self.notebook, padding=5)
        self.factors_tab = ttk.Frame(self.notebook, padding=5)

        self.notebook.add(self.summary_tab, text="Summary")
        self.notebook.add(self.details_tab, text="Details")
        self.notebook.add(self.comparisons_tab, text="Fun Facts")
        self.notebook.add(self.factors_tab, text="Impact Factors")

        # Create scrolled text widgets for each tab
        self.summary_text = self.create_text_widget(self.summary_tab)
        self.details_text = self.create_text_widget(self.details_tab)
        self.comparisons_text = self.create_text_widget(self.comparisons_tab)

        # Create frame for charts in factors tab
        self.factors_frame = ttk.Frame(self.factors_tab)
        self.factors_frame.pack(fill=tk.BOTH, expand=True)

        # Configure text tags
        self.configure_text_tags()

        return self.results_container

    def create_text_widget(self, parent):
        # Create container frame for better padding control
        container = ttk.Frame(parent)
        container.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        text = tk.Text(
            container,
            wrap=tk.WORD,
            font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZES["regular"]),
            bg=StyleConfig.COLOR_BACKGROUND,
            fg=StyleConfig.COLOR_TEXT,
            padx=5,  # Add internal padding
            pady=5
        )

        scrollbar = ttk.Scrollbar(container, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)

        # Pack scrollbar first to prevent it from being compressed
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        return text

    def init_comparison_data(self):
        self.comparison_data = {
            'elephant': {
                'weight': 6000,  # kg
                'name': '🐘 African Elephants',
                'text': 'Equal to {:.2f} elephants',
                'description': 'Adult African elephants weigh about 6,000 kg'
            },
            'beetle': {
                'weight': 1200,  # kg
                'name': '🚗 VW Beetles',
                'text': 'Weighs as much as {:.2f} Volkswagen Beetles',
                'description': 'Classic VW Beetles weigh about 1,200 kg'
            },
            'whale': {
                'weight': 150000,  # kg
                'name': '🐋 Blue Whales',
                'text': 'Equal to {:.2f} blue whales',
                'description': 'Blue whales weigh about 150,000 kg'
            },
            'car': {
                'weight': 1500,  # kg
                'name': '🚙 Cars',
                'text': 'Weighs as much as {:.2f} average cars',
                'description': 'Average car weighs about 1,500 kg'
            },
            'pool': {
                'volume': 2500000,  # liters
                'name': '🏊 Olympic Swimming Pools',
                'text': 'Would fill {:.2f}% of an Olympic swimming pool',
                'description': 'Olympic swimming pool holds 2,500,000 liters'
            },
            'bathtub': {
                'volume': 150,  # liters
                'name': '🛁 Bathtubs',
                'text': 'Would fill {:.2f} bathtubs',
                'description': 'Average bathtub holds 150 liters'
            }
        }

    def configure_text_tags(self):
        """Configure text tags for styling"""
        for text_widget in [self.summary_text, self.details_text, self.comparisons_text]:
            text_widget.tag_config(
                'bold',
                font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZES["large"], 'bold')
            )
            text_widget.tag_config(
                'italic',
                font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZES["regular"], 'italic')
            )
            text_widget.tag_config(
                'header',
                font=(StyleConfig.FONT_FAMILY, StyleConfig.FONT_SIZES["title"], 'bold'),
                foreground=StyleConfig.COLOR_PRIMARY
            )

    @ErrorHandler.handle_exception_decorator
    def calculate_total_poop(self, age_years, poop_per_day, grams_per_poop):
        total_kg = (age_years * 365 * poop_per_day * grams_per_poop) / 1000  # Convert grams to kg
        return total_kg

    @ErrorHandler.handle_exception_decorator
    def display_results(self, all_inputs):
        """Display results based on collected data from previous steps"""
        if not all_inputs:
            self.results_text.insert('end', "No data available to display.")
            return

        # Calculate totals
        total_kg = self.calculate_total_poop(
            all_inputs.get('age_years', 0),
            all_inputs.get('poop_per_day', 0),
            all_inputs.get('grams_per_poop', 0)
        )

        # Display summary
        self.display_summary(total_kg, all_inputs.get('total_poops', 0), all_inputs.get('adjustment_factor', 1.0))

        # Display details
        self.display_details(all_inputs, total_kg, all_inputs.get('adjustment_factor', 1.0))

        # Display comparisons
        self.display_comparisons(total_kg)

        # Display factors
        self.display_factors(all_inputs.get('factors', []))

    def display_summary(self, total_kg, total_poops, adjustment_factor):
        self.summary_text.delete('1.0', tk.END)
        self.summary_text.insert('1.0', f"✨ Summary:\n\n", 'header')
        self.summary_text.insert('end', f"Total Poop Weight: {total_kg:.2f} kg\n")
        self.summary_text.insert('end', f"Total Poops: {total_poops}\n")
        self.summary_text.insert('end', f"Adjustment Factor: {adjustment_factor:.2f}x\n")

    def display_details(self, all_inputs, total_kg, adjustment_factor):
        self.details_text.delete('1.0', tk.END)
        self.details_text.insert('1.0', f"🔍 Details:\n\n", 'header')
        
        for key, value in all_inputs.items():
            self.details_text.insert('end', f"{key.capitalize()}: {value}\n")
        
        self.details_text.insert('end', "\nCalculations:\n")
        self.details_text.insert('end', f"Total Weight: {total_kg:.2f} kg\n")
        self.details_text.insert('end', f"Adjustment Factor: {adjustment_factor:.2f}x\n")

    def display_comparisons(self, total_kg):
        self.comparisons_text.delete('1.0', tk.END)
        self.comparisons_text.insert('1.0', f"🔄 Comparisons:\n\n", 'header')
        
        for comparison_key, comparison_data in self.comparison_data.items():
            if 'weight' in comparison_data:
                comparison_value = total_kg / comparison_data['weight']
                self.comparisons_text.insert('end', comparison_data['text'].format(comparison_value), 'bold\n')
                self.comparisons_text.insert('end', f"  {comparison_data['description']}\n\n")
            elif 'volume' in comparison_data:
                comparison_value = (total_kg * 1000) / comparison_data['volume'] * 100  # Convert kg to liters and calculate percentage
                self.comparisons_text.insert('end', comparison_data['text'].format(comparison_value), 'bold\n')
                self.comparisons_text.insert('end', f"  {comparison_data['description']}\n\n")

    def display_factors(self, factors):
        self.factors_frame.delete('1.0', tk.END)
        self.factors_frame.insert('1.0', f"📊 Impact Factors:\n\n", 'header')
        
        for factor, value in factors.items():
            self.factors_frame.insert('end', f"{factor}: {value}\n")

    @ErrorHandler.handle_exception_decorator
    def store_input(self) -> dict:
        """
        Store and return the step's input data.
        This step doesn't store any inputs as it's the results display step.
        Returns:
            dict: Empty dictionary as this step doesn't store data
        """
        return {}

    def validate(self) -> bool:
        """
        Validate the step's input.
        This step doesn't require validation as it's display-only.
        Returns:
            bool: Always returns True as no validation is needed
        """
        return True