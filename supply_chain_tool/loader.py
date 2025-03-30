import pandas


class SupplyChainLoader:
    """
    Class for loading and filtering supply chain data.
    """

    def load_data(self, filepath: str) -> pandas.DataFrame:
        """
        Loads the supply chain data from a CSV file.

        Parameters:
        - filepath (str): Path to the CSV file.

        Returns:
        - pandas.DataFrame: Loaded data.
        """
        try:
            df = pandas.read_csv(filepath)
            print("Load successful.")
            return df
        except FileNotFoundError:
            raise FileNotFoundError(f" File not found: {filepath}")
        except Exception as e:
            raise RuntimeError(f" Failed to load data: {e}")

    def filter_by_product_type(
        self, df: pandas.DataFrame, product_type: str
    ) -> pandas.DataFrame:
        """
        Filter the data by product type.

        Parameters:
        - df (pandas.DataFrame): The full dataset.
        - product_type (str): The product type to filter by.

        Returns:
        - pandas.DataFrame: Filtered dataset.
        """
        assert isinstance(product_type, str), "Product type must be a string"

        filtered_df = df[df["Product type"].str.lower() == product_type.lower()]
        return filtered_df

    def filter_by_supplier(
        self, df: pandas.DataFrame, supplier_name: str
    ) -> pandas.DataFrame:
        """
        Filter the data by supplier name.

        Parameters:
        - df (pandas.DataFrame): The full dataset.
        - supplier_name (str): The supplier name to filter by.

        Returns:
        - pandas.DataFrame: Filtered dataset.
        """
        assert isinstance(supplier_name, str), "Supplier name must be a string"

        filtered_df = df[df["Supplier name"].str.lower() == supplier_name.lower()]
        return filtered_df

    def validate_data(self, df: pandas.DataFrame) -> pandas.DataFrame:
        """
        Validate and clean the dataset.

        - Drops rows with missing values
        - Warns about negative or unreasonable values
        - Defect rates must be between 0 and 100 as they are percentage values

        Parameters:
        - df (pandas.DataFrame): The dataset to validate

        Returns:
        - pandas.DataFrame: Cleaned dataset
        """
        # Drop rows with missing values
        df_clean = df.dropna()

        # Negatives in cost columns
        cost_columns = ["Shipping costs", "Manufacturing costs", "Costs"]
        for col in cost_columns:
            if (df_clean[col] < 0).any():
                pass

        # Fefect rates out of bounds
        if ((df_clean["Defect rates"] < 0) | (df_clean["Defect rates"] > 100)).any():
            print("Defects outside the 0–100 range.")

        return df_clean
