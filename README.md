# backtest-framework

Modular Backtest Framework for trading strategy allowing high customization thanks to OOP paradygm.

## Usage

Use the backtesting framework to create, evaluate and analyze your trading strategies.
You can create your own signals and strategy by customizing the respective templates, making sure that output formats stay the same. You can also customize the backtesting report and the tracker calculations based on your needs.

A basic example can be found in `example_stdev_pairtrading_backtest.ipynb`.

## Project Structure

```plaintext
backtest-framework/
|-- src/
|   |-- __init__.py
|   |-- backtest.py
|   |-- signal.py
|   |-- strategy.py
|   |-- tracker.py
|   |-- utils.py
|-- example_data/
|   |-- futuresA.csv
|   |-- futuresB.csv
|-- example_stdev_pairtrading_backtest.ipynb
|-- README.md
|-- LICENSE
```
