import numpy as np
import matplotlib.pyplot as plt
from backtesting.strategy import FuturesStdPairStrategy, Strategy

class Backtest:
    """
    Class for conducting backtesting of trading strategies.

    Attributes:
    - dataset: Dataset containing historical price data.
    - strategy: Trading strategy to be backtested.
    - cash (float): Initial cash amount for the backtest.
    - kwargs (dict): Additional keyword arguments for backtest initialization.

    Methods:
    - __init__(self, dataset, strategy, cash=1000000, **kwargs): Initializes a new Backtest instance.
    - plot_pnl(self): Plots the cumulative profit and loss over time.
    - plot_drawdown(self): Plots the drawdown over time.
    - summary(self): Prints a summary of backtest results.

    Notes:
    - The backtest assumes daily frequency data.
    """
    def __init__(self, dataset, strategy, cash=1000000, **kwargs):
        """
        Initializes a new Backtest instance.

        Parameters:
        - dataset: Dataset containing historical price data.
        - strategy: Trading strategy to be backtested.
        - cash (float): Initial cash amount for the backtest.
        - kwargs (dict): Additional keyword arguments for backtest initialization.
        """
        self.dataset = dataset
        
        if not isinstance(strategy, Strategy):
            match strategy.lower():
                case 'future_pairs_strategy' | 'futurepairsstrategy':
                    strategy = FuturesStdPairStrategy(**kwargs)
                case _:
                    raise KeyError(f'Strategy "{strategy}" not recognized!')
        self.strategy = strategy

        self.t_cost = kwargs.get('C', 0.1)
        
        self.initial_value = self.cash = cash
        self.position_value = 0
        self.position_size = 0
        self.prev_price = np.nan
        
        self.max_value = self.initial_value
        self.pnl = []
        self.drawdown = []

        for index, row in self.dataset.df.iterrows():

            asset, trade_size = strategy(index, row, **kwargs)
            price = row[asset]

            if not np.isnan(price):

                if self.prev_price == 0 or np.isnan(price) or np.isnan(self.prev_price):
                    self.day_return = 0    
                else: 
                    self.day_return =  (price/self.prev_price) - 1
                
                self.prev_price = price
                
                self.position_value += self.position_value * self.day_return*self.position_size
                
                
                if trade_size == 'close':
                    self.cash += self.position_value - self.t_cost
                    self.position_value = 0
    
                elif self.cash >= abs(trade_size)*price + self.t_cost:
                    self.cash -= abs(trade_size)*price - self.t_cost
                    self.position_size += trade_size
                    self.position_value += trade_size*price

                
                total_value = self.position_value + self.cash
                self.pnl.append(total_value)


                profit = total_value- self.initial_value
                self.max_value = max(self.max_value, profit)

                drawdown = (self.max_value-total_value)/self.max_value
                self.drawdown.append(drawdown)
            
            else:
                self.pnl.append(self.position_value + self.cash)
                self.drawdown.append(0)
        
        self.results_df = self.dataset.df.copy()
        self.results_df['Cumulative_Pnl'] = self.pnl
        self.results_df['Drawdown'] = self.drawdown

    def plot_pnl(self):
        """
        Plots the cumulative profit and loss over time.
        """
        plt.figure(figsize=(12, 6))
        plt.plot(self.results_df.index, self.results_df['Cumulative_Pnl'])
        plt.xlabel('Date')
        plt.ylabel('Cumulative PnL')
        plt.title('Cumulative Profit and Loss Over Time')
        plt.grid(True)
        plt.show()
        
    def plot_drawdown(self):
        """
        Plots the drawdown over time.
        """
        plt.figure(figsize=(12, 6))
        plt.plot(self.results_df.index, self.results_df['Drawdown'], label='Drawdown', color='red')

        # Add title and labels
        plt.title("Drawdown Over Time")
        plt.xlabel("Date")
        plt.ylabel("Drawdown")

        plt.legend()
        plt.show()
        
    def summary(self):
        """
        Prints a summary of backtest results, including annualized return, Sharpe ratio, and max drawdown.
        """
        self.results_df['Daily_Return'] = self.results_df['Cumulative_Pnl'].pct_change().replace([np.inf, -np.inf, np.nan], 0)
        self.results_df['Cumulative_Return'] = (1 + self.results_df['Daily_Return']).cumprod() - 1

        annualized_return = (1 + self.results_df['Cumulative_Return'].iloc[-1]) ** (252 / self.dataset.df.shape[0]) - 1

        # Calculate the Sharpe ratio
        mean_daily_return = self.results_df['Daily_Return'].mean()
        std_daily_return = self.results_df['Daily_Return'].std()

        # Assuming 252 trading days in a year
        number_of_trading_days = 252

        sharpe_ratio = (mean_daily_return / std_daily_return) * np.sqrt(number_of_trading_days)
        # Calculate max drawdown
        max_drawdown = self.results_df['Drawdown'].max()

        print(f"{self.strategy.__class__.__name__} summary \n"
                f"Annualized return: {annualized_return}\n"
                f"Sharpe ratio: {sharpe_ratio} \n"
                f"Max drawdown: {max_drawdown}"
                    )
