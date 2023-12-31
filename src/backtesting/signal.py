import abc
from backtesting.tracker import Tracker
import numpy as np


class Signal(abc.ABC):
    """
    Abstract base class for defining trading signals.

    Attributes:
    - kwargs (dict): Additional keyword arguments for signal initialization.

    Methods:
    - __init__(self, **kwargs): Initializes a new Signal instance.
    - __call__(self, index, price_args, **kwargs): Abstract method to produce a tuple of signals based on a DataFrame iterrows() input.

    Notes:
    - Subclasses must implement the __call__ method.
    """
    def __init__(self, **kwargs):
        """
        Initializes a new Signal instance.

        Parameters:
        - kwargs (dict): Additional keyword arguments for signal initialization.
        """
        pass

    @abc.abstractmethod
    def __call__(self, index, price_args, **kwargs):
        """
        Abstract method to produce a tuple of signals based on a DataFrame iterrows() input.

        Parameters:
        - index: Current date.
        - price_args: A pandas series of the returns of the asset for the current day.
        
        Returns:
        Tuple: A tuple of signals.
        """
        pass


class StdDevPairSignal(Signal):
    """
    Signal class for generating trading signals based on the standard deviation of a pair of assets.

    Attributes:
    - asset_a (str): Name of the first asset.
    - asset_b (str): Name of the second asset.
    - n_days (int): Number of days for standard deviation calculation.
    - std_rise (float): Threshold for signaling a rise based on standard deviation.
    - std_drop (float): Threshold for signaling a drop based on standard deviation.
    - kwargs (dict): Additional keyword arguments for signal initialization.

    Methods:
    - __init__(self, asset_a, asset_b, n_days, std_rise, std_drop, **kwargs): Initializes a new StdDevPairSignal instance.
    - __call__(self, index, price_args, **kwargs): Generates a tuple of signals based on the standard deviation of asset returns.

    Notes:
    - Inherits from the abstract base class Signal.
    """
    def __init__(self, asset_a, asset_b, n_days, std_rise, std_drop, **kwargs):
        """
        Initializes a new StdDevPairSignal instance.

        Parameters:
        - asset_a (str): Name of the first asset.
        - asset_b (str): Name of the second asset.
        - n_days (int): Number of days for standard deviation calculation.
        - std_rise (float): Threshold for signaling a rise based on standard deviation.
        - std_drop (float): Threshold for signaling a drop based on standard deviation.
        - kwargs (dict): Additional keyword arguments for signal initialization.
        """
        super(StdDevPairSignal, self).__init__(**kwargs)
        self.asset_a, self.asset_b = asset_a, asset_b
        self.tracker = Tracker(n_days)

        self.std_rise, self.std_drop = std_rise, std_drop
        self.n_days = n_days

    def __call__(self, index, price_args, **kwargs):
        """
        Generates a tuple of signals based on the standard deviation of asset returns.

        Parameters:
        - index: Current date.
        - price_args: A pandas series of the returns of the assets for the current day.

        Returns:
        Tuple: A tuple containing the name of the asset and the generated signal.
        """
        current_price = price_args[self.asset_b]
        signal = 0.0

        if np.isnan(current_price) or np.isnan(price_args[self.asset_a]) or np.isnan(self.tracker.std):
            signal = 0
        else:
            self.tracker(index, current_price)
            if self.tracker.std * self.std_rise < self.tracker.day_return:
                signal = 1.0
            if self.tracker.day_return < -self.tracker.std * self.std_drop:
                signal = -1.0

        return (self.asset_a, signal)
