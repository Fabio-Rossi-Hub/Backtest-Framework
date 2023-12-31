import pandas as pd

class CSVDataset:
    """
    Class for handling and cleaning CSV datasets containing price information.

    Attributes:
    - _price_columns (list): List of column names representing price information.

    Methods:
    - __init__(self, **kwargs): Initializes a new CSVDataset instance.
    - get_key(key): Static method to format keys for price columns.

    Notes:
    - Assumes input CSV files have columns 'Date' and price columns listed in _price_columns.
    """
    _price_columns = ['Close', 'Last']

    def __init__(self, **kwargs):
        """
        Initializes a new CSVDataset instance.

        Parameters:
        - kwargs: Dictionary with keys as identifiers and values as paths to CSV files.

        Notes:
        - Assumes input CSV files have columns 'Date' and price columns listed in _price_columns.
        """
        # Input CSV cleaning
        name_mapper = {key: 'Price' for key in self._price_columns}

        df_read = {key: (
            pd.read_csv(path)
            .rename(columns=name_mapper)
        ) for key, path in kwargs.items()}

        df_series = dict()
        for key, df in df_read.items():
            df['date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y")
            df_series[self.get_key(key)] = (
                df.set_index('date')
                .sort_index()['Price']
            )

        # Dataframe merging
        self.df = pd.DataFrame.from_dict(df_series)

    @staticmethod
    def get_key(key):
        """
        Static method to format keys for price columns.

        Parameters:
        - key: Identifier for the dataset.

        Returns:
        str: Formatted key for price columns.
        """
        return f'{key} Price'


class FuturesPairDataset(CSVDataset):
    """
    Class for handling and cleaning CSV datasets specific to futures pairs.

    Attributes:
    - path_a (str): Path to the CSV file for asset A.
    - path_b (str): Path to the CSV file for asset B.

    Methods:
    - __init__(self, path_a, path_b): Initializes a new FuturesPairDataset instance.

    Notes:
    - Inherits from the CSVDataset class.
    """
    def __init__(self, path_a, path_b):
        """
        Initializes a new FuturesPairDataset instance.

        Parameters:
        - path_a (str): Path to the CSV file for asset A.
        - path_b (str): Path to the CSV file for asset B.

        Notes:
        - Inherits from the CSVDataset class.
        """
        super(FuturesPairDataset, self).__init__(A=path_a, B=path_b)
