import numpy as np

class Tracker:
    """
    Tracker class for monitoring price movements and calculating moving averages.

    Attributes:
    - n (int): Number of days for the moving average calculation.
    - prev_date (datetime): Date of the previous price observation.
    - prev_price (float): Previous observed price.
    - day_return (float): Daily return calculated as (price / prev_price) - 1.0.
    - price_window (list): List of recent prices used for moving average calculation.
    - moving_average (float): Moving average of recent prices.
    - std (float): Standard deviation of recent prices.

    Methods:
    - __init__(self, n): Initializes a new Tracker instance with the specified number of days for the moving average.
    - __call__(self, date, price): Updates the tracker with a new price observation.

    Note:
    The moving average and standard deviation are calculated only when a sufficient number of days' prices are available.
    """
    def __init__(self, n):
        """
        Initialize a new Tracker instance.

        Parameters:
        - n (int): Number of days for the moving average calculation.
        """
        self.prev_date, self.prev_price = None, 0.0
        self.day_return = 0.0

        self.n = n
        self.price_window = []
        self.moving_average, self.std = 0.0, 0.0

    def __call__(self, date, price):
        """
        Update the tracker with a new price observation.

        Parameters:
        - date (datetime): Date of the new price observation.
        - price (float): Price value.
        """
        self.price_window.append(price)
        if len(self.price_window) > self.n:
            self.price_window.pop()

            if any(np.isnan(price) for price in self.price_window):
                self.moving_average = np.nan
                self.std = np.nan
                        
            else:
                self.moving_average = sum(self.price_window) / len(self.price_window)

                avg_err_sq = [pow(value - self.moving_average, 2) for value in self.price_window]
                self.std = sum(avg_err_sq) / len(self.price_window)

            self.day_return = 0 if self.prev_price == 0 else (price / self.prev_price) - 1.0 if not(np.isnan(price)) and not(np.isnan(self.prev_price)) else np.nan
            self.prev_price = price
            self.prev_date = date
