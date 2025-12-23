"""
Main entry point with configuration file support.
"""
import os
import configparser
from data_loader import DataLoader
from strategy import FVGStrategy
from backtest import Backtest
from visualization import Visualizer


def load_config(config_file='config.ini'):
    """Load configuration from INI file."""
    config = configparser.ConfigParser()
    
    # Set defaults
    defaults = {
        'data': {
            'start_year': '2018',
            'end_year': '2025',
            'session_start_hour': '2',
            'session_start_minute': '0',
            'session_end_hour': '6',
            'session_end_minute': '0'
        },
        'strategy': {
            'risk_reward_ratio': '1.0',
            'swing_lookback': '5'
        },
        'backtest': {
            'initial_capital': '100000'
        },
        'output': {
            'trade_journal': 'trade_journal.csv',
            'equity_curve': 'equity_curve.png',
            'trade_distribution': 'trade_distribution.png',
            'monthly_returns': 'monthly_returns.png',
            'sample_trades': 'sample_trades.png',
            'num_sample_trades': '10'
        }
    }
    
    # Read config file if it exists
    if os.path.exists(config_file):
        config.read(config_file)
    
    # Merge with defaults
    for section, values in defaults.items():
        if not config.has_section(section):
            config.add_section(section)
        for key, value in values.items():
            if not config.has_option(section, key):
                config.set(section, key, value)
    
    return config


def main():
    """Run the complete backtesting system with configuration."""
    
    print("="*60)
    print("NQ FAIR VALUE GAP BACKTESTING SYSTEM")
    print("="*60)
    print()
    
    # Load configuration
    config = load_config()
    
    # Extract parameters from config
    START_YEAR = config.getint('data', 'start_year')
    END_YEAR = config.getint('data', 'end_year')
    SESSION_START_HOUR = config.getint('data', 'session_start_hour')
    SESSION_START_MINUTE = config.getint('data', 'session_start_minute')
    SESSION_END_HOUR = config.getint('data', 'session_end_hour')
    SESSION_END_MINUTE = config.getint('data', 'session_end_minute')
    RISK_REWARD_RATIO = config.getfloat('strategy', 'risk_reward_ratio')
    SWING_LOOKBACK = config.getint('strategy', 'swing_lookback')
    INITIAL_CAPITAL = config.getfloat('backtest', 'initial_capital')
    
    # Output filenames
    TRADE_JOURNAL = config.get('output', 'trade_journal')
    EQUITY_CURVE = config.get('output', 'equity_curve')
    TRADE_DIST = config.get('output', 'trade_distribution')
    MONTHLY_RET = config.get('output', 'monthly_returns')
    SAMPLE_TRADES = config.get('output', 'sample_trades')
    NUM_SAMPLE_TRADES = config.getint('output', 'num_sample_trades')
    
    DATA_DIRECTORY = "."
    
    print("Configuration:")
    print(f"  Period: {START_YEAR} - {END_YEAR}")
    print(f"  Trading Session: {SESSION_START_HOUR:02d}:{SESSION_START_MINUTE:02d} - {SESSION_END_HOUR:02d}:{SESSION_END_MINUTE:02d}")
    print(f"  Risk/Reward Ratio: {RISK_REWARD_RATIO}:1")
    print(f"  Swing Lookback: {SWING_LOOKBACK} candles")
    print(f"  Initial Capital: ${INITIAL_CAPITAL:,.2f}")
    print()
    
    # Step 1: Load data
    print("Step 1: Loading data...")
    print("-" * 60)
    loader = DataLoader(data_directory=DATA_DIRECTORY)
    df = loader.load_data(start_year=START_YEAR, end_year=END_YEAR)
    print()
    
    # Step 2: Filter to trading session
    print("Step 2: Filtering to trading session...")
    print("-" * 60)
    df = loader.filter_trading_session(
        df, 
        start_hour=SESSION_START_HOUR,
        start_minute=SESSION_START_MINUTE,
        end_hour=SESSION_END_HOUR,
        end_minute=SESSION_END_MINUTE
    )
    print()
    
    # Step 3: Add session markers
    print("Step 3: Adding session markers...")
    print("-" * 60)
    df = loader.add_session_markers(df)
    print()
    
    # Step 4: Initialize strategy
    print("Step 4: Initializing strategy...")
    print("-" * 60)
    strategy = FVGStrategy(
        risk_reward_ratio=RISK_REWARD_RATIO,
        swing_lookback=SWING_LOOKBACK
    )
    print("Strategy initialized")
    print()
    
    # Step 5: Detect FVGs
    print("Step 5: Detecting Fair Value Gaps...")
    print("-" * 60)
    df = strategy.detect_fvg(df)
    total_fvgs = df['fvg_type'].notna().sum()
    bearish_fvgs = (df['fvg_type'] == 'bearish').sum()
    bullish_fvgs = (df['fvg_type'] == 'bullish').sum()
    print(f"Total FVGs detected: {total_fvgs}")
    print(f"  Bearish FVGs: {bearish_fvgs}")
    print(f"  Bullish FVGs: {bullish_fvgs}")
    print()
    
    # Step 6: Identify first FVG per session
    print("Step 6: Identifying first FVG per session...")
    print("-" * 60)
    df = strategy.get_first_fvg_per_session(df)
    first_fvgs = df['first_fvg_of_session'].sum()
    print(f"First FVGs per session: {first_fvgs}")
    print()
    
    # Step 7: Check for FVG fill and reversal signals
    print("Step 7: Checking for entry signals...")
    print("-" * 60)
    df = strategy.check_fvg_fill_and_reversal(df)
    total_signals = df['entry_signal'].notna().sum()
    long_signals = (df['entry_signal'] == 'long').sum()
    short_signals = (df['entry_signal'] == 'short').sum()
    print(f"Total entry signals: {total_signals}")
    print(f"  LONG signals: {long_signals}")
    print(f"  SHORT signals: {short_signals}")
    print()
    
    # Step 8: Run backtest
    print("Step 8: Running backtest...")
    print("-" * 60)
    backtest = Backtest(strategy, initial_capital=INITIAL_CAPITAL)
    trades = backtest.run(df)
    print()
    
    # Step 9: Calculate and display statistics
    print("Step 9: Calculating performance statistics...")
    print("-" * 60)
    backtest.print_statistics()
    
    # Step 10: Export results
    print("Step 10: Exporting results...")
    print("-" * 60)
    backtest.export_trades(TRADE_JOURNAL)
    print()
    
    # Step 11: Generate visualizations
    print("Step 11: Generating visualizations...")
    print("-" * 60)
    visualizer = Visualizer()
    
    if trades:
        visualizer.plot_equity_curve(trades, INITIAL_CAPITAL, EQUITY_CURVE)
        visualizer.plot_trade_distribution(trades, TRADE_DIST)
        visualizer.plot_monthly_returns(trades, MONTHLY_RET)
        visualizer.plot_sample_trades(df, trades, num_trades=min(NUM_SAMPLE_TRADES, len(trades)), filename=SAMPLE_TRADES)
    else:
        print("No trades to visualize.")
    print()
    
    print("="*60)
    print("BACKTEST COMPLETE!")
    print("="*60)
    print()
    print("Generated files:")
    print(f"  - {TRADE_JOURNAL} (detailed trade log)")
    print(f"  - {EQUITY_CURVE} (equity over time)")
    print(f"  - {TRADE_DIST} (trade statistics)")
    print(f"  - {MONTHLY_RET} (monthly P&L)")
    print(f"  - {SAMPLE_TRADES} (sample trade charts)")
    print()


if __name__ == "__main__":
    main()
