#!/usr/bin/env python3
"""
Trade Simulator - Monte Carlo simulation of trading performance
Simulates multiple trials of trades with user-defined win rate and risk/reward parameters
"""

import random
import statistics
from dataclasses import dataclass
from typing import List, Tuple
import sys


@dataclass
class TradeResult:
    """Represents a single trade result"""
    profit: float
    is_win: bool


@dataclass
class TrialResult:
    """Results from a single trial (series of trades)"""
    trades: List[TradeResult]
    final_equity: float
    max_equity: float
    min_equity: float
    max_drawdown_dollars: float
    max_drawdown_percent: float
    consecutive_wins: int
    consecutive_losses: int


@dataclass
class SimulationSummary:
    """Summary statistics across all trials"""
    total_net_profit: float
    wins: int
    losses: int
    win_rate: float
    average_profit: float
    average_loss: float
    expectancy: float
    max_consecutive_wins: int
    max_consecutive_losses: int
    equity_high: float
    equity_low: float
    ending_equity: float
    max_drawdown_dollars: float
    max_drawdown_percent: float
    max_dd_avg_profit_ratio: float
    profit_factor: float
    probability_of_ruin: float


class TradeSimulator:
    def __init__(
        self,
        num_trials: int = 1,
        trades_per_trial: int = 50,
        profit_min: float = 5.0,
        profit_max: float = 25.0,
        loss_min: float = 10.0,
        loss_max: float = 25.0,
        win_percentage: float = 75.0,
        starting_capital: float = 100000.0,
        overhead_percent: float = 0.003,
        moving_avg_bars: int = 30
    ):
        self.num_trials = num_trials
        self.trades_per_trial = trades_per_trial
        self.profit_min = profit_min / 100  # Convert to decimal
        self.profit_max = profit_max / 100
        self.loss_min = loss_min / 100
        self.loss_max = loss_max / 100
        self.win_percentage = win_percentage / 100
        self.starting_capital = starting_capital
        self.overhead_percent = overhead_percent
        self.moving_avg_bars = moving_avg_bars

    def simulate_trade(self, current_equity: float) -> TradeResult:
        """Simulate a single trade"""
        is_win = random.random() < self.win_percentage
        
        if is_win:
            profit_percent = random.uniform(self.profit_min, self.profit_max)
            profit = current_equity * profit_percent
        else:
            loss_percent = random.uniform(self.loss_min, self.loss_max)
            profit = -current_equity * loss_percent
        
        # Apply overhead (commissions and slippage)
        overhead = current_equity * self.overhead_percent
        profit -= overhead
        
        return TradeResult(profit=profit, is_win=is_win)

    def calculate_losing_streak_odds(self) -> dict:
        """Calculate odds of various losing streaks"""
        losing_prob = 1 - self.win_percentage
        streaks = {}
        
        for streak_length in range(2, 11):
            odds = (1 / (losing_prob ** streak_length)) if losing_prob > 0 else float('inf')
            streaks[streak_length] = odds
        
        return streaks

    def simulate_trial(self) -> TrialResult:
        """Run a single trial (series of trades)"""
        equity = self.starting_capital
        trades = []
        equity_curve = [equity]
        
        current_consecutive_wins = 0
        current_consecutive_losses = 0
        max_consecutive_wins = 0
        max_consecutive_losses = 0
        
        for _ in range(self.trades_per_trial):
            trade = self.simulate_trade(equity)
            trades.append(trade)
            equity += trade.profit
            equity_curve.append(equity)
            
            # Track consecutive wins/losses
            if trade.is_win:
                current_consecutive_wins += 1
                current_consecutive_losses = 0
                max_consecutive_wins = max(max_consecutive_wins, current_consecutive_wins)
            else:
                current_consecutive_losses += 1
                current_consecutive_wins = 0
                max_consecutive_losses = max(max_consecutive_losses, current_consecutive_losses)
        
        # Calculate drawdown
        max_equity = max(equity_curve)
        min_equity = min(equity_curve)
        
        max_drawdown_dollars = 0
        max_drawdown_percent = 0
        peak = equity_curve[0]
        
        for value in equity_curve:
            if value > peak:
                peak = value
            drawdown = peak - value
            drawdown_percent = (drawdown / peak * 100) if peak > 0 else 0
            
            if drawdown > max_drawdown_dollars:
                max_drawdown_dollars = drawdown
                max_drawdown_percent = drawdown_percent
        
        return TrialResult(
            trades=trades,
            final_equity=equity,
            max_equity=max_equity,
            min_equity=min_equity,
            max_drawdown_dollars=max_drawdown_dollars,
            max_drawdown_percent=max_drawdown_percent,
            consecutive_wins=max_consecutive_wins,
            consecutive_losses=max_consecutive_losses
        )

    def run_simulation(self) -> SimulationSummary:
        """Run the full simulation with all trials"""
        all_trials = []
        
        for _ in range(self.num_trials):
            trial = self.simulate_trial()
            all_trials.append(trial)
        
        # Aggregate results
        all_trades = [trade for trial in all_trials for trade in trial.trades]
        winning_trades = [t for t in all_trades if t.is_win]
        losing_trades = [t for t in all_trades if not t.is_win]
        
        total_wins = len(winning_trades)
        total_losses = len(losing_trades)
        total_trades = len(all_trades)
        
        win_rate = (total_wins / total_trades * 100) if total_trades > 0 else 0
        
        avg_profit = statistics.mean([t.profit for t in winning_trades]) if winning_trades else 0
        avg_loss = statistics.mean([t.profit for t in losing_trades]) if losing_trades else 0
        
        total_profit = sum([t.profit for t in winning_trades])
        total_loss = abs(sum([t.profit for t in losing_trades]))
        
        profit_factor = (total_profit / total_loss) if total_loss > 0 else 0
        
        expectancy = (win_rate / 100 * avg_profit) + ((1 - win_rate / 100) * avg_loss)
        
        max_consecutive_wins = max([trial.consecutive_wins for trial in all_trials])
        max_consecutive_losses = max([trial.consecutive_losses for trial in all_trials])
        
        final_equities = [trial.final_equity for trial in all_trials]
        equity_high = max(final_equities) if final_equities else self.starting_capital
        equity_low = min(final_equities) if final_equities else self.starting_capital
        ending_equity = statistics.mean(final_equities) if final_equities else self.starting_capital
        
        max_dd_dollars = max([trial.max_drawdown_dollars for trial in all_trials])
        max_dd_percent = max([trial.max_drawdown_percent for trial in all_trials])
        
        max_dd_avg_profit = (max_dd_dollars / abs(avg_profit)) if avg_profit != 0 else 0
        
        # Probability of ruin (simplified calculation)
        losing_trials = sum(1 for trial in all_trials if trial.final_equity < self.starting_capital)
        prob_of_ruin = (losing_trials / self.num_trials * 100) if self.num_trials > 0 else 0
        
        return SimulationSummary(
            total_net_profit=ending_equity - self.starting_capital,
            wins=total_wins,
            losses=total_losses,
            win_rate=win_rate,
            average_profit=avg_profit,
            average_loss=avg_loss,
            expectancy=expectancy,
            max_consecutive_wins=max_consecutive_wins,
            max_consecutive_losses=max_consecutive_losses,
            equity_high=equity_high,
            equity_low=equity_low,
            ending_equity=ending_equity,
            max_drawdown_dollars=max_dd_dollars,
            max_drawdown_percent=max_dd_percent,
            max_dd_avg_profit_ratio=max_dd_avg_profit,
            profit_factor=profit_factor,
            probability_of_ruin=prob_of_ruin
        )


