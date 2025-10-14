#!/usr/bin/env python3
"""
Test script for the trade simulator using default parameters
"""

from trade_simulator import TradeSimulator, print_summary

def test_default_simulation():
    """Test the simulator with default parameters"""
    print("\n" + "="*60)
    print("RUNNING TEST WITH DEFAULT PARAMETERS")
    print("="*60)
    
    simulator = TradeSimulator(
        num_trials=1,
        trades_per_trial=50,
        profit_min=5.0,
        profit_max=25.0,
        loss_min=10.0,
        loss_max=25.0,
        win_percentage=75.0,
        starting_capital=100000.0,
        overhead_percent=0.003,
        moving_avg_bars=30
    )
    
    print("\nParameters:")
    print(f"  Number of trials: {simulator.num_trials}")
    print(f"  Trades per trial: {simulator.trades_per_trial}")
    print(f"  Profit range: {simulator.profit_min*100}% to {simulator.profit_max*100}%")
    print(f"  Loss range: {simulator.loss_min*100}% to {simulator.loss_max*100}%")
    print(f"  Win percentage: {simulator.win_percentage*100}%")
    print(f"  Starting capital: ${simulator.starting_capital:,.2f}")
    print(f"  Overhead: {simulator.overhead_percent*100}%")
    
    print("\nRunning simulation...")
    summary = simulator.run_simulation()
    
    print_summary(summary, simulator)


def test_multiple_trials():
    """Test with multiple trials to show statistical distribution"""
    print("\n" + "="*60)
    print("RUNNING TEST WITH MULTIPLE TRIALS")
    print("="*60)
    
    simulator = TradeSimulator(
        num_trials=10,
        trades_per_trial=100,
        profit_min=5.0,
        profit_max=20.0,
        loss_min=10.0,
        loss_max=20.0,
        win_percentage=60.0,
        starting_capital=50000.0,
        overhead_percent=0.005,
        moving_avg_bars=20
    )
    
    print("\nParameters:")
    print(f"  Number of trials: {simulator.num_trials}")
    print(f"  Trades per trial: {simulator.trades_per_trial}")
    print(f"  Profit range: {simulator.profit_min*100}% to {simulator.profit_max*100}%")
    print(f"  Loss range: {simulator.loss_min*100}% to {simulator.loss_max*100}%")
    print(f"  Win percentage: {simulator.win_percentage*100}%")
    print(f"  Starting capital: ${simulator.starting_capital:,.2f}")
    
    print("\nRunning simulation...")
    summary = simulator.run_simulation()
    
    print_summary(summary, simulator)


if __name__ == "__main__":
    test_default_simulation()
    print("\n" + "="*60 + "\n")
    test_multiple_trials()
