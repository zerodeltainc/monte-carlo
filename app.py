import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from trade_simulator import TradeSimulator, SimulationSummary
import random

# Set page config
st.set_page_config(
    page_title="Trade Simulator",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 Trade Simulator - Monte Carlo Analysis")
st.markdown("Simulate trading performance using user-defined parameters")

# Sidebar for inputs
st.sidebar.header("Simulation Parameters")

# Input fields
num_trials = st.sidebar.number_input(
    "Number of trials",
    min_value=1,
    max_value=100,
    value=1,
    help="Number of trial sets to run"
)

trades_per_trial = st.sidebar.number_input(
    "Simulated trades per trial",
    min_value=10,
    max_value=1000,
    value=50,
    help="Number of trades in each trial"
)

st.sidebar.subheader("Profit/Loss Parameters")

col1, col2 = st.sidebar.columns(2)
with col1:
    profit_min = st.number_input(
        "Profit min %",
        min_value=0.1,
        max_value=100.0,
        value=5.0,
        step=0.5
    )
with col2:
    profit_max = st.number_input(
        "Profit max %",
        min_value=0.1,
        max_value=100.0,
        value=25.0,
        step=0.5
    )

col3, col4 = st.sidebar.columns(2)
with col3:
    loss_min = st.number_input(
        "Loss min %",
        min_value=0.1,
        max_value=100.0,
        value=10.0,
        step=0.5
    )
with col4:
    loss_max = st.number_input(
        "Loss max %",
        min_value=0.1,
        max_value=100.0,
        value=25.0,
        step=0.5
    )

win_percentage = st.sidebar.slider(
    "Win percentage",
    min_value=0.0,
    max_value=100.0,
    value=75.0,
    step=0.5,
    help="Probability of winning trades"
)

st.sidebar.subheader("Capital & Costs")

starting_capital = st.sidebar.number_input(
    "Starting Capital ($)",
    min_value=1000.0,
    max_value=10000000.0,
    value=100000.0,
    step=1000.0
)

overhead_percent = st.sidebar.number_input(
    "Overhead Percent (%)",
    min_value=0.0,
    max_value=10.0,
    value=0.3,
    step=0.01,
    help="Commissions and slippage"
)

moving_avg_bars = st.sidebar.number_input(
    "Moving average bars",
    min_value=5,
    max_value=200,
    value=30
)

# Run simulation button
run_simulation = st.sidebar.button("🚀 Run Simulation", type="primary", use_container_width=True)

# Initialize session state
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'simulator' not in st.session_state:
    st.session_state.simulator = None
if 'equity_curve' not in st.session_state:
    st.session_state.equity_curve = None

def simulate_equity_curve(simulator):
    """Generate equity curve for visualization"""
    equity = simulator.starting_capital
    equity_curve = [equity]
    
    for _ in range(simulator.trades_per_trial):
        trade = simulator.simulate_trade(equity)
        equity += trade.profit
        equity_curve.append(equity)
    
    return equity_curve

# Run simulation when button is clicked
if run_simulation:
    with st.spinner("Running simulation..."):
        simulator = TradeSimulator(
            num_trials=num_trials,
            trades_per_trial=trades_per_trial,
            profit_min=profit_min,
            profit_max=profit_max,
            loss_min=loss_min,
            loss_max=loss_max,
            win_percentage=win_percentage,
            starting_capital=starting_capital,
            overhead_percent=overhead_percent / 100,
            moving_avg_bars=moving_avg_bars
        )
        
        summary = simulator.run_simulation()
        
        # Generate equity curve for single trial visualization
        random.seed(42)  # Set seed for reproducibility
        equity_curve = simulate_equity_curve(simulator)
        
        st.session_state.summary = summary
        st.session_state.simulator = simulator
        st.session_state.equity_curve = equity_curve
        
        st.success("✅ Simulation complete!")

# Display results if simulation has been run
if st.session_state.summary is not None:
    summary = st.session_state.summary
    simulator = st.session_state.simulator
    equity_curve = st.session_state.equity_curve
    
    # Main metrics in columns
    st.header("Trade Performance Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Net Profit",
            f"${summary.total_net_profit:,.2f}",
            delta=f"{(summary.total_net_profit/simulator.starting_capital*100):.2f}%"
        )
    
    with col2:
        st.metric(
            "Win Rate",
            f"{summary.win_rate:.1f}%",
            delta=f"{summary.wins}/{summary.wins + summary.losses}"
        )
    
    with col3:
        st.metric(
            "Expectancy",
            f"${summary.expectancy:,.2f}"
        )
    
    with col4:
        st.metric(
            "Profit Factor",
            f"{summary.profit_factor:.2f}"
        )
    
    # Equity curve chart
    st.header("Equity Curve")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=list(range(len(equity_curve))),
        y=equity_curve,
        mode='lines',
        name='Equity',
        line=dict(color='#1f77b4', width=2)
    ))
    
    # Add moving average
    if len(equity_curve) >= moving_avg_bars:
        moving_avg = []
        for i in range(len(equity_curve)):
            if i < moving_avg_bars:
                moving_avg.append(sum(equity_curve[:i+1]) / (i+1))
            else:
                moving_avg.append(sum(equity_curve[i-moving_avg_bars+1:i+1]) / moving_avg_bars)
        
        fig.add_trace(go.Scatter(
            x=list(range(len(moving_avg))),
            y=moving_avg,
            mode='lines',
            name=f'{moving_avg_bars}-bar MA',
            line=dict(color='red', width=2, dash='dash')
        ))
    
    fig.update_layout(
        xaxis_title="Trade Number",
        yaxis_title="Equity ($)",
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed statistics in tabs
    tab1, tab2, tab3 = st.tabs(["📊 Statistics", "📉 Risk Metrics", "🎲 Streak Odds"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Trade Statistics")
            stats_data = {
                "Metric": [
                    "Total Trades",
                    "Winning Trades",
                    "Losing Trades",
                    "Win Rate",
                    "Average Profit",
                    "Average Loss",
                    "Expectancy"
                ],
                "Value": [
                    f"{summary.wins + summary.losses}",
                    f"{summary.wins}",
                    f"{summary.losses}",
                    f"{summary.win_rate:.2f}%",
                    f"${summary.average_profit:,.2f}",
                    f"(${abs(summary.average_loss):,.2f})",
                    f"${summary.expectancy:,.2f}"
                ]
            }
            st.dataframe(pd.DataFrame(stats_data), hide_index=True, use_container_width=True)
        
        with col2:
            st.subheader("Equity Statistics")
            equity_data = {
                "Metric": [
                    "Starting Equity",
                    "Ending Equity",
                    "Equity High",
                    "Equity Low",
                    "Net Profit/Loss",
                    "Return %",
                    "Profit Factor"
                ],
                "Value": [
                    f"${simulator.starting_capital:,.2f}",
                    f"${summary.ending_equity:,.2f}",
                    f"${summary.equity_high:,.2f}",
                    f"${summary.equity_low:,.2f}",
                    f"${summary.total_net_profit:,.2f}",
                    f"{(summary.total_net_profit/simulator.starting_capital*100):.2f}%",
                    f"{summary.profit_factor:.2f}"
                ]
            }
            st.dataframe(pd.DataFrame(equity_data), hide_index=True, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Drawdown Analysis")
            dd_data = {
                "Metric": [
                    "Max Drawdown ($)",
                    "Max Drawdown (%)",
                    "Max DD / Avg Profit",
                    "Probability of Ruin"
                ],
                "Value": [
                    f"${summary.max_drawdown_dollars:,.2f}",
                    f"{summary.max_drawdown_percent:.2f}%",
                    f"{summary.max_dd_avg_profit_ratio:.2f}",
                    f"{summary.probability_of_ruin:.4f}%"
                ]
            }
            st.dataframe(pd.DataFrame(dd_data), hide_index=True, use_container_width=True)
        
        with col2:
            st.subheader("Consecutive Streaks")
            streak_data = {
                "Metric": [
                    "Max Consecutive Wins",
                    "Max Consecutive Losses"
                ],
                "Value": [
                    f"{summary.max_consecutive_wins}",
                    f"{summary.max_consecutive_losses}"
                ]
            }
            st.dataframe(pd.DataFrame(streak_data), hide_index=True, use_container_width=True)
    
    with tab3:
        st.subheader("Odds of Losing Streaks")
        
        streak_odds = simulator.calculate_losing_streak_odds()
        odds_data = {
            "Losing Streak": [f"{i} losses in a row" for i in range(2, 11)],
            "Odds": [f"{odds:,.0f}:1" if odds != float('inf') else "N/A" 
                     for odds in streak_odds.values()]
        }
        
        st.dataframe(pd.DataFrame(odds_data), hide_index=True, use_container_width=True)
        
        st.info("💡 These odds show the probability of experiencing consecutive losing trades based on your win percentage.")

else:
    # Show instructions when no simulation has been run
    st.info("👈 Configure parameters in the sidebar and click '🚀 Run Simulation' to start")
    
    st.markdown("""
    ### How to use the Trade Simulator
    
    1. **Set Parameters**: Adjust the simulation parameters in the left sidebar
        - Number of trials: How many simulation runs to perform
        - Trades per trial: Number of trades in each simulation
        - Profit/Loss ranges: Min/max percentage gains and losses
        - Win percentage: Probability of winning trades
        - Starting capital: Initial account balance
        - Overhead: Commissions and slippage percentage
    
    2. **Run Simulation**: Click the "Run Simulation" button
    
    3. **Analyze Results**: Review the performance metrics, equity curve, and statistics
    
    ### Key Metrics Explained
    
    - **Expectancy**: Average profit/loss per trade (positive = profitable system)
    - **Profit Factor**: Ratio of gross profit to gross loss (>1 = profitable)
    - **Maximum Drawdown**: Largest peak-to-trough decline
    - **Probability of Ruin**: Likelihood of losing money over the simulation period
    """)

# Footer
st.markdown("---")
st.markdown("Trade Simulator - Monte Carlo Analysis Tool | Built with Streamlit")