def print_summary(summary: SimulationSummary, simulator: TradeSimulator):
    """Print the simulation summary in a formatted way"""
    print("\n" + "="*60)
    print("TRADE PERFORMANCE SUMMARY")
    print("="*60)
    
    print(f"\nTotal Net Profit:        ${summary.total_net_profit:,.2f}")
    print(f"Wins:                    {summary.wins} ({summary.win_rate:.1f}%)")
    print(f"Losses:                  {summary.losses} ({100-summary.win_rate:.1f}%)")
    print(f"Average profit:          ${summary.average_profit:,.2f}")
    print(f"Average loss:            (${abs(summary.average_loss):,.2f})")
    print(f"Expectancy:              ${summary.expectancy:,.2f}")
    print(f"Max consecutive wins:    {summary.max_consecutive_wins} (odds {summary.max_consecutive_wins}.2:1)")
    print(f"Max consecutive losses:  {summary.max_consecutive_losses} (odds {summary.max_consecutive_losses}.0:1)")
    print(f"Equity high value:       ${summary.equity_high:,.2f}")
    print(f"Equity low value:        ${summary.equity_low:,.2f}")
    print(f"Ending Equity:           ${summary.ending_equity:,.2f}")
    
    print(f"\nMaximum Draw Down Dollars:  ${summary.max_drawdown_dollars:,.2f}")
    print(f"Maximum Draw Down Percent:  {summary.max_drawdown_percent:.1f}%")
    print(f"Max Draw Down/Average Profit: {summary.max_dd_avg_profit_ratio:.2f}")
    print(f"Profit Factor:              {summary.profit_factor:.2f}")
    print(f"Probability of Ruin:        {summary.probability_of_ruin:.4f}%")
    
    print("\n" + "="*60)
    print("ODDS OF LOSING STREAKS")
    print("="*60)
    
    streak_odds = simulator.calculate_losing_streak_odds()
    for streak, odds in streak_odds.items():
        if odds != float('inf'):
            print(f"Losing Streak {streak}: {odds:,.0f}:1")


