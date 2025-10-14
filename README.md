# Trade Simulator

A Monte Carlo simulation tool for analyzing trading performance based on user-defined parameters.

## 🚀 Quick Start

### Web App (Streamlit - Recommended)
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Command Line Interface
```bash
python3 trade_simulator.py
```

### Run Tests
```bash
python3 test_simulator.py
```

## Features

- **Monte Carlo Simulation**: Run multiple trials to simulate trading performance
- **Interactive Web Interface**: Beautiful Streamlit UI with real-time charts
- **Customizable Parameters**: 
  - Number of trials and trades per trial
  - Win/loss percentage ranges
  - Win rate
  - Starting capital
  - Overhead costs (commissions and slippage)
  
- **Comprehensive Statistics**:
  - Net profit/loss
  - Win rate and expectancy
  - Maximum drawdown (dollars and percentage)
  - Consecutive win/loss streaks
  - Profit factor
  - Probability of ruin
  - Odds of losing streaks

- **Visualizations**:
  - Interactive equity curve with Plotly
  - Moving average overlay
  - Performance metrics dashboard

## Files

- `app.py` - Streamlit web application (recommended)
- `trade_simulator.py` - Core simulator engine & CLI
- `test_simulator.py` - Test script with examples
- `requirements.txt` - Python dependencies

## Usage

### Streamlit Web App

The web app provides an intuitive interface with:
- **Sidebar controls** for all parameters
- **Real-time visualization** of equity curves
- **Interactive charts** with zoom and hover details
- **Tabbed statistics** for detailed analysis

Simply adjust the parameters and click "Run Simulation"!

### Command Line

Run the CLI version:
```bash
python3 trade_simulator.py
```

The program will prompt you for parameters. Press Enter to use default values:

- **Number of trials**: 1 (use more trials to see statistical distribution)
- **Trades per trial**: 50
- **Profit range**: 5% to 25% on winning trades
- **Loss range**: 10% to 25% on losing trades
- **Win percentage**: 75%
- **Starting capital**: $100,000
- **Overhead**: 0.3% (commissions and slippage)
- **Moving average bars**: 30

## Example Output

```
TRADE PERFORMANCE SUMMARY
Total Net Profit:        $266,188
Wins:                    32 (64.0%)
Losses:                  18 (36.0%)
Average profit:          $35,700
Average loss:            ($48,658)
Expectancy:              $14,610.22
Max consecutive wins:    4 (odds 3.2:1)
Max consecutive losses:  2 (odds 16.0:1)
```

## Understanding the Results

- **Expectancy**: Average amount you can expect to win per trade
- **Profit Factor**: Ratio of gross profit to gross loss (>1 is profitable)
- **Maximum Drawdown**: Largest peak-to-trough decline during the simulation
- **Probability of Ruin**: Likelihood of losing money over the simulation period
- **Losing Streak Odds**: Statistical probability of consecutive losses

## Requirements

- Python 3.7 or higher
- Streamlit (for web app)
- Plotly (for interactive charts)
- Pandas (for data handling)

Standard library only for CLI version (no dependencies needed).

## Installation

```bash
# Clone or download the files
pip install -r requirements.txt
streamlit run app.py
```

## License

Open source - feel free to use and modify!
