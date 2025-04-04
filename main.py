from supply_chain_tool.loader import SupplyChainLoader
from supply_chain_tool.analyzer import SupplyChainAnalyzer

import pandas

pandas.set_option("display.max_columns", None)
# 1. Load data
loader = SupplyChainLoader()
df = loader.load_data("data/supply_chain_data.csv")
print("\nOriginal data:")
print(df.head(5))

# 2. Validate data
df_clean = loader.validate_data(df)
print("\nCleaned data, nothing should change:")
print(df_clean.head(5))

# 3. Filter examples
filtered_by_product = loader.filter_by_product_type(df_clean, "haircare")
filtered_by_supplier = loader.filter_by_supplier(df_clean, "Supplier 1")
print("\nOnly Haircare products:")
print(filtered_by_product.head(5))
print("\nOnly the first Supplier:")
print(filtered_by_supplier.head(5))

# 4. Revenue analysis and its visualization
analyzer = SupplyChainAnalyzer()
revenue_by_type = analyzer.revenue_by_product_type(df_clean)
print("\nRevenue generated by product type:")
print(revenue_by_type)
analyzer.plot_revenue_by_product_type(df_clean)

# 5. Profitability ranking
ranked_profit = analyzer.ranked_profitability(df_clean)
print("\nTop 10 most profitable products:")
print(ranked_profit.head(10))
print("\n10 least profitable products:")
print(ranked_profit.tail(10))

# 8. Algorithm for reordering products
reorder_plan = analyzer.generate_reorder_plan(df_clean)
print("\nReorder recommendations given the current demand and lead times:")
print(reorder_plan.head(10))