def get_float_input(prompt: str, default: float) -> float:
    """Get float input from user with default value"""
    user_input = input(f"{prompt} [{default}]: ").strip()
    if not user_input:
        return default
    try:
        return float(user_input)
    except ValueError:
        print(f"Invalid input. Using default: {default}")
        return default


def get_int_input(prompt: str, default: int) -> int:
    """Get integer input from user with default value"""
    user_input = input(f"{prompt} [{default}]: ").strip()
    if not user_input:
        return default
    try:
        return int(user_input)
    except ValueError:
        print(f"Invalid input. Using default: {default}")
        return default


def main():
    """Main function to run the trade simulator"""
    print("\n" + "="*60)
    print("TRADE SIMULATOR - Monte Carlo Analysis")
    print("="*60)
    print("\nPress Enter to use default values shown in brackets")
    print()
    
    # Get user inputs
    num_trials = get_int_input("Number of trials", 1)
    trades_per_trial = get_int_input("Simulated trades per trial", 50)
    profit_min = get_float_input("Profit on winning trades - minimum %", 5.0)
    profit_max = get_float_input("Profit on winning trades - maximum %", 25.0)
    loss_min = get_float_input("Loss on losing trades - minimum %", 10.0)
    loss_max = get_float_input("Loss on losing trades - maximum %", 25.0)
    win_percentage = get_float_input("Win percentage", 75.0)
    starting_capital = get_float_input("Starting Capital $", 100000.0)
    overhead_percent = get_float_input("Overhead Percent (commissions/slippage)", 0.3)
    overhead_percent = overhead_percent / 100  # Convert to decimal
    moving_avg_bars = get_int_input("Moving average bars", 30)
    
    # Create simulator
    simulator = TradeSimulator(
        num_trials=num_trials,
        trades_per_trial=trades_per_trial,
        profit_min=profit_min,
        profit_max=profit_max,
        loss_min=loss_min,
        loss_max=loss_max,
        win_percentage=win_percentage,
        starting_capital=starting_capital,
        overhead_percent=overhead_percent,
        moving_avg_bars=moving_avg_bars
    )
    
    print("\nRunning simulation...")
    summary = simulator.run_simulation()
    
    print_summary(summary, simulator)
    print("\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSimulation cancelled by user.")
        sys.exit(0)
