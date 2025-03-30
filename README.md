# Supply Chain Analytics Tool

This Python package provides tools for analyzing, visualizing, and optimizing supply chain data.

The package includes functionality for:
- Revenue and profitability analysis
- Reorder recommendations based on supply chain factors
- Data validation and filtering
- Basic visualization

---

## Project Description

The dataset used in this project comes from a fashion and beauty company’s supply chain. It includes detailed information on:

- Product sales and pricing
- Inventory availability and stock levels
- Lead times and costs
- Supplier and manufacturing details

The goal of the project was to create a Python package that performs a series of supply chain analyses.

**Data Source:**  
[Supply Chain Analysis – Kaggle Dataset](https://www.kaggle.com/datasets/harshsingh2209/supply-chain-analysis)

---

## Installation

To install the package locally:

```bash
git clone https://github.com/EmmaKliushnichenko/supply-chain-tool.git
cd supply-chain-tool
pip install -e .
```

Make sure the following Python packages are installed:

- pandas
- matplotlib

You can also install dependencies using:

```bash
pip install -r requirements.txt
```

---

## Usage Example

The file main.py in the project root can be used as well.

```python
from supply_chain_tool.loader import SupplyChainLoader
from supply_chain_tool.analyzer import SupplyChainAnalyzer

# Load and validate data
loader = SupplyChainLoader()
df = loader.load_data("data/supply_chain_data.csv")
df_clean = loader.validate_data(df)

# Analyze revenue and plot
analyzer = SupplyChainAnalyzer()
analyzer.plot_revenue_by_product_type(df_clean)

# Profitability ranking
profit_table = analyzer.ranked_profitability(df_clean)

# Generate reorder plan
reorder_plan = analyzer.generate_reorder_plan(df_clean)
```

---

## Tutorial

See `TUTORIAL.ipynb` for a step-by-step walkthrough of the package with example outputs.

---

## License

This project is licensed under the MIT License.  
See `LICENSE.txt` for details.

---

## Code Style

This project follows the PEP8 style guide and was auto-formatted using [`black`]
