import abc
from backtesting.signal import StdDevPairSignal

class Strategy(abc.ABC):
    """
    Abstract base class for defining trading strategies.

    Attributes:
    - kwargs (dict): Additional keyword arguments for strategy initialization.

    Methods:
    - __init__(self, **kwargs): Initializes a new Strategy instance.
    - __call__(self, index, price_args, **kwargs): Abstract method to produce a tuple of trading orders based on a DataFrame iterrows() input.

    Notes:
    - Subclasses must implement the __call__ method.
    """
    def __init__(self, **kwargs):
        """
        Initializes a new Strategy instance.

        Parameters:
        - kwargs (dict): Additional keyword arguments for strategy initialization.
        """
        pass

    @abc.abstractmethod
    def __call__(self, index, price_args, **kwargs):
        """
        Abstract method to produce a tuple of trading orders based on a DataFrame iterrows() input.

        Parameters:
        - index: Current date.
        - price_args: A pandas series of the returns of the asset for the current day.

        Returns:
        Tuple: A tuple of trading orders.
        """
        pass


class FuturesStdPairStrategy(Strategy):
    """
    Strategy class implementing trading decisions based on standard deviation signals for futures contracts.

    Attributes:
    - kwargs (dict): Additional keyword arguments for strategy initialization.

    Methods:
    - __init__(self, **kwargs): Initializes a new FuturesStdPairStrategy instance.
    - __call__(self, index, price_args, **kwargs): Generates trading orders based on standard deviation signals.

    Notes:
    - Inherits from the abstract base class Strategy.
    """
    def __init__(self, **kwargs):
        """
        Initializes a new FuturesStdPairStrategy instance.

        Parameters:
        - kwargs (dict): Additional keyword arguments for strategy initialization.
        """
        super(FuturesStdPairStrategy, self).__init__(**kwargs)
        self.stdsignal = StdDevPairSignal(**kwargs)
        self.buy_size = kwargs.get("long_size", 10)
        self.short_size = kwargs.get("short_size", 10)

    def __call__(self, index, price_args, **kwargs):
        """
        Generates trading orders based on standard deviation signals.

        Parameters:
        - index: Current date.
        - price_args: A pandas series of the returns of the asset for the current day.

        Returns:
        Tuple: A tuple containing the asset name and the trading order size.
        """
        asset, std_signal = self.stdsignal(index, price_args)

        if std_signal == 1:
            # Buy
            return (asset, self.buy_size * std_signal)

        if std_signal == -1:
            # Sell
            return (asset, self.short_size * std_signal)

        else:
            # Close all positions
            return (asset, 'close')
