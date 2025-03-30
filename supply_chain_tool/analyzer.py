import pandas
import matplotlib.pyplot as matplotlib


class SupplyChainAnalyzer:
    """
    Class for analyzing supply chain performance metrics.
    """

    def revenue_by_product_type(self, df: pandas.DataFrame) -> pandas.DataFrame:
        """
        Total revenue for each product type.

        Parameters:
        - df (pandas.DataFrame): The supply chain data set.

        Returns:
        - pandas.DataFrame: Product types with total revenue.
        """
        result = df.groupby("Product type")["Revenue generated"].sum().reset_index()
        result = result.sort_values(by="Revenue generated", ascending=False)
        return result

    def plot_revenue_by_product_type(self, df: pandas.DataFrame) -> None:
        """
        Plot total revenue for each product type as a bar chart.

        Parameters:
        - df (pandas.DataFrame): The supply chain data set.
        """
        revenue_df = self.revenue_by_product_type(df)

        matplotlib.figure(figsize=(8, 5))
        matplotlib.bar(revenue_df["Product type"], revenue_df["Revenue generated"])
        matplotlib.title("Total Revenue by Product Type")
        matplotlib.xlabel("Product Type")
        matplotlib.ylabel("Revenue")
        matplotlib.grid(True)
        matplotlib.tight_layout()
        matplotlib.show()

    def ranked_profitability(self, df: pandas.DataFrame) -> pandas.DataFrame:
        """
        Rank all products by actual profit, adjusted for defect rates.

        Adds columns for:
        - Total profit
        - Profit per unit sold
        - Profit margin (%)

        Parameters:
        - df (pandas.DataFrame): The supply chain dataset.

        Returns:
        - pandas.DataFrame: Ranked list of SKUs with profit, profit per unit, and margin.
        """
        df = df.copy()

        # Revenue without defects
        df["Effective Revenue"] = (
            df["Price"] * df["Number of products sold"] * (1 - df["Defect rates"] / 100)
        )

        # Profit = revenue - total cost
        df["Profit"] = df["Effective Revenue"] - df["Costs"]

        # Profit per unit sold
        df["Profit Per Unit"] = df["Profit"] / df["Number of products sold"]

        # Profit margin as percent of revenue
        df["Profit Margin"] = df["Profit"] / df["Effective Revenue"]
        df["Profit Margin"] = df["Profit Margin"].replace(
            [float("inf"), -float("inf")], 0
        )

        ranked = df[
            ["SKU", "Product type", "Profit", "Profit Per Unit", "Profit Margin"]
        ]
        ranked = ranked.sort_values(by="Profit", ascending=False).reset_index(drop=True)
        return ranked

    def generate_reorder_plan(self, df: pandas.DataFrame) -> pandas.DataFrame:
        """
        A reordering algorithm based on stock levels, lead times, and demand.
        Uses low/medium/high tiers and includes demand + lead time ranks.

        Returns:
        - pandas.DataFrame: SKU, Reorder Decision, Suggested Quantity, Reason, Ranks
        """
        df = df.copy()

        # Lead times are given in three different categories, best is to aggregate them
        df["Total Lead Time"] = (
            df["Lead time"] + df["Lead times"] + df["Manufacturing lead time"]
        )

        # Demand and lead time ranks, descending
        df["Demand Rank"] = (
            df["Number of products sold"]
            .rank(method="min", ascending=False)
            .astype(int)
        )
        df["Lead Time Rank"] = (
            df["Total Lead Time"].rank(method="min", ascending=False).astype(int)
        )

        # Quantile thresholds defined for low-medium-high groupings
        demand_q1 = df["Number of products sold"].quantile(0.33)
        demand_q2 = df["Number of products sold"].quantile(0.67)
        lead_q1 = df["Total Lead Time"].quantile(0.33)
        lead_q2 = df["Total Lead Time"].quantile(0.67)

        decisions = []

        for i in range(len(df)):
            row = df.iloc[i]

            demand = row["Number of products sold"]
            lead_time = row["Total Lead Time"]
            stock = row["Stock levels"]
            availability = row["Availability"]
            sku = row["SKU"]

            # Tiers
            if demand < demand_q1:
                demand_level = "low"
            elif demand < demand_q2:
                demand_level = "medium"
            else:
                demand_level = "high"

            if lead_time < lead_q1:
                lead_level = "low"
            elif lead_time < lead_q2:
                lead_level = "medium"
            else:
                lead_level = "high"

            # Reorder thresholds
            reorder_thresholds = {
                ("high", "high"): (70, "High demand & high lead time"),
                ("high", "medium"): (60, "High demand & medium lead time"),
                ("high", "low"): (50, "High demand & low lead time"),
                ("medium", "high"): (55, "Medium demand & high lead time"),
                ("medium", "medium"): (45, "Medium demand & medium lead time"),
                ("medium", "low"): (35, "Medium demand & low lead time"),
                ("low", "high"): (40, "Low demand & high lead time"),
                ("low", "medium"): (30, "Low demand & medium lead time"),
                ("low", "low"): (20, "Low demand & low lead time"),
            }

            threshold, reason = reorder_thresholds[(demand_level, lead_level)]

            # Reorder logic
            if stock < threshold and availability >= 30:
                reorder = "Yes"
                buffer = 5
                while buffer < 15:
                    buffer += 1
                suggested_qty = int((demand * (lead_time / 10)) + buffer)
            else:
                reorder = "No"
                suggested_qty = 0

            decisions.append(
                {
                    "SKU": sku,
                    "Reorder": reorder,
                    "Suggested Quantity": suggested_qty,
                    "Reason": reason,
                    "Demand Rank": row["Demand Rank"],
                    "Lead Time Rank": row["Lead Time Rank"],
                }
            )
        return pandas.DataFrame(decisions)
